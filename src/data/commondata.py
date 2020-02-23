#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains the common data to social networks and the preprocessing
methods to verify the values of the collected data.

@author: Lidia Sánchez Mérida
"""
import sys
sys.path.append("../")
from exceptions import ProfileNotFound, BasicProfileDataNotFound, RelathionshipsListNotFound, LikersListNotFound, IdNotFound, PostsDictNotFound, UsernameNotFound
from datetime import date

class CommonData:
    
    def __init__(self, mongodb, profileUser={}, posts={}, likers=[], followers=[], followings=[]):
        """Constructor. You can create an instance from this class using two different ways.
            1) Only passing the database object to connect to it and sending queries.
            2) Also passing the user data to preprocess and insert them to the database."""
        self.profileUser = profileUser
        self.posts = posts
        self.likers = likers
        self.followers = followers
        self.followings = followings
        self.mongodb = mongodb
    
    def check_profile_field(self, field):
        """Checks if a field exists and has a value."""
        field_value = None
        if (field in self.profileUser):
            if (field == None): self.profileUser[field] = "None"
            else: field_value = self.profileUser[field]
        else:
            self.profileUser[field] = "None"
            
        return field_value
            
    def profile_preprocessing(self):
        """Check if the user profile exists."""
        if (self.profileUser == None or len(self.profileUser) == 0): 
            raise ProfileNotFound("User profile not provided")
        """Checks the structure of a provided profile and their values of its
            fields."""
        username_value = self.check_profile_field('username')
        self.check_profile_field('name')
        self.check_profile_field('email')
        self.check_profile_field('biography')
        self.check_profile_field('gender')
        self.check_profile_field('profile_pic')
        self.check_profile_field('location')
        self.check_profile_field('birthday')
        self.check_profile_field('date_joined')
        self.check_profile_field('private_account')
        self.check_profile_field('n_followers')
        self.check_profile_field('n_followings')
        """To string."""
        if (self.profileUser['private_account'] == True): self.profileUser['private_account'] = 'Yes'
        elif (self.profileUser['private_account'] == False): self.profileUser['private_account'] = 'No'
        
        if (username_value == None):
            raise BasicProfileDataNotFound("Basic profile data not found.")
                    
        return self.profileUser
    
    def relationships_preprocessing(self):
        """Checks if the followers/followings list exist. If they're not, they'll be
            initialized as empty lists."""
        if (self.followers == None): self.followers = []
        if (self.followings == None): self.followings = []
        """Checks the types."""
        if (type(self.followers) != list and self.followers != None):
            raise RelathionshipsListNotFound("Followers should be a list.")
        if (type(self.followings) != list and self.followings != None):
            raise RelathionshipsListNotFound("Followings should be a list.")
        """Removes None followings/followers."""
        validFollowers = [follower for follower in self.followers if follower is not None]
        validFollowings = [following for following in self.followings if following is not None]
        """Update followers/followings."""
        self.followers = validFollowers
        self.followings = validFollowings
        return True
    
    def likers_preprocessing(self):
        """Checks if there are some posts. If there aren't, likers can't exist."""
        if (len(self.posts) == 0):
            raise PostsDictNotFound("Posts should be a dict.")
        """Checks if the dict of likers exists."""
        if (self.likers == None): self.likers = {}
        """Checks the list of people who like the posts of the user."""
        if (type(self.likers) != list and self.likers != None):
            raise LikersListNotFound("Likers should be a list.")
        return True
    
    def posts_preprocessing(self):
        """Checks if the dict of posts exists."""
        if (self.posts == None): self.posts = {}
        """Checks the list of posts of the user."""
        if (type(self.posts) != dict and self.posts != None):
            raise PostsDictNotFound("Posts should be a dict.")
        """Preprocessing the value of the fields of the posts dict"""
        for post in self.posts:
            if (post == None): raise IdNotFound("Error. A post doesn't have an id.")
            if (self.posts[post]['likes'] == None): self.posts[post]['likes'] = str(0)
            if (self.posts[post]['comments'] == None): self.posts[post]['comments'] = str(0)
        """Check complete"""
        return True
    
    def preprocessing(self):
        """Checks user data."""
        self.profile_preprocessing()
        self.relationships_preprocessing()
        self.likers_preprocessing()
        self.posts_preprocessing()
        data = {'profile':self.profileUser, 'posts':self.posts, 'likers':self.likers,
                'followers':self.followers, 'followings':self.followings}
        return data
    
    def add_user_data(self):
        """Preprocesses the provided user data."""
        userData = self.preprocessing()
        """Id = username, date = today date. These will be the two fields which insert
            method will have into account in order to insert a new element."""
        userData['id'] = userData['profile']['username']
        userData['date'] = str(date.today())
        return self.mongodb.insert(userData)
    
    def get_user_data(self, username):
        """Gets all rows related to a username from a collection."""
        if (username == None or type(username) != str or username == ""):
            raise UsernameNotFound("You should specify a valid username.")
        
        userData = self.mongodb.get_item_records('id', username)
        if (userData == None or len(userData) == 0):
            raise IdNotFound("The specified username doesn't exist in the database.")
        return userData