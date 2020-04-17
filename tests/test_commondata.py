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
from exceptions import UsernameNotFound, ProfileDictNotFound, ContactsListsNotFound \
, PostsDictNotFound, LikersListNotFound, IdNotFound, CommentsListNotFound, EmptyCollection

"""Creates a object to connect to the database."""
test_collection = MongoDB(os.environ.get("MONGODB_URI"), 'SocialNetworksDB', 'test')

def test1_preprocess_profile():
    """Test to check the provided profile. In this case it's right because it has
        at least the username."""
    profile = {'username':'lidia', 'name':'Lidia'}
    user_data = {'profile':profile}
    data = commondata.CommonData(test_collection, user_data)
    result = data.preprocess_profile()
    assert type(result) == dict

def test2_preprocess_profile():
    """Test to check the provided profile. In this case it's not right because it
        hasn't got a valid username. It'll raise an exception."""
    profile = {'username':None, 'name':'Lidia'}
    user_data = {'profile':profile}
    data = commondata.CommonData(test_collection, user_data)
    with pytest.raises(UsernameNotFound):
        assert data.preprocess_profile()

def test3_preprocess_profile():
    """Test to check the behaviour of the class when the user profile is not provided.
        It should raise an exception."""
    data = commondata.CommonData(test_collection)
    with pytest.raises(ProfileDictNotFound):
        assert data.preprocess_profile()
        
def test4_preprocess_profile():
    """Test to check the behaviour of the class when there isn't the username
        in the data user."""
    profile = {'name':'Lidia'}
    user_data = {'profile':profile}
    data = commondata.CommonData(test_collection, user_data)
    with pytest.raises(UsernameNotFound):
        assert data.preprocess_profile()

def test5_preprocess_profile():
    """Test to check the behaviour if one of the required fields has a None value."""
    profile = {'username':'Lidia', 'name':'Lidia', 'gender':None}
    user_data = {'profile':profile}
    data = commondata.CommonData(test_collection, user_data)
    result = data.preprocess_profile()
    assert type(result) == dict
        
def test6_preprocess_profile():
    """Test to check the behaviour of the class if there's a not required field.
        It should be removed."""
    profile = {'username':'Lidia', 'name':'Lidia', 'pets':'No'}
    user_data = {'profile':profile}
    data = commondata.CommonData(test_collection, user_data)
    result = data.preprocess_profile()
    assert type(result) == dict

def test7_preprocess_profile():
    """Test to check the behaviour of the class when the profile is not a dict."""
    profile = []
    user_data = {'profile':profile}
    data = commondata.CommonData(test_collection, user_data)
    with pytest.raises(ProfileDictNotFound):
        assert data.preprocess_profile()
        
def test1_preprocess_contacts():
    """Test to check the behaviour of the class when followings aren't in a list.
        It should raise an exception."""
    profile = {'username':'Lidia'}
    followings = "Hey"
    followers = ['anaortiz', 'luciav']
    user_data = {'profile':profile, 'followings':followings, 'followers':followers}
    data = commondata.CommonData(test_collection, user_data)
    with pytest.raises(ContactsListsNotFound):
        assert data.preprocess_contacts()
        
def test2_preprocess_contacts():
    """Same test than the previous one except in this case followers aren't in a list."""
    profile = {'username':'Lidia'}
    followers = "Hey"
    followings = ['anaortiz', 'luciav']
    user_data = {'profile':profile, 'followings':followings, 'followers':followers}
    data = commondata.CommonData(test_collection, user_data)
    with pytest.raises(ContactsListsNotFound):
        assert data.preprocess_contacts()

def test3_preprocess_contacts():
    """Test to check if the followers/followings are lists. In this case both are."""
    profile = {'username':'Lidia'}
    followers = ['anaortiz', 'luciav']
    followings = ['anaortiz', 'luciav']
    user_data = {'profile':profile, 'followings':followings, 'followers':followers}
    data = commondata.CommonData(test_collection, user_data)
    result = data.preprocess_contacts() 
    assert type(result) == dict and type(result['followers']) == list and type(result['followings']) == list

def test4_preprocess_contacts():
    """Test to check if the followers/followings are lists and removes the None values."""
    profile = {'username':'Lidia'}
    followers = ['anaortiz', None]
    followings = ['anaortiz', 'luciav']
    user_data = {'profile':profile, 'followings':followings, 'followers':followers}
    data = commondata.CommonData(test_collection, user_data)
    result = data.preprocess_contacts() 
    assert type(result) == dict and type(result['followers']) == list and type(result['followings']) == list
    
def test1_preprocess_posts():
    """Test to check the type of the posts, which should be a dict. In this case it's not,
        so the method will raise an exception."""
    profile = {'username':'Lidia'}
    posts = []
    user_data = {'profile':profile, 'posts':posts}
    data = commondata.CommonData(test_collection, user_data)
    with pytest.raises(PostsDictNotFound):
       assert data.preprocess_posts()

def test2_preprocess_posts():
    """Test to check that each post has an id. In this case some hasn't so an
        exception will be raised."""
    profile = {'username':'Lidia'}
    posts = {'123':{'likes':'367', 'comments':'23'}, '':{'likes':'54', 'comments':'78'}}
    user_data = {'profile':profile, 'posts':posts}
    data = commondata.CommonData(test_collection, user_data)
    with pytest.raises(IdNotFound):
       assert data.preprocess_posts()

def test3_preprocess_posts():
    """Test to check that likes and comments are integer numbers. In this case some
        of them aren't so an exception will be raised."""
    profile = {'username':'Lidia'}
    posts = {'123':{'likes':'367', 'comments':'23'}, '654':{'likes':'hey', 'comments':'78'}}
    user_data = {'profile':profile, 'posts':posts}
    data = commondata.CommonData(test_collection, user_data)
    with pytest.raises(ValueError):
       assert data.preprocess_posts()
       
