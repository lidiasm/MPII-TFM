#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Singleton class to establish a connection with one APIs among many APIs in order to download
and preprocess data related to social networks. This information will be
stored in the database.

@author: Lidia Sánchez Mérida
"""

import os
import sys
sys.path.append("../")
from exceptions import SingletonClass, InvalidCredentials, UsernameNotFound \
, MaxRequestsExceed, PostsDictNotFound
from InstagramAPI import InstagramAPI
import time 

class Api:
    __instance = None
    
    def __init__(self):
        """Creates the instance if it doesn't exist."""
        if Api.__instance != None: raise SingletonClass("Singleton class can't have more than one instance.")
        else: Api.__instance = self
    
    @staticmethod
    def get_instance():
        """Gets the current and unique instance. If it doesn't exist, it will be created."""
        if Api.__instance == None: Api()
        return Api.__instance
    
    @staticmethod
    def connect_to_instagram_api():
        """Connects to the api with the username and password of your Instagram account.
            For safety reasons your credentials should be in env variables in your sistem."""
        username = os.environ.get("INSTAGRAM_USER")
        pswd = os.environ.get("INSTAGRAM_PSWD")
        if (type(username) != str or type(pswd) != str or username == None or
            pswd == None or username == "" or pswd == ""):
            raise InvalidCredentials("Username and/or password are not right.")
        
        api = InstagramAPI(username, pswd)
        api.login()
        if (api.LastJson['status'] != 'ok'):
            raise InvalidCredentials("Invalid Instagram credentials.")
        
        return api
    
    @staticmethod
    def get_instagram_profile(api, search_user):
        """Gets and preprocesses data of an user's profile."""
        if (search_user == None or type(search_user) != str or search_user == ""):
            raise UsernameNotFound("ERROR. Invalid username.")
        
        """Search the id of the user."""
        api.searchUsername(search_user)
        if (api.LastJson['status'].lower() != 'ok'):
                raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
                
        """Get the profile of the search user."""
        profile = {}
        profile['userid'] = api.LastJson['user']['pk']
        profile['name'] = api.LastJson['user']['full_name']
        profile['username'] = api.LastJson['user']['username']
        profile['biography'] = api.LastJson['user']['biography']
        profile['gender'] = None
        profile['profile_pic'] = api.LastJson['user']['profile_pic_url']
        profile['location'] = None
        profile['birthday'] = None
        profile['date_joined'] = None
        profile['n_followers'] = api.LastJson['user']['follower_count']
        profile['n_following'] = api.LastJson['user']['following_count']
        profile['n_medias'] = api.LastJson['user']['media_count']
        
        return profile
        
    @staticmethod
    def get_instagram_posts(api, userid):
        """Gets data related to the posts of an user such as their ids, number
            of likes and number of comments."""
        posts = {}
        more_posts = True
        max_id = ""
        while more_posts:
            """Get media user."""
            api.getUserFeed(userid, max_id)
            if (api.LastJson['more_available'] == False):
                more_posts = False
            """We only save media id, likes and comments count."""
            max_id = api.LastJson.get('next_max_id', '')
            items_list = api.LastJson['items']
            for i in items_list:
                posts[i['id']] = {'likes':i['like_count'], 'comments':i['comment_count']}
            
            """Wait some time to avoid flooding the servers."""
            time.sleep(2)
            
        return posts

    @staticmethod
    def get_instagram_posts_likers(api, userid, posts, username):
        """Gets people who like the posts of an user. They're in descending order."""
        if (posts == None or type(posts) != dict):
            raise PostsDictNotFound("ERROR. There aren't any posts so their likers can't be got.")
        if (username == None or type(username) != str):
            raise UsernameNotFound("ERROR. Invalid username.")
        
        likers = {}
        for post in posts:
            api.getMediaLikers(post)
            if (api.LastJson['status'].lower() != 'ok'):
                raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
            """Get likers"""
            if ('users' in api.LastJson):
                users = api.LastJson['users']
                for user in users:
                    if (user['username'] in likers):
                        likers[user['username']] += 1
                    elif (user['username'] != username):
                        likers[user['username']] = 1
            """Wait some time to avoid flooding the servers."""
            time.sleep(2)
                    
        return likers
    
    @staticmethod
    def get_instagram_posts_comments(api, userid, posts, username):
        """Gets people who like the posts of an user. They're in descending order."""
        if (posts == None or type(posts) != dict):
            raise PostsDictNotFound("ERROR. There aren't any posts so their likers can't be got.")
        if (username == None or type(username) != str):
            raise UsernameNotFound("ERROR. Invalid username.")
        
        comments = {}
        for post in posts:
            api.getMediaComments(post)
            # Get max 20 comments
            if (api.LastJson['status'].lower() != 'ok'):
                raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
            
            if ('comments' in api.LastJson):
                post_comments = api.LastJson['comments']
                comments_list = []
                for comm in post_comments:
                    if (comm['user']['username'] != username):
                        comments_list.append({'user':comm['user']['username'], 'comment':comm['text']})
                
                """Add the comments of the post"""
                comments[post] = comments_list
            
            """Wait some time to avoid flooding the servers."""
            time.sleep(2)
        
        return comments

    @staticmethod
    def get_instagram_contacts(api, userid):
        """Gets the followers and followings of an user."""
        # Max 100 followers
        api.getUserFollowings(userid)
        if (api.LastJson['status'].lower() != 'ok'):
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
        """Get the usernames of the followings."""
        followings_usernames = []
        followings = api.LastJson['users']
        for following in followings:
            followings_usernames.append(following['username'])

        # Max 100 followings
        api.getUserFollowers(userid)
        if (api.LastJson['status'].lower() != 'ok'):
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")    
        """Get the usernames of the followers."""
        followers_usernames = []
        followers = api.LastJson['users']
        for follower in followers:
            followers_usernames.append(follower['username'])
        
        return [followings_usernames, followers_usernames]
    
    @staticmethod
    def get_instagram_data(search_user):
        """Gets all type of data from a Instagram user."""
        # Connection to the Instagram API
        api = Api.connect_to_instagram_api()
        user_data = {}
        try:
            user_data['profile'] = Api.get_instagram_profile(api, search_user)
            time.sleep(5)
            user_data['posts'] = Api.get_instagram_posts(api, user_data['profile']['userid'])
            time.sleep(5)
            likers = Api.get_instagram_posts_likers(api, user_data['profile']['userid'],
                    user_data['posts'], user_data['profile']['username'])
            
            """Likers in descending order to show the fans first."""
            sorted_likers = sorted(likers.items(), key=lambda k:k[1], reverse=True) 
            user_data['likers'] = sorted_likers
            time.sleep(5)
            
            user_data['comments'] = Api.get_instagram_posts_comments(api, user_data['profile']['userid'],
                    user_data['posts'], user_data['profile']['username'])
            time.sleep(5)
            contacts = Api.get_instagram_contacts(api, user_data['profile']['userid'])
            time.sleep(5)
            user_data['followings'] = contacts[0]
            user_data['followers'] = contacts[1]
            
        except MaxRequestsExceed:
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
        
        return user_data
