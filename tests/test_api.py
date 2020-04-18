#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests to check the right behaviour of the methods included in the singleton class
Api. 

@author: Lidia Sánchez Mérida
"""

import sys
import pytest
sys.path.append("src")
sys.path.append("src/data")
from api import Api
from exceptions import UsernameNotFound, MaxRequestsExceed, SingletonClass \
, InvalidCredentials, PostsDictNotFound
import os

"""Username to sign in the API."""
username = os.environ["INSTAGRAM_USER"]

def test1_init():
    """Test to check the singleton class in order to not allow creating more than
        one instance."""
    _ = Api()
    with pytest.raises(SingletonClass):
        assert Api()
        
def test1_get_instance():
    """Test to check the singleton class in order to create the instance if it's not
        or return it."""
    assert Api.get_instance() != None

def test1_connect_to_instagram_api():
    """Test to check a wrong connection to the Instagram Api without
        providing the username. In order to do that we modify the env variable 
        of that field."""
    os.environ["INSTAGRAM_USER"] = ""
    with pytest.raises(InvalidCredentials):
        Api.connect_to_instagram_api()

def test2_connect_to_instagram_api():
    """Test to check a wrong connection to the Instagram Api providing
        wrong credentials."""
    os.environ["INSTAGRAM_USER"] = "hi"
    with pytest.raises(InvalidCredentials):
        Api.connect_to_instagram_api()

def test3_connect_to_instagram_api():
    """Test to check a right connection to the Instagram Api. To do that
        we set de right username."""
    os.environ["INSTAGRAM_USER"] = username
    """Global variable which stores the connection to the Instagram API."""
    global connection 
    connection = Api.connect_to_instagram_api()
    assert connection.LastJson['status'] == 'ok'

def test1_get_instagram_profile():
    """Test to check the method which gets the profile of an user."""
    search_user = "pabloalvarezss"
    global connection
    try:
        """Global variable to store the user id to test the next methods without
            sending more requests to get that."""
        global user_profile
        user_profile = Api.get_instagram_profile(connection, search_user)
        assert type(user_profile) == dict
    except MaxRequestsExceed:
        print("Max requests exceed. Please wait to send more.")

def test2_get_instagram_profile():
    """Test to check the method which gets the profile of an user when the username
        is not provided. An exception should be raised."""
    global connection
    with pytest.raises(UsernameNotFound):
        Api.get_instagram_profile(connection, None)

def test1_get_instagram_posts():
    """Test to check the method which gets data posts of an user."""
    global connection
    try:
        global user_profile
        """Global variable which stores the posts of the user to get the likers
            and comments without sending another request."""
        global posts
        posts = Api.get_instagram_posts(connection, user_profile['userid'])
        assert type(posts) == dict
    except MaxRequestsExceed:
        print("Max requests exceed. Please wait to send more.")

def test1_get_instagram_posts_likers():
    """Test to check the method which gets the users who like the posts of an 
        user. """
    username = "pabloalvarezss"
    global connection
    try:
        global user_profile
        """Global variable which stores the posts of the user to get the likers
            and comments without sending another request."""
        global posts
        likers = Api.get_instagram_posts_likers(connection, user_profile['userid'], posts, username)
        assert type(likers) == dict
    except MaxRequestsExceed:
        print("Max requests exceed. Please wait to send more.")

def test2_get_instagram_posts_likers():
    """Test the behaviour of the get likers method when there aren't any posts provided.
        An exception should be raised."""
    username = "pabloalvarezss"
    global connection
    global user_profile
    with pytest.raises(PostsDictNotFound):
        Api.get_instagram_posts_likers(connection, user_profile['userid'], [], username)

def test3_get_instagram_posts_likers():
    """Test the behaviour of the get likers method when a username is not provided.
        An exception should be raised."""
    global connection
    global user_profile
    global posts
    with pytest.raises(UsernameNotFound):
        Api.get_instagram_posts_likers(connection, user_profile['userid'], posts, None)

def test1_get_instagram_posts_comments():
    """Test to check the method which gets the comments of an user's posts."""
    username = "pabloalvarezss"
    global connection
    global user_profile
    try:
        """Global variable which stores the posts of the user to get the likers
            and comments without sending another request."""
        global posts
        comments = Api.get_instagram_posts_comments(connection, user_profile['userid'], posts, username)
        assert type(comments) == dict
    except MaxRequestsExceed:
        print("Max requests exceed. Please wait to send more.")

def test2_get_instagram_posts_comments():
    """Test to check the method which gets the comments of an user's posts
        when there aren't any posts provided. An exception should be raised."""
    username = "pabloalvarezss"
    global connection
    global user_profile
    with pytest.raises(PostsDictNotFound):
        Api.get_instagram_posts_comments(connection, user_profile['userid'], [], username)

def test3_get_instagram_posts_comments():
    """Test to check the method which gets the comments of an user's posts
        when the username is not provided. An exception should be raised."""
    global connection
    global user_profile
    global posts
    with pytest.raises(UsernameNotFound):
        Api.get_instagram_posts_comments(connection, user_profile['userid'], posts, None)
        
def test1_get_instagram_contacts():
    """Test to check the method which gets the followers and followings of an user."""
    global connection
    global user_profile
    try:
        result = Api.get_instagram_contacts(connection, user_profile['userid'])
        assert type(result) == list
    except MaxRequestsExceed:
        print("Max requests exceed. Please wait to send more.")    

def test1_get_instagram_data():
    """Test to check the process which gets all Instagram data type of an user."""
    username = "pabloalvarezss"
    global connection
    try:
        result = Api.get_instagram_data(username)
        assert type(result) == dict
    except MaxRequestsExceed:
        print("Max requests exceed. Please wait to send more.")
