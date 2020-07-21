#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class in which there are many APIs to connect to in order to download and get
interesting data related to an user social media account. Then, this information
will be stored in the database.

@author: Lidia Sánchez Mérida
"""

import os
from os import path
import sys
sys.path.append("../")
from exceptions import InvalidCredentials, UsernameNotFound, MaxRequestsExceed \
    , InvalidUserId, InvalidLimit, PostsListNotFound, PostDictNotFound
from InstagramAPI import InstagramAPI
import time 
import pickle

class Api:
    
    def __init__(self):
        """Creates a new API object which contains the connection stablished to
            an API."""
        self.connection = None
        
    def connect_levpasha_instagram_api(self, use_session_file=True, session_file="./levpasha_session.txt"):
        """Connects to LevPasha Instagram API using:
            - A file in which there is the connection object stored.
            - The credentials of your Instagram account. For safety reasons 
                there should be as env variables in the sistem."""
        if (path.exists(session_file) and use_session_file):
            self.connection = pickle.load(open(session_file, "rb"))
        else:
            username = os.environ.get("INSTAGRAM_USER2")
            pswd = os.environ.get("INSTAGRAM_PSWD2")
            if (type(username) != str or type(pswd) != str or username == None or
                pswd == None or username == "" or pswd == ""):
                raise InvalidCredentials("Username and/or password are not right.")
            
            self.connection = InstagramAPI(username, pswd)
            self.connection.login()
            if (self.connection.LastJson['status'] != 'ok'):
                raise InvalidCredentials("Invalid Instagram credentials.")
            
            if (type(session_file) != str or session_file == ""):
                session_file = "./levpasha_session.txt"
                
            pickle.dump(self.connection, open(session_file, "wb"))
        
        return self.connection
    
    def get_levpasha_instagram_profile(self, search_user):
        """Downloads the profile of a specific user from LevPasha Instagram 
            API and returns a dict with the interesting data of the user profile."""
        if (type(search_user) != str or search_user == ""):
            raise UsernameNotFound("ERROR. The username should be a non empty string.")
        
        # Gets the profile of the user
        self.connection.searchUsername(search_user)
        # Exception when the max number of requests has been exceeded
        if (self.connection.LastJson['status'].lower() != 'ok'):    # pragma: no cover
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
            
        # Profile with the interesting fields
        profile = {}
        profile['userid'] = self.connection.LastJson['user']['pk']
        profile['name'] = self.connection.LastJson['user']['full_name']
        profile['username'] = self.connection.LastJson['user']['username']
        profile['biography'] = self.connection.LastJson['user']['biography']
        profile['gender'] = None
        profile['profile_pic'] = self.connection.LastJson['user']['profile_pic_url']
        profile['location'] = None
        profile['birthday'] = None
        profile['date_joined'] = None
        profile['n_followers'] = self.connection.LastJson['user']['follower_count']
        profile['n_following'] = self.connection.LastJson['user']['following_count']
        profile['n_medias'] = self.connection.LastJson['user']['media_count']
        
        return profile
    
    def get_levpasha_instagram_posts(self, user_id, limit=100):
        """Gets some posts of an user providing their user id, which can be
            found in their profile. The number of posts downloaded can be specified."""
        # Check the user id
        if (type(user_id) != int or user_id < 0):
            raise InvalidUserId("ERROR. The user id should be a positive number.")
        # Check the limit
        if (type(limit) != int or limit <= 0):
            raise InvalidLimit("ERROR. The post limit should be a number greater than 0.")
        
        posts = []
        more_posts = True
        max_id = ""
        n_downloaded_posts = 0
        # Gets posts while there are still more posts
        while more_posts:
            self.connection.getUserFeed(user_id, max_id)
            if (self.connection.LastJson['more_available'] == False):
                more_posts = False
                
            """Save the media id, its number of likes and comments."""
            max_id = self.connection.LastJson.get('next_max_id', '')
            items_list = self.connection.LastJson['items']
            for i in items_list:
                posts.append({'id_post':i['id'], 'likes':i['like_count'], 'comments':i['comment_count']})
            
            n_downloaded_posts += len(items_list)
            if (n_downloaded_posts >= limit): break
            """Wait some time to avoid flooding the servers."""
            time.sleep(20)
            
        return posts
    
    def get_levpasha_instagram_posts_likers(self, username, posts):
        """Downloads the username of the Instagram accounts who liked the
            user posts."""
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non empty string.")
        if (type(posts) != list or len(posts) == 0):
            raise PostsListNotFound("ERROR. There aren't any posts to get their likers.")
        
        """Iterate over each post and each user who liked it."""
        all_likers = []
        for post in posts:
            # Check each post
            if (type(post) != dict or len(post) == 0):
                raise PostDictNotFound("ERROR. Each post should be a non empty dict.")
            if ('id_post' not in post):
                raise PostDictNotFound("ERROR. Each post should have its id.")
                
            self.connection.getMediaLikers(post['id_post'])
            # Prevent max requests exception
            if (self.connection.LastJson['status'].lower() != 'ok'):    # pragma: no cover
                raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
            
            if ('users' in self.connection.LastJson):
                users = self.connection.LastJson['users']
                # Get the usernames of the people who liked the current post
                for user in users:
                    if (user['username'] != username):
                        all_likers.append(user['username'])
                    
            """Wait some time to avoid flooding the servers."""
            time.sleep(20)
        
        """Count number of likes for each user and sort them in order to show the fans first."""
        count_likes = {user:all_likers.count(user) for user in all_likers}
        
        return sorted(count_likes.items(), key=lambda k:k[1], reverse=True) 
     
    def get_levpasha_instagram_posts_comments(self, username, posts):
        """Gets the comments made by Instagram users to the posts of a specific user."""
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non empty string.")
        if (type(posts) != list or len(posts) == 0):
            raise PostsListNotFound("ERROR. There aren't any posts to get their likers.")
        
        comments = []
        for post in posts:
            # Check each post
            if (type(post) != dict or len(post) == 0):
                raise PostDictNotFound("ERROR. Each post should be a non empty dict.")
            if ('id_post' not in post):
                raise PostDictNotFound("ERROR. Each post should have its id.")
                
            # MAX 20 COMMENTS PER POST
            self.connection.getMediaComments(post['id_post'])
            if (self.connection.LastJson['status'].lower() != 'ok'):    # pragma: no cover
                raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
            # Save the user who wrote the comment and the text
            if ('comments' in self.connection.LastJson):
                post_comments = self.connection.LastJson['comments']
                comments_list = []
                for comm in post_comments:
                    if (comm['user']['username'] != username):
                        comments_list.append({'user':comm['user']['username'], 'comment':comm['text']})
                
                """Add the comments of the post"""
                comments.append({'id_post':post['id_post'], 'comments':comments_list})
            
            """Wait some time to avoid flooding the servers."""
            time.sleep(20)
        
        return comments
    
    def get_levpasha_instagram_contacts(self, user_id):
        """Downloads the usernames of the followers and followings of a 
            specific user using their user id."""
        # Check the user id
        if (type(user_id) != int or user_id < 0):
            raise InvalidUserId("ERROR. The user id should be a positive number.")
            
        # Max 100 followings
        self.connection.getUserFollowings(user_id)
        if (self.connection.LastJson['status'].lower() != 'ok'):    # pragma: no cover
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
        # List of usernames of the followings 
        followings_usernames = []
        followings = self.connection.LastJson['users']
        for following in followings:
            followings_usernames.append(following['username'])
        
        """Wait some time to avoid flooding the servers."""
        time.sleep(20)
            
        # Max 100 followers
        self.connection.getUserFollowers(user_id)
        if (self.connection.LastJson['status'].lower() != 'ok'):    # pragma: no cover
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")  
        # List of usernames of the followers
        followers_usernames = []
        followers = self.connection.LastJson['users']
        for follower in followers:
            followers_usernames.append(follower['username'])
        
        return [followings_usernames, followers_usernames]
    
    def get_levpasha_instagram_data(self, search_user, use_session_file=True, session_file="./levpasha_session.txt"):
        """Downloads Instagram data from a specific user account. In order to do
            that, the previous method will be used to get the profile, followers
            followings, posts, users who liked them as well as the comments."""
        if (type(search_user) != str or search_user == ""):
            raise UsernameNotFound("ERROR. The username should be a non empty string.")
            
        # Connect to LevPasha Instagram API
        self.connect_levpasha_instagram_api(use_session_file, session_file)
        user_data = {}
        try:
            # Profile
            user_data['profile'] = self.get_levpasha_instagram_profile(search_user)
            time.sleep(30)
            
            # Posts
            user_data['posts'] = self.get_levpasha_instagram_posts(user_data['profile']['userid'])
            time.sleep(30)
            # Likers
            user_data['likers'] = self.get_levpasha_instagram_posts_likers(user_data['profile']['username'], user_data['posts'])
            time.sleep(30)
            # Comments of the posts
            user_data['comments'] = self.get_levpasha_instagram_posts_comments(
                user_data['profile']['username'], user_data['posts'])
            time.sleep(30)
            
            # Followers and followings
            contacts = self.get_levpasha_instagram_contacts(user_data['profile']['userid'])
            time.sleep(30)
            user_data['followings'] = contacts[0]
            user_data['followers'] = contacts[1]
            
        except MaxRequestsExceed:   # pragma: no cover
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
        
        return user_data