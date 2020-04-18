#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains the main operations which can be done on the web platform.

@author: Lidia Sánchez Mérida
"""
import os
import sys
sys.path.append('src/data')
import api
import commondata
from mongodb import MongoDB
from exceptions import UsernameNotFound, MaxRequestsExceed

class MainOperations:
    
    def __init__(self):
        """Constructor. It has a mongodb object to work with the database."""
        self.mongodb = MongoDB(os.environ.get("MONGODB_URI"), 'SocialNetworksDB', 'profiles')
    
    def get_user_instagram_data(self, search_user):
        if (search_user == None or type(search_user) != str or search_user == ""):
            raise UsernameNotFound("ERROR. Invalid username.")
            
        """Gets, preprocesses and stores in Mongo database an user's Instagram data."""
        result = {'profile':None, 'posts':None, 'contacts': None}
        inst_api = api.Api()
        try:
            user_instagram_data = inst_api.get_instagram_data(search_user)
            # Preprocess data
            cd = commondata.CommonData(self.mongodb, user_instagram_data)
            prep_user_data = cd.preprocess_user_data()
            id1_db = cd.add_user_data(prep_user_data['profile']['username'], prep_user_data['profile'], 'profiles')
            """Put posts, their likers and comments together."""
            all_posts = {}
            all_posts['posts'] = prep_user_data['posts']
            all_posts['likers'] = prep_user_data['likers']
            all_posts['comments'] = prep_user_data['comments']
            id2_db = cd.add_user_data(prep_user_data['profile']['username'], all_posts, 'posts')
            """Put followings and followers together."""
            all_contacts = {}
            all_contacts['followings'] = prep_user_data['followings']
            all_contacts['followers'] = prep_user_data['followers']
            id3_db = cd.add_user_data(prep_user_data['profile']['username'], all_contacts, 'contacts')
            
            """Updates the results"""
            result['profile'] = id1_db
            result['contacts'] = id2_db
            result['posts'] = id3_db
            
            return result
        
        except MaxRequestsExceed:
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
        