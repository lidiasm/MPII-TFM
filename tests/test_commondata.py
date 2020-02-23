#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests to check the right behaviour of the methods included in the class CommonData.

@author: Lidia Sánchez Mérida
"""

import os
import sys
import pytest
sys.path.append("src")
from mongodb import MongoDB
sys.path.append("src/data")
import commondata 
from exceptions import ProfileNotFound, BasicProfileDataNotFound, RelathionshipsListNotFound, LikersListNotFound, PostsDictNotFound, IdNotFound, UsernameNotFound

"""Creates a object to connect to the database."""
testCollection = MongoDB(os.environ.get("MONGODB_URI"), 'SocialNetworksDB', 'test')

def test1_check_profile_field():
    """Test to check if the field 'birthday' exists in a JSON dict. In this case
        it doesn't so it will return None"""
    profile = {'username':'lidia', 'name':'Lidia', 'email':'lidia@lidia.es'}
    followings = {'1':'Ana Ortiz', '2':'Eva García'}
    followers = {'1':'Ana Ortiz', '2':'Paloma Peña'}
    data1 = commondata.CommonData(testCollection, profile, {}, {}, followings, followers)
    assert data1.check_profile_field('birthday') == None

def test2_check_profile_field():
    """Test to check if the field 'username' exists in a JSON dict. In this case
        it does so it will return its value."""
    profile = {'username':'lidia', 'name':'Lidia', 'email':'lidia@lidia.es'}
    followings = {'1':'Ana Ortiz', '2':'Eva García'}
    followers = {'1':'Ana Ortiz', '2':'Paloma Peña'}
    data1 = commondata.CommonData(testCollection, profile, {}, {}, followings, followers)
    assert type(data1.check_profile_field('username')) == str and data1.check_profile_field('username') != "None"

def test3_check_profile_field():
    """Test to check if a None value is changed to 'None' string."""
    profile = {'username':'lidia', 'name':'Lidia', 'email':'lidia@lidia.es', 'location':None}
    followings = {'1':'Ana Ortiz', '2':'Eva García'}
    followers = {'1':'Ana Ortiz', '2':'Paloma Peña'}
    data1 = commondata.CommonData(testCollection, profile, {}, {}, followings, followers)
    assert data1.check_profile_field('location') == None

def test1_profile_preprocessing():
    """Test to check if the provided profile is valid. In this case it is so
        after the preprocessing it will be returned."""
    profile = {'username':'lidia', 'name':'Lidia', 'email':'lidia@lidia.es'}
    followings = {'1':'Ana Ortiz', '2':'Eva García'}
    followers = {'1':'Ana Ortiz', '2':'Paloma Peña'}
    data1 = commondata.CommonData(testCollection, profile, {}, {}, followings, followers)
    assert type(data1.profile_preprocessing()) == dict

def test2_profile_preprocessing():
    """Test to check if the provided profile is valid. In this case it's not
        so the method will raise an exception."""
    profile = {'username':None}
    followings = {'1':'Ana Ortiz', '2':'Eva García'}
    followers = {'1':'Ana Ortiz', '2':'Paloma Peña'}
    data1 = commondata.CommonData(testCollection, profile, {}, {}, followings, followers)
    with pytest.raises(BasicProfileDataNotFound):
        assert data1.profile_preprocessing()

def test3_profile_preprocessing():
    """Test to check if the provided profile is valid. In this case it's not
        so the method will raise an exception."""
    data1 = commondata.CommonData(testCollection, {}, {}, {}, {}, {})
    with pytest.raises(ProfileNotFound):
        assert data1.profile_preprocessing()
        
def test1_relationships_preprocessing():
    """Test to check if the followers/followings are lists. In this case followings
        isn't so the method will raise an exception."""
    profile = {'username':None}
    followings = "Hey"
    followers = ['anaortiz', 'luciav']
    data1 = commondata.CommonData(testCollection, profile, {}, {}, followings, followers)
    with pytest.raises(RelathionshipsListNotFound):
        assert data1.relationships_preprocessing()
        
def test2_relationships_preprocessing():
    """Test to check if the followers/followings are lists. In this case followers
        isn't so the method will raise an exception."""
    profile = {'username':None}
    followers = "Hola"
    followings = ['anaortiz', 'luciav']
    data1 = commondata.CommonData(testCollection, profile, {}, {}, followings, followers)
    with pytest.raises(RelathionshipsListNotFound):
        assert data1.relationships_preprocessing()

def test3_relationships_preprocessing():
    """Test to check if the followers/followings are lists. In this case both are"""
    profile = {'username':None}
    followers = ['anaortiz', 'luciav']
    followings = ['anaortiz', 'luciav', 'zuck', 'nick']
    data1 = commondata.CommonData(testCollection, profile, {}, {}, followings, followers)
    assert data1.relationships_preprocessing() == True
    
def test4_relationships_preprocessing():
    """Test to check if the followers/followings are lists and removes the None values."""
    profile = {'username':None}
    followers = ['anaortiz', None, 'anita']
    followings = ['anaortiz', 'luciav', 'zuck', 'nick']
    data1 = commondata.CommonData(testCollection, profile, {}, {}, followings, followers)
    assert data1.relationships_preprocessing() == True
    
