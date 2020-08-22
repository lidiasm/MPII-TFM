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
from exceptions import InvalidMongoDbObject, ProfileDictNotFound, UsernameNotFound \
    , ContactDictNotFound, MediaListNotFound, MediaDictNotFound, LikerListNotFound \
    , TextListNotFound, TextDictNotFound, UserDataNotFound, CollectionNotFound \
    , InvalidQuery, InvalidSocialMediaSource, InvalidUserId
from datetime import date
from googletrans import Translator
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import emoji

class CommonData:

    def __init__(self, mongodb=None):
        """
        Creates a CommonData object whose attributes are:
            - A MongoDB object to operate with the Mongo database. It could be
                None if the MongoDB operations are not required.
            - The lists of avalaible fields for the user profile.
            - The list of avalaible social media sources.

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
          'location', 'birthday', 'date_joined', 'n_followers', 'n_followings', 'n_medias', 
          'date', 'id', 'social_media']
        self.social_media_sources = ["instagram"]
    
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
        # Check the data type
        if (type(user_profile) != dict or user_profile == None):
            raise ProfileDictNotFound("ERROR. User profile should be a dict.")
        # IMPORTANT!
        ## Username has to exist because it identifiers the user.
        if ('username' not in user_profile):
            raise UsernameNotFound("ERROR. The field 'username' is required.")
        elif (type(user_profile['username']) != str or user_profile['username'] == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")
        # Check the provided social media source
        if (type(social_media) != str or social_media == ""):
            raise InvalidSocialMediaSource("ERROR. The social media source should be a non-empty string.")
        if (social_media.lower() not in self.social_media_sources):
            raise InvalidSocialMediaSource("ERROR. Avalaible social media sources: "+str(self.social_media_sources))
            
        # Copy of the user profile to remove non-required fields.
        preprocessed_user_profile = {}
        for field in user_profile:
            if field in self.profile_keys:
                preprocessed_user_profile[field] = user_profile[field]
                if user_profile[field] == None:
                    # Add None value as a string
                    preprocessed_user_profile[field] = 'None'
        
        # Add the social media source
        preprocessed_user_profile['social_media'] = social_media
        return preprocessed_user_profile

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
        userid : int
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
        if (type(userid) != int or userid < 0):
            raise InvalidUserId("ERROR. The user id should be a positive integer.")
        
        # Followers and followings only can contain non-empty strings (usernames).
        validFollowers = [follower for follower in contacts['followers'] if type(follower) == str and follower != ""]
        validFollowings = [following for following in contacts['followings'] if type(following) == str and following != ""]

        return {'followers':validFollowers, 'followings':validFollowings, 
                    'social_media':social_media, 'userid':userid}

    def preprocess_medias(self, medias, social_media, userid):
        """
        Preprocesses the list of medias of a specific user. Each media is a dict
        whose keys are: id_media, title, like_count and comment_count in order
        to get their id, title and the number of likes and comments.

        Parameters
        ----------
        posts : list of dicts.
            It's the list of medias of a specific user.
        social_media : str
            It's the social media which the user data came from.
        userid : int
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
            If the provided user id is not a positive integer.

        Returns
        -------
        A dict which contains the list of media data as well as the social media source.
        """
        # Check the provided medias
        if (type(medias) != list):
            raise MediaListNotFound("ERROR. The medias of an user should be in a list of dicts.")
        # Check the provided social media source
        if (type(social_media) != str or social_media == ""):
            raise InvalidSocialMediaSource("ERROR. The social media source should be a non-empty string.")
        if (social_media.lower() not in self.social_media_sources):
            raise InvalidSocialMediaSource("ERROR. Avalaible social media sources: "+str(self.social_media_sources))
        # Check the provided user id
        if (type(userid) != int or userid < 0):
            raise InvalidUserId("ERROR. The user id should be a positive integer.")
        
        # Preprocessing
        preprocessed_medias = {}
        media_list = []
        for media in medias:
            # Check the type of each media
            if (type(media) != dict or len(media) == 0):
                raise MediaDictNotFound("ERROR. Each media should be a non-empty dict.")
            # Check the keys and their values
            if ('id_media' not in media or 'title' not in media or
                'like_count' not in media or 'comment_count' not in media):
                raise MediaDictNotFound("ERROR. Each media should have its id,"
                           +" title as well as the number of likes and comments.")
            # Check the type of the values
            if (type(media['id_media']) != str or media['id_media'] == "" or
                type(media['like_count']) != int or media['like_count'] < 0 or
                type(media['comment_count']) != int or media['like_count'] < 0):
                raise MediaDictNotFound("ERROR. The media id should be a non-empty string,"
                           +" as well as the like and comment count should be positive integers.")
            
            # Check the title which could be None
            title = media['title'] if media['title'] != None else 'None'
            # Copy the keys and their values in a dict
            media_list.append({'id_media':media['id_media'],
                               'title':title,
                               'like_count':media['like_count'],
                               'comment_count':media['comment_count']})
        
        # Preprocessed medias dict
        preprocessed_medias['medias'] = media_list
        preprocessed_medias['social_media'] = social_media
        preprocessed_medias['userid'] = userid
            
        return preprocessed_medias

    def preprocess_media_likers(self, likers, social_media, userid):
        """
        Preprocesses the list of people who liked the medias of a specific user.

        Parameters
        ----------
        likers : list of str
            It's the list of the usernames who liked the posts of a specific user.
        social_media : str
            It's the social media which the user data came from.
        userid : int
            It's the id of the studied user account.

        Raises
        ------
        LikerListNotFound
            If the provided likers are not in a list of strings.
        InvalidSocialMediaSource
            If the provided social media source is not a non-empty string or it's
            not one of the avalaible social media sources.
        InvalidUserId
            If the provided user id is not a positive integer.

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
        if (type(userid) != int or userid < 0):
            raise InvalidUserId("ERROR. The user id should be a positive integer.")
        
        preprocessed_likers = {}
        liker_list = []
        for record in likers:
            # Check the keys
            if ('id_media' not in record or 'users' not in record):
                raise LikerListNotFound("ERROR. Likers should have 'id_media' and 'users' keys.")
            # Check the type of the values
            if (type(record['id_media']) != str or record['id_media'] == "" or type(record['users']) != list):
                raise LikerListNotFound("ERROR. The 'id_media' should be a" 
                    +" non-empty string and the 'users' should be a list.")
            # Check the usernames of the likers
            for user in record['users']:
                if (type(user) != str or user == ""):
                    raise LikerListNotFound("ERROR. The usernames should be non-empty strings.")
            
            liker_list.append({'id_media':record['id_media'],
                               'users':record['users']})
            
        # Preprocessed likers
        preprocessed_likers['likers'] = liker_list
        preprocessed_likers['social_media'] = social_media
        preprocessed_likers['userid'] = userid
        
        return preprocessed_likers

    def preprocess_media_texts(self, text_list, social_media, userid):
        """
        Preprocesses the texts from the medias of a specific user, like comments.

        Parameters
        ----------
        text_list : list of dicts
            It's the list of texts for each media whose fields contains the user
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
        # Check the data type
        if (type(text_list) != list or len(text_list) == 0):
            raise TextListNotFound("ERROR. The texts from medias should be in a non-empty list.")
        # Check the provided social media source
        if (type(social_media) != str or social_media == ""):
            raise InvalidSocialMediaSource("ERROR. The social media source should be a non-empty string.")
        if (social_media.lower() not in self.social_media_sources):
            raise InvalidSocialMediaSource("ERROR. Avalaible social media sources: "+str(self.social_media_sources))
        # Check the provided user id
        if (type(userid) != int or userid < 0):
            raise InvalidUserId("ERROR. The user id should be a positive integer.")
        
        # Check the texts from each media
        preprocessed_texts = {}
        media_texts = []
        for media in text_list:
            # Check the keys of the dict
            if ('id_media' not in media or 'texts' not in media):
                raise TextDictNotFound("ERROR. Each media should have a 'id_media' and 'texts' keys.")
            # Check the type of each key
            if (type(media['id_media']) != str or media['id_media'] == "" or type(media['texts']) != list):
                raise TextDictNotFound("ERROR. Each media should have a"+ 
                       " non-empty id_media and a list of text.")
            
            # Check the list of texts for each media
            for record in media['texts']:
                if ('user' not in record or 'text' not in record):
                    raise TextDictNotFound("ERROR. Each record should have 'user' and 'text' keys.")
                # Check the type of the values 
                if (type(record['user']) != str or record['user'] == "" or
                    type(record['text']) != str or record['text'] == ""):
                    raise TextDictNotFound("ERROR. The user and the text should be non-empty strings.")
        
            media_texts.append({'id_media':media['id_media'],
                                'texts':media['texts']})
        
        # Preprocessed media texts
        preprocessed_texts['text_list'] = media_texts
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
        texts = self.preprocess_media_texts(user_data['texts'], social_media, userid)
        data = {'profile':profile, 'media_list':medias, 'media_likers':likers, 
                'media_texts':texts, 'contacts':contacts}
        return data

    def transform_text(self, text_list, social_media, userid):
        """
        Preprocesses a list of texts from the medias of some user account in order
        to analyze the text. The next operations will be applied:
            - Translate the text to English language.
            - Transform each letter to lower-case.
            - Transform emojis to text.
            - Remove punctuation marks, stop words, numbers and non-sense words.

        Parameters
        ----------
        text_list : list of dicts
            It's the list of texts for each media whose fields contains the user
            who wrote the text and the text itself.
        social_media : str
            It's the social media which the user data came from.
        userid : int
            It's the id of the studied user account.
            
        Returns
        -------
        A list of dicts with the transformed and cleaned texts.
        """
        # Check the list of text
        preprocessed_texts = self.preprocess_media_texts(text_list, social_media, userid)
        
        ############# TEXT COMMENTS PREPROCESSING ###############
        ## Google Translator object.
        translator = Translator()
        ## Pattern to get the stop words in English
        pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
        transformed_texts = []
        
        for media in preprocessed_texts['text_list']:
            for record in media['texts']:
                # Translate to English
                p_com = (translator.translate(record['text'], dest="en")).text
                # Lower-case
                p_com = p_com.lower()
                # Emojis to text
                p_com = emoji.demojize(p_com)
                p_com = p_com.replace(":"," ")
                p_com = ' '.join(p_com.split())
                # Remove numbers
                p_com = re.sub(r"\d+", "", p_com)
                # Remove stop words in English
                p_com = pattern.sub('', p_com)
                # Remove punctuation marks
                p_com = re.sub(r'[¡#@¿\'\"\[!#?\],.:\_\-";*]', ' ', p_com)
                # Remove non-sense words, like loose letters
                p_com = ' '.join( [w for w in p_com.split() if len(w)>1] )
                # Store the preprocessed comment text
                transformed_texts.append({'user':record['user'], 'transformed_text':p_com})
        
        return transformed_texts

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
        