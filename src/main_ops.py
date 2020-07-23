#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains the main operations which can be done on the web platform.

@author: Lidia Sánchez Mérida
"""
import os
import sys
sys.path.append('src/data')
sys.path.append('data')
from api import Api
import commondata
import data_analyzer
from mongodb import MongoDB
from postgresql import PostgreSQL
from exceptions import UsernameNotFound, MaxRequestsExceed, UserDataNotFound \
    , InvalidSocialMediaSource, InvalidDatabaseCredentials, InvalidMongoDbObject \
    , InvalidAnalysis, InvalidPreferences

class MainOperations:

    def __init__(self):
        """Constructor. It creates a MainOperations objects whose attributes are:
            - CommonData object to preprocess the common data.
            - MongoDB object to work with the first database.
            - DataAnalyzer object to perform the different avalaible analysis.
            - A list with the different avalaible analysis to perform.
            - PostgreSQL object to insert and get data from the SQL tables.
        """
        psql_user = os.environ.get("POSTGRES_USER")
        psql_pswd = os.environ.get("POSTGRES_PSWD")
        if (type(psql_user) != str or type(psql_pswd) != str or psql_user == "" or psql_pswd == ""):
            raise InvalidDatabaseCredentials("ERROR. PostgreSQL should be non-empty strings.")
            
        self.mongodb = MongoDB('profiles')
        self.common_data = commondata.CommonData(self.mongodb)
        self.data_analysis = data_analyzer.DataAnalyzer()
        self.avalaible_analysis = ["ProfileEvolution", "SortPosts", "PostsEvolution",
                         "FollowersActivity", "ContactsActivity", "GeneralBehaviour", "Haters/Friends"]
        self.postgresql = PostgreSQL()

    def get_user_instagram_common_data(self, search_user):
        """Downloads Instagram data of a specific user using the LevPasha Instagram
            API and stores the main fields in a MongoDB database."""
        if (search_user == None or type(search_user) != str or search_user == ""):
            raise UsernameNotFound("ERROR. Invalid username.")
        try:
            """Connect to the Levpasha Instagram API"""
            inst_api = Api()
            inst_api.connect_levpasha_instagram_api()
            """Download Instagram user data"""
            user_instagram_data = inst_api.get_levpasha_instagram_data(search_user)
            """Preprocess and store user data"""
            user_data = self.preprocess_and_store_common_data(user_instagram_data, 'Instagram')
            return user_data
        except MaxRequestsExceed:   # pragma: no cover
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")

    def preprocess_and_store_common_data(self, user_data, social_media):
        """Preprocesses and stores user data from any API source into the MongoDB database."""
        if (type(user_data) != dict or len(user_data) == 0):
            raise UserDataNotFound("ERROR. User data should be a non empty dict.")
        if (type(social_media) != str or social_media == ""):
            raise InvalidSocialMediaSource("ERROR. Social media type should be a non empty string.")
        if (type(self.mongodb) != MongoDB):
            raise InvalidMongoDbObject("ERROR. The connection to the MongoDB database "+
                                       "should be a MongoDB object.")
            
        # Preprocess data
        cd = commondata.CommonData(self.mongodb)
        prep_user_data = cd.preprocess_user_data(user_data)
        """Store preprocessed user profile to MongoDB collection 'profiles'"""
        profile = cd.add_user_data(prep_user_data['profile']['username'],
            prep_user_data['profile'], 'profiles', social_media)

        """Store user posts, their likers and comments into the same MongoDB collection 'posts'"""
        all_posts = {}
        all_posts['posts'] = prep_user_data['posts']
        all_posts['likers'] = prep_user_data['likers']
        all_posts['comments'] = prep_user_data['comments']
        posts = cd.add_user_data(prep_user_data['profile']['username'],
              all_posts, 'posts', social_media)
        """Store the user followings and followers into the same MongoDB collection 'contacts'."""
        all_contacts = {}
        all_contacts['followings'] = prep_user_data['followings']
        all_contacts['followers'] = prep_user_data['followers']
        contacts = cd.add_user_data(prep_user_data['profile']['username'],
            all_contacts, 'contacts', social_media)

        """Return the final user data"""
        result = {'profile':None, 'posts':None, 'contacts': None}
        result['profile'] = profile[1]
        result['contacts'] = contacts[1]
        result['posts'] = posts[1]

        return result
    
    # def perform_analysis(self, data_analysis):
    #     """Method which searchs for the required data to the Mongo database in 
    #         order to preprocess and store them in the PostgreSQL database. Then,
    #         depending on the type of analysis and specified preferences, it gets
    #         the required data from PostgreSQL in order to perform the specified analysis.
    #     """
    ######## VER SI ES UN DICT
    ######## CAMPOS OBLIGATORIOS Y NO VACÍOS: user, analysis
    ##### OBTENER LOS DATOS DE MONGODB EN FUNCIÓN DEL ANÁLISIS ELEGIDO
    ##### FILTRARLOS POR LAS FECHAS QUE SEAN PROPORCIONANDOLAS PARA QUE EL USUARIO ESCOJA SOBRE SEGURO
    ##### VER LAS PREFERENCIAS EN FUNCIÓN DEL ANÁLISIS QUE SEA Y PONER LAS EXCEPCIONES
    ###### PARÁMETROS DEL DICT: {'user':<username>, 'init_date':<str or None>, 'fin_date':<str or None>,
    ######                          'analysis':<str>, 'preferences':{}}