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
from exceptions import SingletonClass, InvalidCredentials, UsernameNotFound, MaxRequestsExceed
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
    def get_instagram_user_posts(api, userid):
        """Get their posts, likes and comments count."""
        posts = {}
        morePosts = True
        maxId = ""
        likers = {}
        while morePosts:
            """Get media user."""
            api.getUserFeed(userid, maxId)
            if (api.LastJson['more_available'] == False):
                morePosts = False
            """We only save a media id, likes and comments count."""
            maxId = api.LastJson.get('next_max_id', '')
            itemsList = api.LastJson['items']
            for i in itemsList:
                posts[str(i['id'])] = {'likes':str(i['like_count']), 'comments':str(i['comment_count'])}
                api.getMediaLikers(i['id'])
                if (api.LastJson['status'].lower() != 'ok'):
                    raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
                
                users = api.LastJson['users']
                for user in users:
                    if (user['username'] in likers):
                        likers[user['username']] += 1
                    else:
                        likers[user['username']] = 1

            """Wait some time to avoid flooding the servers."""
            time.sleep(2)
        
        return [posts, likers]
    
    @staticmethod
    def get_instagram_user_people(api, userid):
        """Get max 100 followings."""
        api.getUserFollowings(userid)
        if (api.LastJson['status'].lower() != 'ok'):
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
        
        """Get the usernames of the followings."""
        followingsUsernames = []
        followings = api.LastJson['users']
        for following in followings:
            followingsUsernames.append(following['username'])

        """Get max 100 followers."""
        api.getUserFollowers(userid)
        if (api.LastJson['status'].lower() != 'ok'):
            raise MaxRequestsExceed("Max requests exceed. Wait to send more.")
            
        """Get the usernames of the followers."""
        followersUsernames = []
        followers = api.LastJson['users']
        for follower in followers:
            followersUsernames.append(follower['username'])
        
        return [followingsUsernames, followersUsernames]
        
    @staticmethod
    def instagram_api(searchUser):
        if (searchUser == None or type(searchUser) != str or searchUser == ""):
            raise UsernameNotFound("Invalid username.")
        """Connection."""
        api = Api.connect_to_instagram_api()
        userData = {}
        
        """Get the profile of the search user."""
        api.searchUsername(searchUser)
        userid = api.LastJson['user']['pk']
        profile = {}
        profile['name'] = api.LastJson['user']['full_name']
        profile['username'] = api.LastJson['user']['username']
        profile['email'] = None
        profile['biography'] = api.LastJson['user']['biography']
        profile['gender'] = None
        profile['profile_pic'] = api.LastJson['user']['profile_pic_url']
        profile['location'] = None
        profile['birthday'] = None
        profile['date_joined'] = None
        profile['private_account'] = api.LastJson['user']['is_private']
        profile['n_followers'] = api.LastJson['user']['follower_count']
        profile['n_following'] = api.LastJson['user']['following_count']
        profile['n_medias'] = api.LastJson['user']['media_count']
        """Add the profile to the final dict."""
        userData['profile'] = profile
        
        """Add the posts and ordered likers."""
        posts_likers = Api.get_instagram_user_posts(api, userid)
        userData['posts'] = posts_likers[0]
        likers = posts_likers[1]
        sortedLikers = sorted(likers.items(), key=lambda k:k[1], reverse=True) 
        userData['likers'] = sortedLikers
        
        """Add the usernames of the followers and followings."""
        people = Api.get_instagram_user_people(api, userid)
        userData['followings'] = people[0]
        userData['followers'] = people[1]
        
        return userData
