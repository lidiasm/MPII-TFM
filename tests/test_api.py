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
from exceptions import InvalidCredentials, UsernameNotFound, MaxRequestsExceed \
    , InvalidUserId, InvalidLimit, PostsListNotFound, PostDictNotFound
import os

"""Store the right username to connect to the API to test the connection
    method setting invalid credentials."""
username = os.environ["INSTAGRAM_USER2"]

"""Username to test the class with."""
search_user = "lidia.96.sm"

"""API object"""
api = Api()

def test1_connect_levpasha_instagram_api():
    """Test to check the behaviour of the method which connects to LevPasha
        Instagram API without providing a right username. In order to do that,
        we set the env username variable to an empty string. It will raise an exception."""
    os.environ["INSTAGRAM_USER2"] = ""
    with pytest.raises(InvalidCredentials):
        api.connect_levpasha_instagram_api(use_session_file=False)

def test2_connect_levpasha_instagram_api():
    """Test to check the behaviour of the method which connects to LevPasha
        Instagram API providing invalid credentials. In order to do that,
        we set the env username variable to an invalid value. It will raise an exception."""
    os.environ["INSTAGRAM_USER2"] = "hey"
    with pytest.raises(InvalidCredentials):
        api.connect_levpasha_instagram_api(use_session_file=False)

def test3_connect_levpasha_instagram_api():
    """Test to connect to LevPasha using Instagram credentials and then save the
        connection object into a file."""
    os.environ["INSTAGRAM_USER2"] = username
    result = api.connect_levpasha_instagram_api(use_session_file=False)
    assert result.LastJson['status'] == 'ok'

def test4_connect_levpasha_instagram_api():
    """Test to connect to LevPasha using the previous file in which there is
        a connection object to login again."""
    result = api.connect_levpasha_instagram_api(session_file=1234)
    assert result.LastJson['status'] == 'ok'

def test1_get_levpasha_instagram_profile():
    """Test to check the behaviour of the method which gets the user profile
        without providing a right username."""
    with pytest.raises(UsernameNotFound):
        api.get_levpasha_instagram_profile(None)

def test2_get_levpasha_instagram_profile():
    """Test to downloads the Instagram profile of a specific user using
        the LevPasha Instagram API."""
    try:
        global profile
        api_prof = Api()
        profile = api_prof.get_levpasha_instagram_profile(search_user)
        assert type(profile) == dict
    except MaxRequestsExceed:
        print("Max requests exceed. Please wait to send more.")

def test1_get_levpasha_instagram_posts():
    """Test to check the behaviour of the method which gets the posts of an user
        without providing a right user id. It will raise an exception."""
    with pytest.raises(InvalidUserId):
        api.get_levpasha_instagram_posts(user_id=None)

def test2_get_levpasha_instagram_posts():
    """Test to check the behaviour of the method which gets the posts of an user
        without providing a right limit. It will raise an exception."""
    with pytest.raises(InvalidLimit):
        api.get_levpasha_instagram_posts(user_id=1234, limit=0)

def test3_get_levpasha_instagram_posts():
    """Test to download the posts of a specific user using their user id and the
        LevPasha Instagram API."""
    try:
        global profile     
        if (type(profile) == dict and len(profile) > 0):
            global posts
            api_posts = Api()
            posts = api_posts.get_levpasha_instagram_posts(user_id=profile['userid'])
            assert type(posts) == list
    except MaxRequestsExceed:
        print("Max requests exceed. Please wait to send more.")

def test1_get_levpasha_instagram_posts_likers():
    """Test to check the behaviour of the method which gets the usernames of 
        the Instagram users who liked the posts of the specific user without
        providing a right username. It will raise an exception."""
    with pytest.raises(UsernameNotFound):
        api.get_levpasha_instagram_posts_likers(None, None)

def test2_get_levpasha_instagram_posts_likers():
    """Test to check the behaviour of the method which gets the usernames of 
        the Instagram users who liked the posts of the specific user without
        providing their posts. It will raise an exception."""
    with pytest.raises(PostsListNotFound):
        api.get_levpasha_instagram_posts_likers(search_user, {})

