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
from mongodb import MongoDB
from exceptions import UsernameNotFound, MaxRequestsExceed, UserDataNotFound \
    , InvalidSocialMediaSource

class MainOperations:

    def __init__(self):
        """Constructor. It has a MongoDB object to work with the database."""
        self.mongodb = MongoDB(os.environ.get("MONGODB_URI"), 'SocialNetworksDB', 'profiles')

    def get_user_instagram_common_data(self, search_user):
        """Downloads Instagram data of a specific user using the LevPasha Instagram
            API and stores the main fields in a MongoDB database."""
        if (search_user == None or type(search_user) != str or search_user == ""):
            raise UsernameNotFound("ERROR. Invalid username.")

        inst_api = Api()
        try:
            """Download Instagram user data"""
            user_instagram_data = inst_api.get_levpasha_instagram_data(search_user)
            return user_instagram_data
            """Preprocess and store user data"""
            user_data = self.preprocess_and_store_common_data(user_instagram_data, 'Instagram')
            return user_data
        except MaxRequestsExceed:   # pragma: no cover
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")

    def preprocess_and_store_common_data(self, user_data, social_media):
        """Preprocess and store user data from any API source into the MongoDB database."""
        if (type(user_data) != dict or len(user_data) == 0):
            raise UserDataNotFound("ERROR. User data should be a non empty dict.")
        if (type(social_media) != str or social_media == ""):
            raise InvalidSocialMediaSource("ERROR. Social media type should be a non empty string.")

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