def test4_preprocess_posts():
    """Test to check that posts are in a dict and their fields are correct. In this
        case they are."""
    profile = {'username':'Lidia'}
    posts = {'123':{'likes':'367', 'comments':'23'}, '654':{'likes':'45', 'comments':'78'}}
    user_data = {'profile':profile, 'posts':posts}
    data = commondata.CommonData(test_collection, user_data)
    result = data.preprocess_posts()
    assert type(result) == dict
    
def test1_preprocess_likers():
    """Test to check the preprocess likers method when there aren't any posts."""
    profile = {'username':'Lidia'}
    likers = [('luciav',5), ('ana',10)]
    user_data = {'profile':profile, 'likers':likers}
    data = commondata.CommonData(test_collection, user_data)
    with pytest.raises(PostsDictNotFound):
        assert data.preprocess_likers()
        
def test2_preprocess_likers():
    """Test to check that likers are in a list. In this case there aren't so it
        should raise an exception."""
    profile = {'username':'Lidia'}
    posts = {'123654': {'likes': '367', 'comments': '12'}}
    likers = {}
    user_data = {'profile':profile, 'posts':posts, 'likers':likers}
    data = commondata.CommonData(test_collection, user_data)
    with pytest.raises(LikersListNotFound):
        assert data.preprocess_likers()
        
def test3_preprocess_likers():
    """Test to check that likers are in a list. In this case they are."""
    profile = {'username':'Lidia'}
    posts = {'123654': {'likes': '367', 'comments': '12'}}
    likers = [('ana',84), ('maria',54)]
    user_data = {'profile':profile, 'posts':posts, 'likers':likers}
    data = commondata.CommonData(test_collection, user_data)
    result = data.preprocess_likers()
    assert type(result) == list
    
def test1_preprocess_comments():
    """Test to check the preprocess comments method when there aren't any posts."""
    profile = {'username':'Lidia'}
    comments = [{'123':[{'user': 'ana', 'comment': 'Hey hey!'}]}]
    user_data = {'profile':profile, 'comments':comments}
    data = commondata.CommonData(test_collection, user_data)
    with pytest.raises(PostsDictNotFound):
        assert data.preprocess_comments()
        
def test2_preprocess_comments():
    """Test to check that comments are in a list. In this case there aren't so it
        should raise an exception."""
    profile = {'username':'Lidia'}
    posts = {'123654': {'likes': '367', 'comments': '12'}}
    comments = {}
    user_data = {'profile':profile, 'posts':posts, 'comments':comments}
    data = commondata.CommonData(test_collection, user_data)
    with pytest.raises(CommentsListNotFound):
        assert data.preprocess_comments()
        
def test3_preprocess_comments():
    """Test to check that comments are in a list. In this case they are."""
    profile = {'username':'Lidia'}
    posts = {'123654': {'likes': '367', 'comments': '12'}}
    comments = [{'123654':[{'user': 'ana', 'comment': 'Hey hey!'}]}]
    user_data = {'profile':profile, 'posts':posts, 'comments':comments}
    data = commondata.CommonData(test_collection, user_data)
    result = data.preprocess_comments()
    assert type(result) == list
    
def test1_preprocess_user_data():
    """Test to check the method which preprocess all user data with the previous
        tested methods."""
    profile = {'username':'Lidia'}
    posts = {'123654': {'likes': '367', 'comments': '12'}}
    comments = [{'123654':[{'user': 'ana', 'comment': 'Hey hey!'}]}]
    likers = [('ana',84), ('maria',54)]
    followers = ['anaortiz', 'luciav']
    followings = ['anaortiz', 'luciav']
    user_data = {'profile':profile, 'posts':posts, 'likers':likers, 
                 'comments':comments, 'followers':followers, 'followings':followings}
    
    data = commondata.CommonData(test_collection, user_data)
    result = data.preprocess_user_data()
    assert type(result) == dict

def test1_add_user_data():
    """Test to check that user data is preprocessed and inserted in the test 
        collection of the database. We make sure the user data don't already exist by
        deleting the collection."""
    try:
        test_collection.empty_collection()
    except EmptyCollection:
        print('Collection was already empty')
        
    profile = {'username':'Lidia'}
    posts = {'123654': {'likes': '367', 'comments': '12'}}
    comments = [{'123654':[{'user': 'ana', 'comment': 'Hey hey!'}]}]
    likers = [('ana',84), ('maria',54)]
    followers = ['anaortiz', 'luciav']
    followings = ['anaortiz', 'luciav']
    user_data = {'profile':profile, 'posts':posts, 'likers':likers, 
                 'comments':comments, 'followers':followers, 'followings':followings}
    
    data = commondata.CommonData(test_collection, user_data)
    result = data.add_user_data()
    assert type(result) == str

def test1_get_user_data():
    """Test to check the behaviour of the get method when there's not username provided.
        It should raise an exception."""
    data = commondata.CommonData(test_collection)
    with pytest.raises(UsernameNotFound):
        assert data.get_user_data("")

def test2_get_user_data():
    """Test to check the behaviour of the get method when the username provided doesn't exist.
        It should raise an exception."""
    data = commondata.CommonData(test_collection)
    with pytest.raises(IdNotFound):
        assert data.get_user_data('heyyy')
        
def test3_get_user_data():
    """Test to check the behaviour of the get method when the username exists."""
    data = commondata.CommonData(test_collection)
    result = data.get_user_data('Lidia')
    assert type(result) == dict