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
    , InvalidUserId, InvalidLimit, PostListNotFound, PostDictNotFound
from InstagramAPI import InstagramAPI
import time 
import pickle

class Api:
    
    def __init__(self):
        """
        Creates an API object whose attributes are:
            - The connection to one of the avalaible APIs.

        Returns
        -------
        An API object.
        """
        self.connection = None
        
    def connect_levpasha_instagram_api(self, use_session_file=True, 
                                       session_file="./levpasha_session.txt"):
        """
        Connects to the LevPasha Instagram API. The two avalaible ways are:
            - Using a file in which there is a connection object to the API.
            - The credentials of your Instagram account. For safety reasons 
                there should be as env variables in the sistem.

        Parameters
        ----------
        use_session_file : bool
            If True, a filename must be provided in order to load the connection object.
            If False, the Instagram credentials will be used to make the connection.
        session_file : str
            The filename which could be used for:
                - Loading the connection object to the Instagram API.
                - Storing the connection made to the Instagram API.
            The default is "./levpasha_session.txt".

        Raises
        ------
        InvalidCredentials
            If the credentials are not strings, are not stored are not in env 
            variables or are wrong.

        Returns
        -------
        The connection made to the LevPasha Instagram API.
        """
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
        """
        Gets the profile of the specified user using the LevPasha Instagram API.

        Parameters
        ----------
        search_user : str
            The username of the Instagram user in order to get their profile.

        Raises
        ------
        UsernameNotFound
            If the provided username is not a non-empty string.
        MaxRequestsExceed
            If the maximum number of requests has been excedeed.

        Returns
        -------
        profile : dict
            It's a dict with the interesting fields of the profile of the user.
        """
        if (type(search_user) != str or search_user == ""):
            raise UsernameNotFound("ERROR. The username should be a non empty string.")
        # Check the connection to the API Instagram
        if (self.connection == None):
            self.connection = self.connect_levpasha_instagram_api()
            
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
        """
        Gets post data of a specific user. Establishing a maximum number of post
        data is advisable in order to not exceed the maximum number of requests
        of the LevPasha Instagram API. By default, the maximum number of post
        data is 100 posts.

        Parameters
        ----------
        user_id : integer
            It's the user id which represents the user to get their post data.
        limit : integer
            It's the maximum number of post data to get. The default is 100.

        Raises
        ------
        InvalidUserId
            If the provided user id is not a positive integer.
        InvalidLimit
            If the provided maximum of post data is not a positive integer.

        Returns
        -------
        posts : list of dicts.
            It's the list of post data whose fields are:
                - The post id.
                - The post title.
                - The like_count as well as comment_count.
        """
        # Check the user id
        if (type(user_id) != int or user_id < 0):
            raise InvalidUserId("ERROR. The user id should be a positive number.")
        # Check the limit
        if (type(limit) != int or limit <= 0):
            raise InvalidLimit("ERROR. The post limit should be a number greater than 0.")
        # Check the connection to the API Instagram
        if (self.connection == None):
            self.connection = self.connect_levpasha_instagram_api()
            
        posts = []
        more_posts = True
        max_id = ""
        n_downloaded_posts = 0
        # Get posts while there are still more posts
        while more_posts:
            self.connection.getUserFeed(user_id, max_id)
            if (self.connection.LastJson['more_available'] == False):
                more_posts = False

            # Save the media id, its number of likes and comments.
            max_id = self.connection.LastJson.get('next_max_id', '')
            items_list = self.connection.LastJson['items']
            for i in items_list:
                posts.append({'id_media':i['id'], 
                              'title':None,
                              'like_count':i['like_count'], 
                              'comment_count':i['comment_count']})
            
            n_downloaded_posts += len(items_list)
            if (n_downloaded_posts >= limit): break
            # IMPORTANT!
            ## Wait some time to avoid flooding the servers.
            time.sleep(20)
            
        return posts
    
    def get_levpasha_instagram_posts_likers(self, username, posts):
        """
        Gets the usernames of the people who liked some Instagram posts of a 
        specific user.

        Parameters
        ----------
        username : str
            The username of the user to get the people who liked their posts.
        posts : list of dicts.
            It's the list of posts of the user. It'll be used to get the post ids
            in order to get the usernames of the people who liked them.

        Raises
        ------
        UsernameNotFound
            If the provided username is not a non-empty string.
        PostListNotFound
            If the provided list of posts is not a non-empty list of dicts.
        PostDictNotFound
            If the provided list of posts is not a non-empty list of dicts.
        MaxRequestsExceed
            If the maximum number of requests has been excedeed.

        Returns
        -------
        likers : list of dicts.
            A list of dicts in which each dict contains the people who liked each
            post.
        """
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non empty string.")
        if (type(posts) != list or len(posts) == 0):
            raise PostListNotFound("ERROR. There aren't any posts to get their likers.")
        # Check the connection to the API Instagram
        if (self.connection == None):
            self.connection = self.connect_levpasha_instagram_api()
            
        # Iterate over each post in order to get the usernames of the people who liked it.
        likers = []
        for post in posts:
            # Check each post
            if (type(post) != dict or len(post) == 0):
                raise PostDictNotFound("ERROR. Each post should be a non empty dict.")
            if ('id_media' not in post):
                raise PostDictNotFound("ERROR. Each post should have its id.")
                
            self.connection.getMediaLikers(post['id_media'])
            # IMPORTANT !
            ## Prevent max requests exception
            if (self.connection.LastJson['status'].lower() != 'ok'):    # pragma: no cover
                raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
            
            if ('users' in self.connection.LastJson):
                users = self.connection.LastJson['users']
                current_likers = []
                # Get the usernames of the people who liked the current post
                for user in users:
                    if (user['username'] != username):
                        current_likers.append(user['username'])
            
            # Store the likers of each post
            likers.append({'id_media':post['id_media'], 'users':current_likers})
            # IMPORTANT!
            ## Wait some time to avoid flooding the servers.
            time.sleep(20)
        
        return likers
     
    def get_levpasha_instagram_posts_comments(self, username, posts):
        """
        Gets the comments of the users who commented in the posts of a specific
        user.

        Parameters
        ----------
        username : str
            The username of the user to get comments of their posts.
        posts : list of dicts.
            It's the list of posts of the user. It'll be used to get the post ids
            in order to get their comments.

        Raises
        ------
        UsernameNotFound
            If the provided username is not a non-empty string.
        PostListNotFound
            If the provided list of posts is not a non-empty list of dicts.
        PostDictNotFound
            If the provided list of posts is not a non-empty list of dicts.
        MaxRequestsExceed
            If the maximum number of requests has been excedeed.

        Returns
        -------
        comments : list of dicts.
            A list of dicts in which each dict which contains the comments of each post.
        """
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non empty string.")
        if (type(posts) != list or len(posts) == 0):
            raise PostListNotFound("ERROR. There aren't any posts to get their likers.")
        # Check the connection to the API Instagram
        if (self.connection == None):
            self.connection = self.connect_levpasha_instagram_api()
            
        comments = []
        for post in posts:
            # Check each post
            if (type(post) != dict or len(post) == 0):
                raise PostDictNotFound("ERROR. Each post should be a non empty dict.")
            if ('id_media' not in post):
                raise PostDictNotFound("ERROR. Each post should have its id.")
            
            # IMPORTANT!
            ## 20 max comments per post
            self.connection.getMediaComments(post['id_media'])
            if (self.connection.LastJson['status'].lower() != 'ok'):    # pragma: no cover
                raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
            # Save the user who wrote the comment and the text
            if ('comments' in self.connection.LastJson):
                post_comments = self.connection.LastJson['comments']
                comments_list = []
                for comm in post_comments:
                    if (comm['user']['username'] != username):
                        comments_list.append({'user':comm['user']['username'], 'text':comm['text']})
                
                """Add the comments of the post"""
                comments.append({'id_media':post['id_media'], 'texts':comments_list})
            
            """Wait some time to avoid flooding the servers."""
            time.sleep(20)
        
        return comments
    
    def get_levpasha_instagram_contacts(self, user_id):
        """
        Gets the usernames of the followers and followings of a specific user.

        Parameters
        ----------
        user_id : integer
            It's the user id which represents the user to get their post data.

        Raises
        ------
        InvalidUserId
            If the provided user id is not a positive integer.
        MaxRequestsExceed
            If the maximum number of requests has been excedeed.

        Returns
        -------
        A dict whose keys are:
            - followings, which contains the list of followings.
            - followers, which contains the list of followers.
        """
        # Check the user id
        if (type(user_id) != int or user_id < 0):
            raise InvalidUserId("ERROR. The user id should be a positive number.")
        # Check the connection to the API Instagram
        if (self.connection == None):
            self.connection = self.connect_levpasha_instagram_api()
        
        # IMPORTANT!
        ## Max 100 followings
        self.connection.getUserFollowings(user_id)
        if (self.connection.LastJson['status'].lower() != 'ok'):    # pragma: no cover
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
        # List of usernames of the followings 
        followings_usernames = []
        followings = self.connection.LastJson['users']
        for following in followings:
            followings_usernames.append(following['username'])
        
        # IMPORTANT!
        ## Wait some time to avoid flooding the servers.
        time.sleep(20)
            
        # IMPORTANT!
        ## Max 100 followers
        self.connection.getUserFollowers(user_id)
        if (self.connection.LastJson['status'].lower() != 'ok'):    # pragma: no cover
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")  
            
        # List of usernames of the followers
        followers_usernames = []
        followers = self.connection.LastJson['users']
        for follower in followers:
            followers_usernames.append(follower['username'])
        
        return {'followings':followings_usernames, 'followers':followers_usernames}
    
    def get_levpasha_instagram_data(self, search_user, use_session_file=True, 
                                    session_file="./levpasha_session.txt"):
        """
        Gets Instagram data from a specific user account. In order to do that,
        the previous methods will be used to get data such as:
            - The profile.
            - The posts of the user along with the people who liked them as well
                as the comments.
                - The list of followings and followers.

        Parameters
        ----------
        search_user : str
            The username of the Instagram user in order to get their profile.
        use_session_file : bool
            If True, a filename must be provided in order to load the connection object.
            If False, the Instagram credentials will be used to make the connection.
        session_file : str
            The filename which could be used for:
                - Loading the connection object to the Instagram API.
                - Storing the connection made to the Instagram API.
            The default is "./levpasha_session.txt".

        Raises
        ------
        UsernameNotFound
            If the provided username is not a non-empty string.
        MaxRequestsExceed
            If the maximum number of requests has been excedeed.

        Returns
        -------
        user_data : dict
            It's a dict with the Instagram data of a specific user. Keys are:
                - profile, which contains the dict of the user profile.
                - medias, which contains a list of the posts of the user with
                    their ids, titles and number of likes and comments.
                - likers, which contains the list of usernames which represent
                    the people who liked each media.
                - texts, which contains a list of the posts of the user with their
                    ids, the usernames of the people who wrote comments on them 
                    as well as the text.
                - followings, which is the list of followings of the user.
                - followers, which is the list of followers of the user.
                
        """
        if (type(search_user) != str or search_user == ""):
            raise UsernameNotFound("ERROR. The username should be a non empty string.")
            
        # Connect to LevPasha Instagram API
        self.connection = self.connect_levpasha_instagram_api(use_session_file, session_file)
        user_data = {}
        try:
            # Profile
            user_data['profile'] = self.get_levpasha_instagram_profile(search_user)
            time.sleep(30)
            
            # Posts
            user_data['medias'] = self.get_levpasha_instagram_posts(user_data['profile']['userid'])
            time.sleep(30)
            # Likers
            user_data['likers'] = self.get_levpasha_instagram_posts_likers \
                (user_data['profile']['username'], user_data['medias'])
            time.sleep(30)
            # Comments of the posts
            user_data['texts'] = self.get_levpasha_instagram_posts_comments(
                user_data['profile']['username'], user_data['medias'])
            time.sleep(30)
            
            # Followers and followings
            user_data['contacts'] = self.get_levpasha_instagram_contacts(user_data['profile']['userid'])
            
        except MaxRequestsExceed:   # pragma: no cover
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
        
        return user_data