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
    , MediaListNotFound, MediaDictNotFound, TextListNotFound, TextDictNotFound \
    , UserDataNotFound, CollectionNotFound, InvalidQuery, InvalidSocialMediaSource \
    , UsernameNotFound, InvalidMediaId, InvalidQueryValues, InvalidUserId
from datetime import date, datetime
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
            - The list of the required keys for the media texts.
            - The list of avalaible social media sources.
            - The list of stopwords to remove from text.
            - The relationship between the user data and the collection to save them.

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
        self.profile_keys = ['biography', 'birthday', 'date_joined', 'gender', 
                          'location', 'n_followers', 'n_followings', 'n_medias', 
                          'name', 'profile_pic', 'userid', 'username']
        self.media_keys = ['comment_count','id_media', 'like_count', 'taken_at', 'title', 'url']
        self.text_keys = ['id_media', 'texts']
        self.text_list_keys = ['text', 'user',]
        self.social_media_sources = ["instagram"]
        self.stopwords = ['a', 'an', 'the', 'and', 'or', 'i', 'you', 'he', 'she',
                          'it', 'we', 'they', 'my', 'your', 'his', 'her', 'its',
                          'ours', 'yours', 'them', 'me', 'us']
        self.related_collections = {
            "profiles":"insert_profile",
            "medias":"insert_medias",
            "comments":"insert_comments",
            "test":"insert_test",
            "test_medias":"insert_test",
            "test_comments":"insert_test"}

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
        InvalidUserId
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
        user_profile['date'] = datetime.strptime((date.today()).strftime("%d-%m-%Y"),'%d-%m-%Y')
        return user_profile
    
    def preprocess_medias(self, medias, social_media, username):
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
        username : str
            It's the username of the studied user account.

        Raises
        ------
        MediaListNotFound
            If the provided medias are not in a list.
        MediaDictNotFound
            If the provided medias are not dicts.
        InvalidSocialMediaSource
            If the provided social media source is not a non-empty string or it's
            not one of the avalaible social media sources.
        UsernameNotFound
            If the provided username is not a non-empty string.

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
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")

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
        preprocessed_medias["social_media"] = social_media
        preprocessed_medias['date'] = datetime.strptime((date.today()).strftime("%d-%m-%Y"),'%d-%m-%Y')
        preprocessed_medias["username"] = username
        return preprocessed_medias

    def preprocess_media_comments(self, comments, social_media, username):
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
        username : str
            It's the username of the studied user account.

        Raises
        ------
        TextListNotFound
            If the texts from the medias are not in a list.
        TextDictNotFound
            If the media data is not in a dict.
        InvalidSocialMediaSource
            If the provided social media source is not a non-empty string or it's
            not one of the avalaible social media sources.
        UsernameNotFound
            If the provided username is not a positive integer.

        Returns
        -------
        A dict with the media texts as well as the social media source.
        """
        # Check if the comments are in a list
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
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")

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
        preprocessed_texts['date'] = datetime.strptime((date.today()).strftime("%d-%m-%Y"),'%d-%m-%Y')
        preprocessed_texts['username'] = username

        return preprocessed_texts

    def preprocess_user_data(self, user_data, social_media):
        """
        Preprocesses the social media user data such as the profile, medias as
        well as their comments.

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
        username = profile['username']
        medias = self.preprocess_medias(user_data['medias'], social_media, username)
        comments = self.preprocess_media_comments(user_data['comments'], social_media, username)
        data = {'profile':profile, 'media_list':medias, 'media_comments':comments}
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
            import time 
            start = time.time()
            # try:
            #     # Translate to English
            #     english_text = (translator.translate(text, dest="en")).text
            # except: #pragma no cover
            #     english_text = text
            end = time.time()
            #print("Translate: ",end - start)
            # Remove specific stopwords
            english_text = text
            start = time.time()
            english_words = english_text.split()
            non_stopwords = [word for word in english_words if word.lower() not in self.stopwords]
            non_stopwords = ' '.join(non_stopwords)
            end = time.time()
            # print("Stopwords" ,end - start)
            # Remove numbers
            start = time.time()
            non_numbers = re.sub(r"\d+", "", non_stopwords)
            end = time.time()
            # print("Non numbers",end - start)
            # Remove some special characters
            start = time.time()
            non_special_characters = re.sub(r'[#@\"\-"*$%&\+\_]', ' ', non_numbers)
            end = time.time()
            # print("Special chracters", end - start)
            # Add the cleaned text to the list of cleaned texts
            cleaned_texts.append(non_special_characters)

        return cleaned_texts

    def insert_user_data(self, user_data, collection):
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
        # Check if the collection exists
        if (collection not in self.related_collections):
            raise CollectionNotFound("ERROR. The provided collection does not exist.")
         # Check the current MongoDB object
        if (type(self.mongodb) != mongodb.MongoDB):
                raise InvalidMongoDbObject("ERROR. The connection to the MongoDB database "+
                                       "should be a MongoDB object.")
        
        # Set the collection to insert the user data
        self.mongodb.set_collection(collection)
        # Stores user data in the specified collection of a Mongo database.
        return self.mongodb.insert_item(user_data)

    def get_user_data(self, collection, query, values={}):
        """
        Gets the matched records from a specific collection and related to a
        specific query.

        Parameters
        ----------
        collection : str
            It's the collection in which the query will be made and the data will
            be recovered.
        query : str
            It's the query to make in order to get the matched records.
        values : dict, optional
            They're the parameters to add to the query in order to filter the
            data to recover. The default is {}.

        Raises
        ------
        CollectionNotFound
            If the provided collection is not a non-empty string.
        InvalidQuery
            If the provided query is not a non-empty string or does not exist.
        InvalidQueryValues
            If the provided values are not in a dict.
        InvalidMongoDbObject
            If the MongoDB object does not contain the connection to the Mongo database.

        Returns
        -------
        A dict which contains the matched records as dicts too.
        """
        # Check the MongoDB object
        if (type(self.mongodb) != mongodb.MongoDB):
            raise InvalidMongoDbObject("ERROR. The connection to the MongoDB database "+
                                   "should be a MongoDB object.")
        # Check the provided collection
        if (collection == "" or type(collection) != str):
            raise CollectionNotFound("ERROR. The collection name should be a non-empty string.")
        # Check if the provided collection exists
        if (collection not in self.related_collections):
            raise CollectionNotFound("ERROR. The provided collection does not exist.")
        # Check the provided query
        if (type(query) != str or query == ""):
            raise InvalidQuery("ERROR. The query should be a non-empty dict.")
        # Check if the provided query exists
        if (query not in self.mongodb.get_queries):
            raise InvalidQuery("ERROR. The provided query does not exist.")
        # Check the values
        if (type(values) != dict):
            raise InvalidQueryValues("ERROR. The values should be a dict.")
        
        # Set the collection
        self.mongodb.set_collection(collection)
        return self.mongodb.get_records(query, values)
