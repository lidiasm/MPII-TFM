#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains the main operations which can be done on the web platform.

@author: Lidia Sánchez Mérida
"""
import os
import sys
sys.path.append('src/data')
from api import Api
import commondata
from mongodb import MongoDB
from exceptions import UsernameNotFound, MaxRequestsExceed

class MainOperations:
    
    def __init__(self):
        """Constructor. It has a MongoDB object to work with the database."""
        self.mongodb = MongoDB(os.environ.get("MONGODB_URI"), 'SocialNetworksDB', 'profiles')
    
    def get_user_instagram_data(self, search_user):
        """Downloads Instagram data of a specific user using the LevPasha Instagram
            API and stores the main fields in a MongoDB database."""
        if (search_user == None or type(search_user) != str or search_user == ""):
            raise UsernameNotFound("ERROR. Invalid username.")
            
        result = {'profile':None, 'posts':None, 'contacts': None}
        inst_api = Api()
        try:
            """Download Instagram user data"""
            user_instagram_data = inst_api.get_levpasha_instagram_data(search_user)
            """Preprocess data"""
            cd = commondata.CommonData(self.mongodb, user_instagram_data)
            prep_user_data = cd.preprocess_user_data()        
            """Store preprocessed user profile to MongoDB collection 'profiles'"""
            profile = cd.add_user_data(prep_user_data['profile']['username'],
               prep_user_data['profile'], 'profiles', 'Instagram')            
            
            """Store user posts, their likers and comments into the same MongoDB collection 'posts'"""
            all_posts = {}
            all_posts['posts'] = prep_user_data['posts']
            all_posts['likers'] = prep_user_data['likers']
            all_posts['comments'] = prep_user_data['comments']
            posts = cd.add_user_data(prep_user_data['profile']['username'],
                 all_posts, 'posts', 'Instagram')
            """Store the user followings and followers into the same MongoDB collection 'contacts'."""
            all_contacts = {}
            all_contacts['followings'] = prep_user_data['followings']
            all_contacts['followers'] = prep_user_data['followers']
            contacts = cd.add_user_data(prep_user_data['profile']['username'], 
                all_contacts, 'contacts', 'Instagram')
            
            """Returns the final user data"""
            result['profile'] = profile[1]
            result['contacts'] = contacts[1]
            result['posts'] = posts[1]
            
            return result
        
        except MaxRequestsExceed:
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
