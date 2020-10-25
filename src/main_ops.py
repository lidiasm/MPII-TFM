#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains the main operations which can be done on the web platform.

@author: Lidia Sánchez Mérida
"""
import os
import sys
from datetime import date

sys.path.append('src/data')
sys.path.append('data')
from api import Api
import commondata
#import data_analyzer
from mongodb import MongoDB
from postgredb import PostgreDB
from exceptions import UsernameNotFound, MaxRequestsExceed, UserDataNotFound \
   , InvalidDatabaseCredentials, InvalidMongoDbObject, InvalidSocialMediaSource

class MainOperations:

    def __init__(self):
        """
        Creates a MainOperations object whose attributes are:
            - A CommonData object to preprocess the user data.
            - A MongoDB object to operate with the Mongo database.
            - A DataAnalyzer object to perform the different avalaible analysis.
            - A list with the different avalaible analysis to perform.
            - A PostgreDB object to insert and get data from the SQL tables.

        Raises
        ------
        InvalidDatabaseCredentials
            If the credentials are not non-empty strings, are not saved in env
            variables or are wrong.

        Returns
        -------
        A MainOperations object.
        """
        psql_user = os.environ.get("POSTGRES_USER")
        psql_pswd = os.environ.get("POSTGRES_PSWD")
        if (type(psql_user) != str or type(psql_pswd) != str or psql_user == "" or psql_pswd == ""):
            raise InvalidDatabaseCredentials("ERROR. PostgreDB should be non-empty strings.")
            
        self.mongodb = MongoDB('profiles')
        self.common_data = commondata.CommonData(self.mongodb)
        #self.data_analysis = data_analyzer.DataAnalyzer()
        self.avalaible_analysis = ["ProfileEvolution", "SortPosts", "PostsEvolution",
                         "FollowersActivity", "ContactsActivity", "GeneralBehaviour", "Haters/Friends"]
        self.postgredb = PostgreDB()

    def get_user_instagram_common_data(self, search_user):
        """
        Gets common Instagram data of a specific user using the LevPasha Instagram
        API. The downloaded user data is stored in the Mongo database.

        Parameters
        ----------
        search_user : str
            It's the username of the user to get their data.

        Raises
        ------
        UsernameNotFound
            If the provided username is not a non-empty string.
        MaxRequestsExceed
            If the maximum number of requests of the LevPasha Instagram API
            has been exceeded.

        Returns
        -------
        A dict with the downloaded user data.
        """
        if (search_user == None or type(search_user) != str or search_user == ""):
            raise UsernameNotFound("ERROR. Invalid username.")
        try:
            # Connect to the Levpasha Instagram API
            inst_api = Api()
            inst_api.connect_levpasha_instagram_api()
            # Download Instagram user data
            user_instagram_data = inst_api.get_levpasha_instagram_data(search_user)
            # Preprocess and store user data
            user_data = self.preprocess_and_store_common_data(user_instagram_data, "Instagram")
            return user_data
        except MaxRequestsExceed:   # pragma: no cover
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")

    def preprocess_and_store_common_data(self, user_data, social_media):
        """
        Preprocesses the common data of a specific user from any API source and
        stores them in the Mongo database, if there aren't any items with the same
        id and date. In this case, the provided user data won't be inserted.

        Parameters
        ----------
        user_data : dict
            It's the user data to preprocess and store.
        social_media : str
            It's the social media which the user data came from.

        Raises
        ------
        UserDataNotFound
            If the provided user data is not a dict.
        InvalidSocialMediaSource
            If the provided social media source is not a non-empty string or it's
            not one of the avalaible social media sources.
        InvalidMongoDbObject
            If the MongoDB object has not been initialized and does not have the
            connection to the Mongo database.

        Returns
        -------
        A dict whose keys are the different user data and whose values indicate
        if each type of user data has been inserted in the Mongo database. Options are:
            - None, the item has not been inserted.
            - str, the id of the new inserted item.
        """
        if (type(user_data) != dict or len(user_data) == 0):
            raise UserDataNotFound("ERROR. User data should be a non empty dict.")
        # Check the provided social media source
        if (type(social_media) != str or social_media == ""):
            raise InvalidSocialMediaSource("ERROR. The social media source should be a non-empty string.")
        if (social_media.lower() not in self.common_data.social_media_sources):
            raise InvalidSocialMediaSource("ERROR. Avalaible social media sources: "
               +str(self.common_data.social_media_sources))
        
        if (type(self.mongodb) != MongoDB):
            raise InvalidMongoDbObject("ERROR. The connection to the MongoDB database "+
                                       "should be a MongoDB object.")
        
        # Preprocess the user data
        preprocessed_data = self.common_data.preprocess_user_data(user_data, social_media)
        # Common query to each type of user data. The new item won't be inserted
        # if there are some matches (id, date)
        query = {'id':str(preprocessed_data['profile']['userid'])+"_"+preprocessed_data['profile']['social_media'],
                 'date':(date.today()).strftime("%d-%m-%Y")}
        
        # Store the preprocessed profile
        profile = self.common_data.insert_user_data(preprocessed_data['profile'],
                        'profiles', query)
        # Store the preprocessed medias
        medias = self.common_data.insert_user_data(preprocessed_data['media_list'],
                        'medias', query)
        # Store the preprocessed likers from the medias
        likers = self.common_data.insert_user_data(preprocessed_data['media_likers'],
                        'likers', query)
        # Store the preprocessed comments from the medias
        comments = self.common_data.insert_user_data(preprocessed_data['media_comments'],
                        'comments', query)
        # Store the preprocessed followers and followings
        contacts = self.common_data.insert_user_data(preprocessed_data['contacts'],
                        'contacts', query)
        
        return {'profile':profile, 'media':medias, 'likers':likers, 
                'comments':comments, 'contacts':contacts}
    