def test5_relationships_preprocessing():
    """Test to check if the followers/followings are lists and removes the None values."""
    profile = {'username':None}
    followers = ['anaortiz', 'anita']
    followings = ['anaortiz', None, None, 'zuck', 'nick']
    data1 = commondata.CommonData(testCollection, profile, {}, {}, followings, followers)
    assert data1.relationships_preprocessing() == True

def test1_likers_preprocessing():
    """Test to check the likers method when there aren't any posts."""
    profile = {'username':None}
    followers = ['zuck', 'luciav', 'ana']
    followings = ['anaortiz', 'luciav']
    likers = [('luciav',5), ('ana',10)]
    data1 = commondata.CommonData(testCollection, profile, {}, likers, followings, followers)
    with pytest.raises(PostsDictNotFound):
        assert data1.likers_preprocessing()
        
def test2_likers_preprocessing():
    """Test to check the type of likers dict."""
    profile = {'username':'lidia'}
    posts = {'id':'1', 'likes':'23', 'comments':'3'}
    followers = ['zuck', 'luciav', 'ana']
    followings = ['anaortiz', 'luciav']
    data1 = commondata.CommonData(testCollection, profile, posts, "Hey", followings, followers)
    with pytest.raises(LikersListNotFound):
        assert data1.likers_preprocessing()
        
def test3_likers_preprocessing():
    """Test to check the likers dict. In this case, it's correct."""
    profile = {'username':'lidia'}
    posts = {'id':'1', 'likes':'23', 'comments':'3'}
    likers = [('luciav',5), ('ana',10)]
    followers = ['zuck', 'luciav', 'ana']
    followings = ['anaortiz', 'luciav']
    data1 = commondata.CommonData(testCollection, profile, posts, likers, followings, followers)
    assert data1.likers_preprocessing() == True
        
def test1_posts_preprocessing():
    """Test to check if the posts dict exists or not. In this case, there isn't."""
    profile = {'username':None}
    followers = ['zuck', 'luciav', 'ana']
    followings = ['anaortiz', 'luciav']
    data1 = commondata.CommonData(testCollection, profile, [], {}, followings, followers)
    with pytest.raises(PostsDictNotFound):
        assert data1.posts_preprocessing()

def test2_posts_preprocessing():
    """Test to check the structure of the posts dict. In this case, it's correct."""
    profile = {'username':None}
    posts = {'1': {'likes':'23', 'comments':'3'}, '2': {'likes':'5', 'comments':'1'}}
    followers = ['zuck', 'luciav', 'ana']
    followings = ['anaortiz', 'luciav']
    data1 = commondata.CommonData(testCollection, profile, posts, [], followings, followers)
    assert data1.posts_preprocessing() == True
        
def test3_posts_preprocessing():
    """Test to check the structure of the posts dict. None keys are not valid."""
    profile = {'username':None}
    posts = {'1': {'likes':'23', 'comments':'3'}, None: {'likes':'23', 'comments':'3'}}
    followers = ['zuck', 'luciav', 'ana']
    followings = ['anaortiz', 'luciav']
    data1 = commondata.CommonData(testCollection, profile, posts, [], followings, followers)
    with pytest.raises(IdNotFound):
        assert data1.posts_preprocessing()
        
def test1_preprocessing():
    """Test to check if the data are correct. In this case, they are so the
        method will return them."""
    profile = {'username':'lidia', 'name':'Lidia', 'email':'lidia@lidia.es'}
    posts = {'1': {'likes':'23', 'comments':'3'}, '2': {'likes':'5', 'comments':'1'}}
    followings = ['anaortiz', 'luciav']
    followers = ['anaortiz']
    data1 = commondata.CommonData(testCollection, profile, posts, [], followings, followers)
    assert type(data1.preprocessing()) == dict

def test1_add_user_data():
    """Test to check the insert method into the database. If the new record has the
        same username and date, then it will no be inserted. Otherwise, it will.
        In order to test the method, we first check if the user is already in the database."""
    profile = {'username':'eva', 'name':'Eva'}
    posts = {'1': {'likes':'23', 'comments':'3'}, '2': {'likes':'5', 'comments':'1'}}
    likers = [('lidiasm',5), ('luciav',18)]
    followings = ['anaortiz', 'luciav', 'lidiasm']
    followers = ['anaortiz', 'lidiasm']
    data = commondata.CommonData(testCollection, profile, posts, likers, followings, followers)
    if (data.get_user_data('eva') != None):
        data.mongodb.delete_item('id', 'eva')
    
    result = data.add_user_data()
    assert result != None

def test2_get_user_data():
    data1 = commondata.CommonData(testCollection)
    with pytest.raises(UsernameNotFound):
        assert data1.get_user_data("")

def test3_get_user_data():
    data1 = commondata.CommonData(testCollection)
    with pytest.raises(IdNotFound):
        assert data1.get_user_data('heyyy')