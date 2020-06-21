#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains the common data to social networks and the preprocessing
methods to verify the values of the collected data.

@author: Lidia Sánchez Mérida
"""
import sys
sys.path.append("../")
from exceptions import ProfileDictNotFound, UsernameNotFound, ContactsListsNotFound \
, LikersListNotFound, IdNotFound, PostsDictNotFound, CommentsDictNotFound, UserDataNotFound, CollectionNotFound

from datetime import date

class CommonData:
    
    def __init__(self, mongodb, user_data={}):
        """Constructor. You can create an instance from this class using two different ways.
            1) Only passing the database object to connect to it and sending queries.
            2) Also passing the user data to preprocess and insert them to the database."""
        self.mongodb = mongodb
        self.user_data = user_data
    
    def preprocess_profile(self):
        """Check the values of the profile and the fields on it. If there isn't some
            mandatory field, it'll be added with default value."""
        if ('profile' in self.user_data): 
            user_profile = self.user_data['profile']
            """Check the type."""
            if (type(user_profile) != dict or user_profile == None):
                raise ProfileDictNotFound("ERROR. User profile should be a dict.")
            """Username has to exist because it identifiers the user."""
            if ('username' not in user_profile):
                raise UsernameNotFound("Username not provided.")
            elif (user_profile['username'] == None or user_profile['username'] == ""):
                raise UsernameNotFound("Username not provided.")
            
            """Mandatory fields"""
            required_fields = ['userid', 'username', 'name', 'biography', 'gender', 'profile_pic',
              'location', 'birthday', 'data_joined', 'n_followers', 'n_followings']
            """Copy of the user profile to remove not required fields."""
            preprocessed_user_profile = {}
            for field in user_profile:
                if field in required_fields:
                    preprocessed_user_profile[field] = user_profile[field]
                    if user_profile[field] == None: 
                        preprocessed_user_profile[field] = 'None'
            return preprocessed_user_profile
        else:
            raise ProfileDictNotFound("ERROR. User profile not provided.")
    
    def preprocess_contacts(self):
        """Checks the followers/followings of an user. If there aren't, both lists
            will be initialized as empty lists."""
        user_followers = []
        user_followings = []
        if ('followers' in self.user_data): user_followers = self.user_data['followers']
        if ('followings' in self.user_data): user_followings = self.user_data['followings']
        """Check types."""
        if (type(user_followers) != list or user_followers == None or 
            type(user_followings) != list or user_followings == None):
            raise ContactsListsNotFound('ERROR. Followings and followers should be lists.')
        
        """Removes 'None' followings/followers."""
        validFollowers = [follower for follower in user_followers if follower is not None]
        validFollowings = [following for following in user_followings if following is not None]
        
        return {'followers':validFollowers, 'followings':validFollowings}
    
    def preprocess_posts(self):
        """Checks the user posts provdided."""
        posts = {}
        if ('posts' in self.user_data):
            posts = self.user_data['posts']
            """Check type"""
            if (type(posts) != dict or posts == None):
                raise PostsDictNotFound("ERROR. Posts should be a dict.")
            """Check likers and comments fields. They should be integers."""
            for id_post in posts:
                if (id_post == None or id_post == "" or type(id_post) != str):
                    raise IdNotFound("ERROR. Invalid id post.")
                try:
                    int(posts[id_post]['likes'])
                    int(posts[id_post]['comments'])
                    posts[id_post]['likes'] = str(posts[id_post]['likes'])
                    posts[id_post]['comments'] = str(posts[id_post]['comments'])
                except ValueError:
                    raise ValueError("ERROR. Likers and comments should be numbers.")
        return posts
    
    def preprocess_likers(self):
        """Checks if there are some posts. If there are, then it checks the people
            who like them."""
        if ('posts' in self.user_data):
            likers = []
            if ('likers' in self.user_data):
                likers = self.user_data['likers']
            """Check type."""
            if (type(likers) != list or likers == None):
                raise LikersListNotFound("ERROR. Likers should be a list.")
            
            return likers
        else:
            raise PostsDictNotFound("There aren't any posts so likers can't be analyzed.")
            
    def preprocess_comments(self):
        """Checks if there are some posts. If there are, then it checks the comments
            on them."""
        if ('posts' in self.user_data):
            comments = {}
            if ('comments' in self.user_data):
                comments = self.user_data['comments']
            """Check type."""
            if (type(comments) != dict or comments == None):
                raise CommentsDictNotFound("ERROR. Post comments should be a list.")
            
            return comments
        else:
            raise PostsDictNotFound("There aren't any posts so their comments can't be analyzed.")
    
    def preprocess_user_data(self):
        """Checks all user data."""
        profile = self.preprocess_profile()
        data = {'profile':profile}
        contacts = self.preprocess_contacts()
        posts = self.preprocess_posts()
        likers = self.preprocess_likers()
        comments = self.preprocess_comments()
        data = {'profile':profile, 'posts':posts, 'likers':likers, 'comments':comments,
                'followers':contacts['followers'], 'followings':contacts['followings']}
        return data
    
    def add_user_data(self, username, user_data, collection):
        if (username == None or type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. Invalid username.")
        if (user_data == None or len(user_data) == 0 or type(user_data) != dict):
            raise UserDataNotFound("ERROR. There aren't any user data to store.")
        if (collection == None or collection == "" or type(collection) != str):
            raise CollectionNotFound("ERROR. Invalid collection name.")
            
        """Stores user data in the specified collection of a Mongo database."""
        # Primary keys: (user id, date)
        user_data['id'] = username
        user_data['date'] = str(date.today())
        # Update the collection
        self.mongodb.set_collection(collection)
        
        return [self.mongodb.insert(user_data), user_data]
    
    def get_user_data(self, username):
        """Gets all rows related to a username from a collection."""
        if (username == None or type(username) != str or username == ""):
            raise UsernameNotFound("You should specify a valid username.")
        
        userData = self.mongodb.get_item_records('id', username)
        if (userData == None or len(userData) == 0):
            raise IdNotFound("The specified username doesn't exist in the database.")
            
        return userData