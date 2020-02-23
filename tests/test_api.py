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
from exceptions import UsernameNotFound, MaxRequestsExceed, SingletonClass, InvalidCredentials
import os

"""Save the right username because it will be modified in the next tests."""
username = os.environ["INSTAGRAM_USER"]

def test1_init():
    """Test to check the singleton class. In the first place we creates an instance
        and then we try to create another one."""
    first = Api()
    with pytest.raises(SingletonClass):
        assert Api()
        
def test1_get_instance():
    """Test to check the singleton class. If the unique instance is not created,
        it will be created. If it is, then it will be returned."""
    assert Api.get_instance() != None

def test1_connect_to_instagram_api():
    """Test to check a wrong connection to the Instagram Api Levpasha without
        providing the username. In order to do that we modify the env variable of that field."""
    os.environ["INSTAGRAM_USER"] = ""
    with pytest.raises(InvalidCredentials):
        Api.connect_to_instagram_api()

def test2_connect_to_instagram_api():
    """Test to check a wrong connection to the Instagram Api Levpasha providing
        wrong credentials."""
    os.environ["INSTAGRAM_USER"] = "hi"
    with pytest.raises(InvalidCredentials):
        Api.connect_to_instagram_api()

def test3_connect_to_instagram_api():
    """Test to check a right connection to the Instagram Api Levpasha. To do that
        we set de right username."""
    os.environ["INSTAGRAM_USER"] = username
    connection = Api.connect_to_instagram_api()
    assert connection.LastJson['status'] == 'ok'

"""For the next tests we create a global connection to the Instagram Api."""
globalConnection = Api.connect_to_instagram_api()
def test1_get_instagram_user_posts():
    """Test to check the method which gets the posts, with their likes and comments,
        as well as people who like them. In order to do that we specify a random user
         and search their user id to get that information."""
    globalConnection.searchUsername("pabloalvarezss")
    userid = globalConnection.LastJson['user']['pk']
    try:
        result = Api.get_instagram_user_posts(globalConnection, userid)
        assert type(result) == list
    except MaxRequestsExceed:
        print("Max requests exceed. Please wait to send more.")

def test1_get_instagram_user_people():
    """Test to check the method which gets the usernames of 100 followers and 
        followings of an user.In order to do that we specify another random 
        user, searching their user id."""
    globalConnection.searchUsername("pabloalvarezss")
    userid = globalConnection.LastJson['user']['pk']
    try:
        result = Api.get_instagram_user_people(globalConnection, userid)
        assert type(result) == list
    except MaxRequestsExceed:
        print("Max requests exceed. Please wait to send more.")    
        
def test1_instagram_api():
    """Test to check the method which connects to an Instagram API and downloads
        profile data from a user which is not specified."""
    with pytest.raises(UsernameNotFound):
        assert Api.instagram_api("")

def test2_instagram_api():
    """Test to check the method which connects to an Instagram API and download
        data profile from a specific user."""
    try:
        assert type(Api.instagram_api("pabloalvarezss")) == dict
    except MaxRequestsExceed:
        print("Maximum requests exceed. Please wait some time before sending more.")