#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests to check the methods of the class MainOperations.

@author: Lidia Sánchez Mérida
"""
import sys
import pytest
sys.path.append('src')
import main_ops 
from exceptions import UsernameNotFound, MaxRequestsExceed, UserDataNotFound \
    , InvalidSocialMediaSource

def test1_get_user_instagram_common_data():
    """Test to check if the method can get, preprocess and store an Instagram user data."""
    try:
        mo = main_ops.MainOperations()
        username = "lidia.96.sm"
        result = mo.get_user_instagram_common_data(username)
        assert result['profile'] != None and result['followers'] != None \
           and result['followings'] != None and result['posts'] != None
    except MaxRequestsExceed:
        print("Max requests exceed. Wait to send more.")

def test2_get_user_instagram_common_data():
    """Test to check if the method can get, preprocess and store an Instagram user
        data without specifing the username."""
    mo = main_ops.MainOperations()
    with pytest.raises(UsernameNotFound):
        assert mo.get_user_instagram_common_data('')
        
def test1_preprocess_and_store_common_data():
    """Test to check the method which preprocesses and stores user data without
        providing the user data."""
    mo = main_ops.MainOperations()
    with pytest.raises(UserDataNotFound):
        assert mo.preprocess_and_store_common_data(None, None)
        
def test2_preprocess_and_store_common_data():
    """Test to check the method which preprocesses and stores user data without
        providing the social media source"""
    mo = main_ops.MainOperations()
    with pytest.raises(InvalidSocialMediaSource):
        assert mo.preprocess_and_store_common_data({'username':'lidia'}, None)

def test3_preprocess_and_store_common_data():
    profile = {"userid" : 123456789, "name" : "Lidia Sánchez", "username" : "lidia.96.sm", 
               "biography" : "\"Si eres valiente para empezar, eres fuerte para acabar.\" Ingeniería Informática.",
               "gender" : "None", "profile_pic" : "https://instagram_example", 
               "location" : "None", "birthday" : "None", "date_joined" : "None", 
               "n_followers" : 61, "n_medias" : 6, "id" : "lidia.96.sm", "date" : "13-07-2020", "social_media" : "Instagram" }

    posts = [{'id_post': '1', 'likes': 29, 'comments': 14}, 
              {'id_post': '2', 'likes': 18, 'comments': 0}]
    likers = [('user1',3), ('user2',2), ('user3',0)]
    comments = [{'id_post': '1', 
                  'comments': [{'user': 'user1', 'comment': 'aa'}, {'user': 'user2', 'comment': 'ee'}]},
                  {'id_post': '2', 'comments': [{'user': 'user3', 'comment': 'ii'}, {'user': 'user2', 'comment': 'oo'}]}]
    followers = ['user1', 'user2', 'user3']
    followings = ['user1', 'user4']
    user_data = {'profile':profile, 'posts':posts, 'likers':likers, 
                  'comments':comments, 'followers':followers, 'followings':followings}
    mo = main_ops.MainOperations()
    result = mo.preprocess_and_store_common_data(user_data, "Instagram")
    assert type(result) == dict