def test3_get_levpasha_instagram_posts_likers():
    """Test to check the behaviour of the method which gets the usernames of 
        the Instagram users who liked the posts of the specific user without
        providing valid posts. It will raise an exception."""
    invalid_posts = [1234]
    with pytest.raises(PostDictNotFound):
        api.get_levpasha_instagram_posts_likers(search_user, invalid_posts)
        
def test4_get_levpasha_instagram_posts_likers():
    """Test to check the behaviour of the method which gets the usernames of 
        the Instagram users who liked the posts of the specific user without
        providing valid posts. It will raise an exception."""
    invalid_posts = [{'post':13}]
    with pytest.raises(PostDictNotFound):
        api.get_levpasha_instagram_posts_likers(search_user, invalid_posts)

def test5_get_levpasha_instagram_posts_likers():
    """Test to get the usernames of the Instagram users who liked the posts
        of a specific user."""
    try:
        global posts
        if (type(posts) == list and len(posts) > 0):
            api_likers = Api()
            likers = api_likers.get_levpasha_instagram_posts_likers(search_user, posts)
            assert type(likers) == list
    except MaxRequestsExceed:
        print("Max requests exceed. Please wait to send more.")
        
def test1_get_levpasha_instagram_posts_comments():
    """Test to check the behaviour of the method which gets the comments wrote
        by Instagram users to the posts of a specific user without
        providing a right username. It will raise an exception."""
    with pytest.raises(UsernameNotFound):
        api.get_levpasha_instagram_posts_comments(None, None)

def test2_get_levpasha_instagram_posts_comments():
    """Test to check the behaviour of the method which gets the comments wrote
        by Instagram users to the posts of a specific user without
        providing their posts. It will raise an exception."""
    with pytest.raises(PostsListNotFound):
        api.get_levpasha_instagram_posts_comments(search_user, {})

def test3_get_levpasha_instagram_posts_comments():
    """Test to check the behaviour of the method which gets the comments wrote
        by Instagram users to the posts of a specific user without
        providing valid posts. It will raise an exception."""
    invalid_posts = [1234]
    with pytest.raises(PostDictNotFound):
        api.get_levpasha_instagram_posts_comments(search_user, invalid_posts)
        
def test4_get_levpasha_instagram_posts_comments():
    """Test to check the behaviour of the method which gets the comments wrote
        by Instagram users to the posts of a specific user without
        providing valid posts. It will raise an exception."""
    invalid_posts = [{'post':13}]
    with pytest.raises(PostDictNotFound):
        api.get_levpasha_instagram_posts_comments(search_user, invalid_posts)

def test5_get_levpasha_instagram_posts_comments():
    """Test to get the the comments wrote by Instagram users to the posts
        of a specific user. Their usernames will be stored too."""
    try:
        global posts
        if (type(posts) == list and len(posts) > 0):
            api_comments = Api()
            comments = api_comments.get_levpasha_instagram_posts_comments(search_user, posts)
            assert type(comments) == list
    except MaxRequestsExceed:
        print("Max requests exceed. Please wait to send more.")
        
def test1_get_levpasha_instagram_contacts():
    """Test to check the behaviour of the method which gets the followers and
        followings of a specific user without providing their right user id.
        It will raise an exception."""
    with pytest.raises(InvalidUserId):
        api.get_levpasha_instagram_contacts(user_id=-90)

def test2_get_levpasha_instagram_contacts():
    """Test to download the usernames of the followers and followings of a
        specific user account (max 100 for each one)."""
    try:
        global profile
        if (type(profile) == dict):
            api_contacts = Api()
            contacts = api_contacts.get_levpasha_instagram_contacts(user_id=profile['userid'])
            assert type(contacts[0]) == list and type(contacts[1]) == list
    except MaxRequestsExceed:
        print("Max requests exceed. Please wait to send more.")

def test1_get_levpasha_instagram_data():
    """Test to get the Instagram data of a specific user account using the previous
        methods. In this case an exception will be raised because the username isn't correct."""
    with pytest.raises(UsernameNotFound):
        api.get_levpasha_instagram_data(1234)

def test2_get_levpasha_instagram_data():
    """Test to download Instagram data of a specific user using LevPasha Instagram API."""
    try:
        user_data = api.get_levpasha_instagram_data(search_user)
        assert type(user_data) == dict
    except MaxRequestsExceed:
        print("Max requests exceed. Please wait to send more.")