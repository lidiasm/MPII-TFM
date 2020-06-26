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
    profile = {'username':'Lidia'}
    posts = {'123654': {'likes': '367', 'comments': '12'}}
    comments = {'123':[{'user': 'ana', 'comment': 'Hey hey!'}, {'user': 'eva', 'comment': 'So cool!'}]}
    likers = [('ana',84), ('maria',54)]
    followers = ['anaortiz', 'luciav']
    followings = ['anaortiz', 'luciav']
    user_data = {'profile':profile, 'posts':posts, 'likers':likers, 
                 'comments':comments, 'followers':followers, 'followings':followings}
            
    mo = main_ops.MainOperations()
    result = mo.preprocess_and_store_common_data(user_data, "Instagram")
    assert type(result) == dict
    
def test1_get_user_instagram_common_data():
    """Test to check if the method can get, preprocess and store an Instagram user data."""
    try:
        mo = main_ops.MainOperations()
        username = "lidia.96.sm"
        result = mo.get_user_instagram_common_data(username)
        assert result['profile'] != None and result['contacts'] != None and result['posts'] != None
    except MaxRequestsExceed:
        print("Max requests exceed. Wait to send more.")

def test2_get_user_instagram_common_data():
    """Test to check if the method can get, preprocess and store an Instagram user
        data without specifing the username."""
    mo = main_ops.MainOperations()
    with pytest.raises(UsernameNotFound):
        assert mo.get_user_instagram_common_data('')