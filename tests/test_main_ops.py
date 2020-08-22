#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests to check the methods of the class MainOperations.

@author: Lidia Sánchez Mérida
"""
import os
import sys
import pytest
sys.path.append('src')
import main_ops 
from exceptions import UsernameNotFound, MaxRequestsExceed, UserDataNotFound \
    , InvalidDatabaseCredentials, InvalidMongoDbObject, InvalidSocialMediaSource
        
def test1_constructor():
    """
    Test to check the constructor when PostgreSQL credentials are not provided to
    connect to the PostgreSQL database. An exception will be raised.
    """
    global psql_user
    psql_user = os.environ["POSTGRES_USER"]
    os.environ["POSTGRES_USER"] = ""
    global psql_pswd
    psql_pswd = os.environ.get("POSTGRES_PSWD")
    os.environ["POSTGRES_PSWD"] = ""
    with pytest.raises(InvalidDatabaseCredentials):
        assert main_ops.MainOperations()
    
def test1_get_user_instagram_common_data():
    """
    Test to check the method which gets, preprocesses and stores user data using the
    LevPasha Instagram API. It returns None, if the user data has not been inserted,
    or a string id if it has been inserted, for each type of user data: profile,
    medias, likers, texts and contacts.
    """
    global psql_user
    os.environ["POSTGRES_USER"] = psql_user
    global psql_pswd
    os.environ["POSTGRES_PSWD"] = psql_pswd
    try:
        mo = main_ops.MainOperations()
        username = "lidia.96.sm"
        result = mo.get_user_instagram_common_data(username)
        assert type(result) == dict
    except MaxRequestsExceed:
        print("Max requests exceed. Wait to send more.")

def test2_get_user_instagram_common_data():
    """
    Test to check the method which gets, preprocesses and stores user data using the
    LevPasha Instagram API without providing the username. It will raise an exception.
    """
    mo = main_ops.MainOperations()
    with pytest.raises(UsernameNotFound):
        assert mo.get_user_instagram_common_data('')
        
def test1_preprocess_and_store_common_data():
    """
    Test to check the method which preprocesses and stores user data from any
    social media source without providing the user data. An exception will be raised.
    """
    mo = main_ops.MainOperations()
    with pytest.raises(UserDataNotFound):
        assert mo.preprocess_and_store_common_data(None, None)
        
def test2_preprocess_and_store_common_data():
    """
    Test to check the method which preprocesses and stores user data from any
    social media source without providing the social media source. An exception will be raised.
    """
    mo = main_ops.MainOperations()
    with pytest.raises(InvalidSocialMediaSource):
        assert mo.preprocess_and_store_common_data({'username':'lidia'}, None)
        
def test3_preprocess_and_store_common_data():
    """
    Test to check the method which preprocesses and stores user data from any
    social media source without providing a valid social media source. An exception will be raised.
    """
    mo = main_ops.MainOperations()
    with pytest.raises(InvalidSocialMediaSource):
        assert mo.preprocess_and_store_common_data({'username':'lidia'}, 'Random')
        
def test4_preprocess_and_store_common_data():
    """
    Test to check the method which preprocesses and stores user data from any social
    media source without providing a valid MongoDB. In order to do that, the 
    MongoDB object is set to a invalid value, so an exception will be raised.
    """
    mo = main_ops.MainOperations()
    mo.mongodb = ""
    with pytest.raises(InvalidMongoDbObject):
        assert mo.preprocess_and_store_common_data({'username':'lidia'}, 'Instagram')

def test5_preprocess_and_store_common_data():
    """
    Test to preprocess and store user data in the Mongo database from any 
    social media source.
    """
    profile = {"userid" : 123456789, "name" : "Lidia Sánchez", "username" : "lidia.96.sm", 
                "biography" : "\"Si eres valiente para empezar, eres fuerte para acabar.\" Ingeniería Informática.",
                "gender" : "None", "profile_pic" : "https://instagram_example", 
                "location" : "None", "birthday" : "None", "date_joined" : "None", 
                "n_followers" : 61, "n_medias" : 6, "social_media" : "Instagram"}

    medias = [{'id_media': '1', 'like_count': 29, 'comment_count': 14, "title":None}, 
              {'id_media': '2', 'like_count': 18, 'comment_count': 0, "title" : "Title 1"}]
    likers = [{'id_media':'1', 'users':['user1','user2','user3']}]
    texts = [{'id_media': '1', 
              'texts': [{'user': 'user1', 'text': 'aa'}, {'user': 'user2', 'text': 'ee'}],
              'social_media':'Instagram'},
              {'id_media': '2', 
              'texts': [{'user': 'user3', 'text': 'ii'}, {'user': 'user2', 'text': 'oo'}]}]
    contacts = {'followers':['user1', 'user2', 'user3'], 'followings':['user1', 'user4']}
    user_data = {'profile':profile, 'medias':medias, 'likers':likers, 
                  'texts':texts, 'contacts':contacts}
    mo = main_ops.MainOperations()
    result = mo.preprocess_and_store_common_data(user_data, 'Instagram')
    assert type(result) == dict