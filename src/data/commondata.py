#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains the common data to social networks and the preprocessing
methods to verify the values of the collected data.

@author: Lidia Sánchez Mérida
"""
import sys
sys.path.append("../")
import mongodb
from exceptions import InvalidMongoDbObject, ProfileDictNotFound, InvalidTextList \
    , ContactDictNotFound, MediaListNotFound, MediaDictNotFound, LikerListNotFound \
    , TextListNotFound, TextDictNotFound, UserDataNotFound, CollectionNotFound \
    , InvalidQuery, InvalidSocialMediaSource, InvalidUserId, InvalidMediaId, LikerDictNotFound
from datetime import date
from googletrans import Translator
import re

class CommonData:

    def __init__(self, mongodb=None):
        """
        Creates a CommonData object whose attributes are:
            - A MongoDB object to operate with the Mongo database. It could be
                None if the MongoDB operations are not required.
            - The list of the required keys for the user profile.
            - The list of the required keys for the media posts.
            - The list of the required keys for the media likers. 
            - The list of the required keys for the media texts.
            - The list of avalaible social media sources.
            - The list of stopwords to remove from text.

        Parameters
        ----------
        mongodb : MongoDB, optional
            It's the MongoDB object which contains the connection to the Mongo
            database in order to operate with it. The default is None.

        Returns
        -------
        A CommonData object.
        """
        self.mongodb = mongodb
        self.profile_keys = ['userid', 'username', 'name', 'biography', 'gender', 'profile_pic',
          'location', 'birthday', 'date_joined', 'n_followers', 'n_followings', 'n_medias']
        self.media_keys = ['id_media', 'like_count', 'comment_count']
        self.liker_keys = ['id_media', 'users']
        self.text_keys = ['id_media', 'texts']
        self.text_list_keys = ['user', 'text']
        self.social_media_sources = ["instagram"]
        self.stopwords = ['a', 'an', 'the', 'and', 'or', 'i', 'you', 'he', 'she',
                          'it', 'we', 'they', 'my', 'your', 'his', 'her', 'its', 
                          'ours', 'yours', 'them', 'me', 'us']
    
    def set_mongodb_connection(self, mongodb_connection):
        """
        Sets the connection to the Mongo database in order to operate with it.

        Parameters
        ----------
        mongodb_connection : MongoDB
            It's a initialized MongoDB object which contains the connection to 
            the Mongo database.

        Raises
        ------
        InvalidMongoDbObject
            If the provided MongoDB object is not valid.

        Returns
        -------
        The MongoDB object which contains the connection to the Mongo database.
        """
        if (type(mongodb_connection) != mongodb.MongoDB):
            raise InvalidMongoDbObject("ERROR. The connection to the MongoDB database "+
                                       "should be a MongoDB object.")
        self.mongodb = mongodb_connection
        return self.mongodb

    def preprocess_profile(self, user_profile, social_media):
        """
        Preprocesses the dict of the user profile as well as their keys and values.
        If some required key is not found, it'll be added with a default value.

        Parameters
        ----------
        user_profile : dict
            It's the dict which contains the user profile from any social media.
        social_media : str
            It's the social media source which the user data came from.

        Raises
        ------
        ProfileDictNotFound
            If the provided user profile is not a dict.
        UsernameNotFound
            If the provided user profile has not a 'username' key.
        InvalidSocialMediaSource
            If the provided social media source is not a non-empty string or it's
            not one of the avalaible social media sources.

        Returns
        -------
        A dict which contains the preprocessed user profile as well as the social media source.
        """
        # Check the provided user profile
        if (type(user_profile) != dict or user_profile == None):
            raise ProfileDictNotFound("ERROR. User profile should be a dict.")
        # Check the provided data by sorting their keys
        provided_keys = list(user_profile.keys())
        provided_keys.sort()
        self.profile_keys.sort()
        if (provided_keys != self.profile_keys):
            raise ProfileDictNotFound("ERROR. Some required data are missing.")
        # Check the provided social media source
        if (type(social_media) != str or social_media == ""):
            raise InvalidSocialMediaSource("ERROR. The social media source should be a non-empty string.")
        if (social_media.lower() not in self.social_media_sources):
            raise InvalidSocialMediaSource("ERROR. Avalaible social media sources: "+str(self.social_media_sources))
        # Check that the provided user id is valid
        if (type(user_profile['userid']) != int or user_profile['userid'] < 0):
            raise InvalidUserId("ERROR. The profile should have a non-empty id.")
        
        # Check the provided values
        for key in user_profile:
            user_profile[key] = 'None' if user_profile[key] == None else str(user_profile[key])
        
        # Add the social media source
        user_profile['social_media'] = social_media
        return user_profile

    def preprocess_contacts(self, contacts, social_media, userid):
        """
        Preprocesses the list of usernames which are the followers and followings
        of a specific user. 

        Parameters
        ----------
        contacts : dict
            It's the dict with the list of followings and followers.
        social_media : str
            It's the social media which the user data came from.
        userid : str
            It's the id of the studied user account.

        Raises
        ------
        ContactDictNotFound
            If the followers or followings are not in a dict.
        InvalidSocialMediaSource
            If the provided social media source is not a non-empty string or it's
            not one of the avalaible social media sources.
        InvalidUserId
            If the provided user id is not a positive integer.

        Returns
        -------
        A dict which contains the list of preprocessed followers and followings
        as well as the social media source.
        """
        # Check the data type
        if (type(contacts) != dict or len(contacts) == 0):
            raise ContactDictNotFound("ERROR. Contacts should be a non-empty dict.")
        # Check the keys
        if ('followers' not in contacts or 'followings' not in contacts):
            raise ContactDictNotFound("ERROR. Contacts should have 'followers' "+
                  "and 'followings' keys.")
        if (type(contacts['followers']) != list or type(contacts['followings']) != list):
            raise ContactDictNotFound("ERROR. The followers and followings should be in lists.")
        # Check the provided social media source
        if (type(social_media) != str or social_media == ""):
            raise InvalidSocialMediaSource("ERROR. The social media source should be a non-empty string.")
        if (social_media.lower() not in self.social_media_sources):
            raise InvalidSocialMediaSource("ERROR. Avalaible social media sources: "+str(self.social_media_sources))
        # Check the provided user id
        if (type(userid) != str or userid == str):
            raise InvalidUserId("ERROR. The user id should be a non-empty string.")
        
        # Followers and followings only can contain non-empty strings (usernames).
        validFollowers = [follower for follower in contacts['followers'] if type(follower) == str and follower != ""]
        validFollowings = [following for following in contacts['followings'] if type(following) == str and following != ""]

        return {'followers':validFollowers, 'followings':validFollowings, 
                    'social_media':social_media, 'userid':str(userid)}

    def preprocess_medias(self, medias, social_media, userid):
        """
        Preprocesses the list of medias of a specific user. Each media is a dict
        whose keys are: id_media, title, like_count and comment_count in order
        to get their id, title and the number of likes and comments.

        Parameters
        ----------
        medias : list of dicts.
            It's the list of medias of a specific user.
        social_media : str
            It's the social media which the user data came from.
        userid : str
            It's the id of the studied user account.

        Raises
        ------
        MediaListNotFound
            If the provided medias are not in a list.
        MediaDictNotFound
            If the provided medias are not dicts.
        InvalidSocialMediaSource
            If the provided social media source is not a non-empty string or it's
            not one of the avalaible social media sources.
        InvalidUserId
            If the provided user id is not a non-empty string.

        Returns
        -------
        A new dict which contains the list of media data as well as the social media source.
        """
        # Check the provided medias
        if (type(medias) != list or len(medias) == 0):
            raise MediaListNotFound("ERROR. The medias of an user should be in a list of dicts.")
        # Check the items of the list
        if (not all(isinstance(record, dict) for record in medias)):
            raise MediaDictNotFound("ERROR. Medias should be a non-empty list of dicts.")
        # Check the provided social media source
        if (type(social_media) != str or social_media == ""):
            raise InvalidSocialMediaSource("ERROR. The social media source should be a non-empty string.")
        if (social_media.lower() not in self.social_media_sources):
            raise InvalidSocialMediaSource("ERROR. Avalaible social media sources: "+str(self.social_media_sources))
        # Check the provided user id
        if (type(userid) != str or userid == ""):
            raise InvalidUserId("ERROR. The user id should be a non-empty string.")
        
        # Preprocessing
        for media in medias:
            # Check the provided data
            media_keys = list(media.keys())
            media_keys.sort()
            self.media_keys.sort()
            if (media_keys != self.media_keys):
                raise MediaDictNotFound("ERROR. Some of the required data are missing.")
            # Check that each media has its id
            if (type(media['id_media']) != str or media['id_media'] == ""):
                raise InvalidMediaId("ERROR. Each media should have a non-empty string.")
            # Transform the media id to string
            media['id_media'] = str(media['id_media'])
            # Check the provided values
            for key in media:
                # Preprocess the None values
                media[key] = 'None' if media[key] == None else str(media[key])
        
        # Add the preprocessed medias
        preprocessed_medias = {}
        preprocessed_medias['medias'] = medias
        # Add the social media source
        preprocessed_medias["social_media"] = social_media 
        # Add the id of the user who owns the media posts
        preprocessed_medias["userid"] = userid
        return preprocessed_medias

    def preprocess_media_likers(self, likers, social_media, userid):
        """
        Preprocesses the list of people who liked the medias of a specific user.
        All usernames which are not strings will be deleted.

        Parameters
        ----------
        likers : list of dicts
            It's the list of dicts in which there are the list of users who liked
            the medias of a specific user.
        social_media : str
            It's the social media which the user data came from.
        userid : str
            It's the id of the studied user account.

        Raises
        ------
        LikerListNotFound
            If the provided likers are not in a list of strings.
        InvalidSocialMediaSource
            If the provided social media source is not a non-empty string or it's
            not one of the avalaible social media sources.
        InvalidUserId
            If the provided user id is not a non-empty string.

        Returns
        -------
        A dict with the list of people who liked the medias of a specific user as
        well as the social media source.
        """
        # Check if the likers are in a list
        if (type(likers) != list or len(likers) == 0):
            raise LikerListNotFound("ERROR. Likers should be a non-empty list.")
        # Check the items of the list
        if (not all(isinstance(record, dict) for record in likers)):
            raise LikerListNotFound("ERROR. Likers should be a non-empty list of dicts.")
        # Check the provided social media source
        if (type(social_media) != str or social_media == ""):
            raise InvalidSocialMediaSource("ERROR. The social media source should be a non-empty string.")
        if (social_media.lower() not in self.social_media_sources):
            raise InvalidSocialMediaSource("ERROR. Avalaible social media sources: "+str(self.social_media_sources))
        # Check the provided user id
        if (type(userid) != str or userid == ""):
            raise InvalidUserId("ERROR. The user id should be a non-empty string.")
        
        # Preprocessing
        for media in likers:
            # Check the provided data
            media_liker_keys = list(media.keys())
            media_liker_keys.sort()
            self.liker_keys.sort()
            if (media_liker_keys != self.liker_keys):
                raise LikerDictNotFound("ERROR. Some of the required data are missing.")
            # Check that each media has its id
            if (type(media['id_media']) != str or media['id_media'] == ""):
                raise InvalidMediaId("ERROR. Each media should have its id as a non-empty string.")
            # Transform the media id to string
            media['id_media'] = str(media['id_media'])
            # Check the provided list of likers
            ## It could be an empty list in case the media hasn't been liked by anyone
            if (type(media['users']) != list):
                raise LikerListNotFound("ERROR. The people who liked the medias should be in a non-empty list.")
            prep_users = [user for user in media['users'] if type(user) == str and user != ""]
            media['users'] = prep_users
            
        # Final liker dict to return
        preprocessed_likers = {}
        preprocessed_likers['likers'] = likers
        preprocessed_likers['social_media'] = social_media
        preprocessed_likers['userid'] = userid
        
        return preprocessed_likers

    def preprocess_media_comments(self, comments, social_media, userid):
        """
        Preprocesses the comments wrote by the users on the medias of a specific
        user account.

        Parameters
        ----------
        comments : list of dicts
            It's the list of comments for each media whose fields contains the user
            who wrote the text and the text itself.
        social_media : str
            It's the social media which the user data came from.
        userid : int
            It's the id of the studied user account.

        Raises
        ------
        TextListNotFound
            If the texts from the medias are not in a list.
        TextDictNotFound
            If the media data is not in a dict.
        InvalidSocialMediaSource
            If the provided social media source is not a non-empty string or it's
            not one of the avalaible social media sources.
        InvalidUserId
            If the provided user id is not a positive integer.

        Returns
        -------
        A dict with the media texts as well as the social media source.
        """
        # Check if the likers are in a list
        if (type(comments) != list or len(comments) == 0):
            raise TextListNotFound("ERROR. Texts should be a non-empty list.")
        # Check the items of the list
        if (not all(isinstance(record, dict) for record in comments)):
            raise TextListNotFound("ERROR. Texts should be a non-empty list of dicts.")
        # Check the provided social media source
        if (type(social_media) != str or social_media == ""):
            raise InvalidSocialMediaSource("ERROR. The social media source should be a non-empty string.")
        if (social_media.lower() not in self.social_media_sources):
            raise InvalidSocialMediaSource("ERROR. Avalaible social media sources: "+str(self.social_media_sources))
        # Check the provided user id
        if (type(userid) != str or userid == ""):
            raise InvalidUserId("ERROR. The user id should be a non-empty string.")
        
        # Preprocessing
        for media in comments:
            # Check the provided data
            media_text_keys = list(media.keys())
            media_text_keys.sort()
            self.text_keys.sort()
            if (media_text_keys != self.text_keys):
                raise TextDictNotFound("ERROR. Some of the required data are missing.")
            # Check that each media has its id
            if (type(media['id_media']) != str or media['id_media'] == ""):
                raise InvalidMediaId("ERROR. Each media should have its id as a non-empty string.")
            # Transform the media id to string
            media['id_media'] = str(media['id_media'])
            
            # Check that the texts are in a list
            ## But it could be an empty list in case the media hasn't got any comments
            
            print(type(media['texts']))
            print(media['texts'])
            if (type(media['texts']) != list):
                raise TextListNotFound("ERROR. The texts from the medias should be in a non-empty list.")
            # Check that each text wrote from a user is in a dict
            if (not all(isinstance(record, dict) for record in media['texts'])):
                raise TextListNotFound("ERROR. The texts from the medias should be in a non-empty list.")
            # Check the required keys and values
            preproc_texts = []
            for record in media['texts']:
                record_keys = list(record.keys())
                record_keys.sort()
                self.text_list_keys.sort()
                if (record_keys != self.text_list_keys):
                    raise TextDictNotFound("ERROR. Some of the required data are missing.")
                # Check data types of the values
                if (type(record['user']) == str and record['user'] != "" and
                    type(record['text']) == str and record['text'] != ""):
                    preproc_texts.append({'user':record['user'], 'text':record['text']})
            # Update the preprocessed texts
            media['texts'] = preproc_texts
            
        # Final text dict to return
        preprocessed_texts = {}
        preprocessed_texts['comments'] = comments
        preprocessed_texts['social_media'] = social_media
        preprocessed_texts['userid'] = userid
        
        return preprocessed_texts
    
    def preprocess_user_data(self, user_data, social_media):
        """
        Preprocesses the social media user data such as the profile, medias, likers,
        texts as well as the followers and followings.

        Parameters
        ----------
        user_data : dict
            It's the dict which contains the user data from any social media.
        social_media : str
            It's the social media which the user data came from.

        Returns
        -------
        A dict with the preprocessed user data from any social media.
        """
        profile = self.preprocess_profile(user_data['profile'], social_media)
        # Get the user id 
        userid = profile['userid']
        contacts = self.preprocess_contacts(user_data['contacts'], social_media, userid)
        medias = self.preprocess_medias(user_data['medias'], social_media, userid)
        likers = self.preprocess_media_likers(user_data['likers'], social_media, userid)
        comments = self.preprocess_media_comments(user_data['comments'], social_media, userid)
        data = {'profile':profile, 'media_list':medias, 'media_likers':likers, 
                'media_comments':comments, 'contacts':contacts}
        return data

    def clean_texts(self, texts):
        """
        Cleans a list of text by applying this set of operations.
            - Translate the text to English.
            - Remove specific stopwords like some prepositions, pronouns, etc.
            - Remove numbers.
            - Remove some useless special characters.

        Parameters
        ----------
        texts : list of strings.
            It's the list of texts to clean.

        Raises
        ------
        TextListNotFound
            If the provided texts are not in a non-empty list.
        InvalidTextList
            If the provided list of texts are not non-empty strings.

        Returns
        -------
        A list of strings with the preprocessed texts.
        """
        # Check the provided list of text
        if (type(texts) != list or len(texts) == 0):
            raise TextListNotFound("ERROR. The texts to clean should be in a non-empty list.")
        # Check the elements of the list
        if (not all(isinstance(text, str) for text in texts)):
            raise InvalidTextList("ERROR. All texts should be non-empty strings.")
        
        # Google Translator object
        translator = Translator()
        # Clean the texts
        cleaned_texts = []
        for text in texts:
            # Translate to English
            english_text = (translator.translate(text, dest="en")).text
            # Remove specific stopwords
            english_words = english_text.split()
            non_stopwords = [word for word in english_words if word.lower() not in self.stopwords]
            non_stopwords = ' '.join(non_stopwords)
            # Remove numbers
            non_numbers = re.sub(r"\d+", "", non_stopwords)
            # Remove some special characters
            non_special_characters = re.sub(r'[#@\"\-"*$%&\+\_]', ' ', non_numbers)
            # Add the cleaned text to the list of cleaned texts
            cleaned_texts.append(non_special_characters)
        
        return cleaned_texts

    def insert_user_data(self, user_data, collection, query=None):
        """
        Inserts user data from any social media source in a collection of Mongo
        database. In order to identify each document and when it was inserted,
        two keys will be added to every document to insert:
            - An id composed by the userid+social_media to avoid troubles if two
            user ids are the same from different social media source.
            - The date which the document was inserted in the Mongo database, in
            order to not insert so much data from one user in the same day.

        Parameters
        ----------
        user_data : dict
            It's the user data from any social media source.
        collection : str
            It's the collection in which the user data is going to be inserted.
        query : dict, optional
            It's the query to make in order to insert the user data if there aren't
            any matches. The default value is None, no query.

        Raises
        ------
        UserDataNotFound
            If the provided user data is not a non-empty dict.
        CollectionNotFound
            If the provided collection is not a non-empty string.
        InvalidMongoDbObject
            If the MongoDB object does not contain the connection to the Mongo database.

        Returns
        -------
        A string with the id of the document inserted.
        None if the document has not been inserted.
        """
        # Check the provided user data
        if (type(user_data) != dict or len(user_data) == 0):
            raise UserDataNotFound("ERROR. The user data should be a non-empty dict.")
        # Check the provided collection
        if (collection == "" or type(collection) != str):
            raise CollectionNotFound("ERROR. The collection name should be a non-empty string.")
        # Check the provided query
        if (query != None):
            if (type(query) != dict or len(query) == 0):
                raise InvalidQuery("ERROR. The query should be a non-empty dict.")
        # Check the current MongoDB object
        if (type(self.mongodb) != mongodb.MongoDB):
                raise InvalidMongoDbObject("ERROR. The connection to the MongoDB database "+
                                       "should be a MongoDB object.")

        # Stores user data in the specified collection of a Mongo database.
        ## Add two keys: id (userid+social_media) and the date
        user_data['id'] = str(user_data['userid']) + "_" + user_data['social_media']
        user_data['date'] = (date.today()).strftime("%d-%m-%Y")
        # Set the collection to insert the user data
        self.mongodb.set_collection(collection)

        return self.mongodb.insert_item(user_data, query)

    def get_user_data(self, query, collection):
        """
        Gets user data from some collection of the Mongo database specifying a
        query in order to filter the records to return.

        Parameters
        ----------
        query : dict
            It's the dict which contains the keys and their values to filter the
            user data of the collection.
        collection : str
            It's the collection in which the query will be made to return the user
            data.

        Raises
        ------
        InvalidQuery
            If the provided query is not a non-empty dict.
        CollectionNotFound
            If the provided collection is not a non-empty string.
        InvalidMongoDbObject
            If the MongoDB object has not the connection to the Mongo database.

        Returns
        -------
        The returned user data if there are any.
        """
        # Check the provided query
        if (type(query) != dict or len(query) == 0):
            raise InvalidQuery("ERROR. The query should be a non-empty dict.")
        # Check the provided collection
        if (collection == "" or type(collection) != str):
            raise CollectionNotFound("ERROR. The collection name should be a non-empty string.")
        # Check the MongoDB object
        if (type(self.mongodb) != mongodb.MongoDB):
                raise InvalidMongoDbObject("ERROR. The connection to the MongoDB database "+
                                       "should be a MongoDB object.")
        # Set the collection
        self.mongodb.set_collection(collection)
        return self.mongodb.get_records(query)
        