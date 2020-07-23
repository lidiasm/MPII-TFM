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
from exceptions import InvalidMongoDbObject, UsernameNotFound, ProfileDictNotFound \
    , ContactsListsNotFound, PostsListNotFound, PostDictNotFound, LikersListNotFound \
    , CommentsListNotFound, PostCommentNotFound, CommentDictNotFound, EmptyCollection \
    , UserDataNotFound, CollectionNotFound, InvalidSocialMediaSource, IdNotFound, DuplicatedPost

"""Creates a object to connect to the database."""
test_collection = MongoDB('test')

def test1_set_mongodb_connection():
    """Test to check the method which sets the connection to the MongoDB database
        without providing a MongoDB object. It will raise an exception"""
    data = commondata.CommonData()
    with pytest.raises(InvalidMongoDbObject):
        data.set_mongodb_connection("Mongodb object")
    
def test2_set_mongodb_connection():
    """Test to set a connection to the 'test' collection in the Mongo database."""
    data = commondata.CommonData()
    result = data.set_mongodb_connection(test_collection)
    assert type(result) == MongoDB
    
def test1_preprocess_profile():
    """Test to preprocess the user profile without providing it. It'll raise
        an exception."""
    data = commondata.CommonData()
    with pytest.raises(ProfileDictNotFound):
        assert data.preprocess_profile([])

def test2_preprocess_profile():
    """Test to preprocess an user profile in which there is not username field
        so an exception will be raised."""
    profile = {'name':'Lidia'}
    data = commondata.CommonData()
    with pytest.raises(UsernameNotFound):
        assert data.preprocess_profile(profile)

def test3_preprocess_profile():
    """Test to preprocess an user profile in which there is not a valid username.
        So an exception will be raised."""
    profile = {'username':1234, 'name':'Lidia'}
    data = commondata.CommonData()
    with pytest.raises(UsernameNotFound):
        assert data.preprocess_profile(profile)
        
def test4_preprocess_profile():
    """Test to preprocess an user profile with None values in some of their fields.
        They should be turn into the string 'None'."""
    profile = {'username':'Lidia', 'name':'Lidia', 'gender':None}
    data = commondata.CommonData()
    result = data.preprocess_profile(profile)
    assert type(result) == dict
        
def test5_preprocess_profile():
    """Test to preprocess the profile with non-required fields.
        They will be removed of the preprocessed profile."""
    profile = {'username':'Lidia', 'name':'Lidia', 'pets':'No'}
    data = commondata.CommonData()
    result = data.preprocess_profile(profile)
    assert type(result) == dict

def test1_preprocess_contacts():
    """Test to preprocess the followers and followings of an specific user without
         providing them. It will raise an exception."""
    data = commondata.CommonData()
    with pytest.raises(ContactsListsNotFound):
        assert data.preprocess_contacts({}, 1234)

def test2_preprocess_contacts():
    """Test to preprocess the followers and followings of an specific user. It will
        return the list of valid followers and followings. In this case, each item
        is a non-empty string (username)."""
    followers = ['user1', 'user2']
    followings = ['user1', 'user3']
    data = commondata.CommonData()
    contacts = data.preprocess_contacts(followers, followings)
    assert type(contacts) == dict and type(contacts['followers']) == list and type(contacts['followings']) == list \
        and len(contacts['followers']) > 0 and len(contacts['followings']) > 0
        
def test3_preprocess_contacts():
    """Test to preprocess the followers and followings of an specific user. It will
        return the list of valid followers and followings. In this case, some of them
        aren't strings so they will be removed from the lists."""
    followers = ['user1', 2, 5, None, 'user2']
    followings = ['user1', 1, 2, 20.0, 'user3']
    data = commondata.CommonData()
    contacts = data.preprocess_contacts(followers, followings)
    assert all(isinstance(item, str) for item in contacts['followings']) == True and \
        all(isinstance(item, str) for item in contacts['followers']) == True
        
def test1_preprocess_posts():
    """Test to check if the provided posts of the user are in a list. In this case,
        they're not so an exception will be raised."""
    data = commondata.CommonData()
    with pytest.raises(PostsListNotFound):
        assert data.preprocess_posts({})
   
def test2_preprocess_posts():
    """Test to check if each post in the list is a dictionary. In this case,
        they're not so an exception will be raised."""
    data = commondata.CommonData()
    with pytest.raises(PostDictNotFound):
        assert data.preprocess_posts([1,2,3,4])
   
def test3_preprocess_posts():
    """Test to check if each post has an id and the number of likes and comments.
        In this case, they haven't these fields so an exception will be raised."""
    posts = [{'likes': 29, 'comments': 14}]
    data = commondata.CommonData()
    with pytest.raises(PostDictNotFound):
        assert data.preprocess_posts(posts)

def test4_preprocess_posts():
    """Test to check if each post has an id and the number of likes and comments.
        In this test, neither the number of likes nor the number of comments are
        number, so an exception will be raised."""
    posts = [{'id_post': '1', 'likes': None, 'comments': ""}]
    data = commondata.CommonData()
    with pytest.raises(ValueError):
        assert data.preprocess_posts(posts)
        
def test5_preprocess_posts():
    """Test to check if each post only appears once in a list of posts. In this
        case the id of the same post is in the list twice so an exception will be raised."""
    posts = [{'id_post': '1', 'likes': 123, 'comments': 456},
             {'id_post': '2', 'likes': 45, 'comments': 56},
             {'id_post': '3', 'likes': 32, 'comments': 12},
             {'id_post': '1', 'likes': 48, 'comments': 72}]
    data = commondata.CommonData()
    with pytest.raises(DuplicatedPost):
        assert data.preprocess_posts(posts)
       
def test6_preprocess_posts():
    """Test to check the method which preprocesses the posts of a specific user."""
    posts = [{'id_post': '1', 'likes': 29, 'comments': 14}, 
              {'id_post': '2', 'likes': 18, 'comments': 0}]
    data = commondata.CommonData()
    result = data.preprocess_posts(posts)
    assert type(result) == list
    
def test1_preprocess_likers():
    """Test to check the method which preprocesses the list of people who liked
        some posts of a specific user without providing these data. It will raise an exception."""
    data = commondata.CommonData()
    with pytest.raises(LikersListNotFound):
        assert data.preprocess_likers([])
        
def test2_preprocess_likers():
    """Test to check the method which preprocesses the list of people who liked
        some posts of a specific user without providing valid data. It will raise an exception."""
    data = commondata.CommonData()
    with pytest.raises(LikersListNotFound):
        assert data.preprocess_likers([1,2,3,4])
        
def test3_preprocess_likers():
    """Test to check the method which preprocesses the list of people who liked
        some posts of a specific user without providing valid data. It will raise an exception."""
    data = commondata.CommonData()
    with pytest.raises(LikersListNotFound):
        assert data.preprocess_likers([("user1", 2), ("user2", "3")])
        
def test4_preprocess_likers():
    """Test to preprocess the poeple who liked some posts of a specific user."""
    data = commondata.CommonData()
    result = data.preprocess_likers([("user1", 2), ("user2", 3)])
    assert type(result) == list

def test1_preprocess_comments():
    """Test to check the method which preprocesses the comments of the posts of a specific user
        without providing any comments. It will raise an exception."""
    data = commondata.CommonData()
    with pytest.raises(CommentsListNotFound):
        assert data.preprocess_comments({})

def test2_preprocess_comments():
    """Test to check the method which preprocesses the comments of the posts of a specific user
        without providing valid comments. It will raise an exception."""
    data = commondata.CommonData()
    with pytest.raises(PostCommentNotFound):
        assert data.preprocess_comments([{}])

def test3_preprocess_comments():
    """Test to check the method which preprocesses the comments of the posts of a specific user
        without providing valid comments. It will raise an exception."""
    comments = [{'id_post': '1'}, {'comments': 0}]
    data = commondata.CommonData()
    with pytest.raises(PostCommentNotFound):
        assert data.preprocess_comments(comments)
        
def test4_preprocess_comments():
    """Test to check the method which preprocesses the comments of the posts of a specific user
        without providing valid comments. It will raise an exception."""
    comments = [{'id_post': 1234, 'comments':None}, {'comments': 0}]
    data = commondata.CommonData()
    with pytest.raises(PostCommentNotFound):
        assert data.preprocess_comments(comments)
        
def test5_preprocess_comments():
    """Test to check the method which preprocesses the comments of the posts of a specific user
        without providing valid comments. It will raise an exception."""
    comments = [{'id_post': '1234', 'comments':[{}]}, {'id_post':'1234', 'comments': [{}]}]
    data = commondata.CommonData()
    with pytest.raises(CommentDictNotFound):
        assert data.preprocess_comments(comments)
        
def test6_preprocess_comments():
    """Test to check the method which preprocesses the comments of the posts of a specific user
        without providing valid comments. It will raise an exception."""
    comments = [{'id_post': '1234', 'comments':[{'user':'user1'}]}, {'id_post':'1234', 'comments': [{}]}]
    data = commondata.CommonData()
    with pytest.raises(CommentDictNotFound):
        assert data.preprocess_comments(comments)
        
def test7_preprocess_comments():
    """Test to check the method which preprocesses the comments of the posts of a specific user
        without providing valid comments. It will raise an exception."""
    comments = [{'id_post': '1234', 'comments':[{'user':'user1', 'comment':1234}]}]
    data = commondata.CommonData()
    with pytest.raises(CommentDictNotFound):
        assert data.preprocess_comments(comments)

def test8_preprocess_comments():
    """Test to check the method which preprocesses the comments of the posts of a specific user
        without providing valid comments. It will raise an exception."""
    comments = [{'id_post': '1234', 'comments':[{'user':'user1', 'comment':'comment 1'},
                                                {'user':'user2', 'comment':'comment 2'}]}]
    data = commondata.CommonData()
    preprocessed_comments = data.preprocess_comments(comments)
    assert type(preprocessed_comments) == list
    
def test1_preprocess_user_data():
    """Test to check the method which preprocesses all user data with the previous
        tested methods."""
    profile = {'username':'Lidia'}
    posts = [{'id_post': '1', 'likes': 29, 'comments': 14}, 
              {'id_post': '2', 'likes': 18, 'comments': 0}]
    likers = [('user1',3), ('user2',2), ('user3',0)]
    comments = [{'id_post': '1', 
                  'comments': [{'user': 'user1', 'comment': 'aa'}, {'user': 'user2', 'comment': 'ee'}]},
                  {'id_post': '2', 'comments': [{'user': 'user3', 'comment': 'ii'}, {'user': 'user2', 'comment': 'oo'}]}]
    user_data = {'profile':profile, 'posts':posts, 'likers':likers, 
                  'comments':comments, 'followers':['user1', 'user2'], 'followings':['user1', 'user3']}
    
    data = commondata.CommonData()
    result = data.preprocess_user_data(user_data)
    assert type(result) == dict
        
def test1_preprocess_text_comments():
    """Test the behaviour of the method which preprocesses the text of the post
        comments. A list of preprocessed comments will be returned."""
    comments = [{'id_post': '1', 'comments': [
                      {'user': 'user1', 'comment': 'Alcohollll alcohol te quiero amigo♥️'}, 
                      {'user': 'user2', 'comment': '🤤🤤🤤'}]},
                  {'id_post': '2', 'comments': [
                      {'user': 'user3', 'comment': 'quien volviera'}, 
                      {'user': 'user2', 'comment': 'Guapo 😍'}]}]
    
    data = commondata.CommonData()
    preprocessed_comments = data.preprocess_text_comments(comments)
    assert type(preprocessed_comments) == list

def test1_add_user_data():
    """Test to check the method which inserts user data into the collection 'test' of the
        MongoDB database without providing a valid username. An exception will be raised."""
    data = commondata.CommonData(test_collection)
    with pytest.raises(UsernameNotFound):
        assert data.add_user_data('', {}, '', '')
        
def test2_add_user_data():
    """Test to check the method which inserts user data into the collection 'test' of the
        MongoDB database without providing a user data. An exception will be raised."""
    data = commondata.CommonData(test_collection)
    with pytest.raises(UserDataNotFound):
        assert data.add_user_data('lidia.96.sm', {}, '', '')
        
def test3_add_user_data():
    """Test to check the method which inserts user data into the collection 'test' of the
        MongoDB database without providing a user data. An exception will be raised."""
    profile = {'username':'Lidia'}
    posts = [{'id_post': '1', 'likes': 29, 'comments': 14}, {'id_post': '2', 'likes': 18, 'comments': 0}]
    comments = [{'id_post': '1', 'comments': [
                      {'user': 'user1', 'comment': 'Alcohollll alcohol te quiero amigo♥️'}, 
                      {'user': 'user2', 'comment': '🤤🤤🤤'}]},
                  {'id_post': '2', 'comments': [
                      {'user': 'user3', 'comment': 'quien volviera'}, 
                      {'user': 'user2', 'comment': 'Guapo 😍'}]}]
    
    user_data = {'profile':profile, 'posts':posts, 'comments':comments}
    data = commondata.CommonData(test_collection)
    with pytest.raises(CollectionNotFound):
        assert data.add_user_data('lidia.96.sm', user_data, '', '')

def test4_add_user_data():
    """Test to check the method which inserts user data into the collection 'test' of the
        MongoDB database without providing a valid social media source. An exception will be raised."""
    profile = {'username':'Lidia'}
    posts = [{'id_post': '1', 'likes': 29, 'comments': 14}, {'id_post': '2', 'likes': 18, 'comments': 0}]
    comments = [{'id_post': '1', 'comments': [
                      {'user': 'user1', 'comment': 'Alcohollll alcohol te quiero amigo♥️'}, 
                      {'user': 'user2', 'comment': '🤤🤤🤤'}]},
                  {'id_post': '2', 'comments': [
                      {'user': 'user3', 'comment': 'quien volviera'}, 
                      {'user': 'user2', 'comment': 'Guapo 😍'}]}]
    
    user_data = {'profile':profile, 'posts':posts, 'comments':comments}
    data = commondata.CommonData(test_collection)
    with pytest.raises(InvalidSocialMediaSource):
        assert data.add_user_data('lidia.96.sm', user_data, 'test', '')
        
def test5_add_user_data():
    """Test to check the method which inserts user data into the collection 'test' of the
        MongoDB database without providing a valid MongoDB object. An exception will be raised."""
    profile = {'username':'Lidia'}
    posts = [{'id_post': '1', 'likes': 29, 'comments': 14}, {'id_post': '2', 'likes': 18, 'comments': 0}]
    comments = [{'id_post': '1', 'comments': [
                      {'user': 'user1', 'comment': 'Alcohollll alcohol te quiero amigo♥️'}, 
                      {'user': 'user2', 'comment': '🤤🤤🤤'}]},
                  {'id_post': '2', 'comments': [
                      {'user': 'user3', 'comment': 'quien volviera'}, 
                      {'user': 'user2', 'comment': 'Guapo 😍'}]}]
    
    user_data = {'profile':profile, 'posts':posts, 'comments':comments}
    data = commondata.CommonData()
    with pytest.raises(InvalidMongoDbObject):
        assert data.add_user_data('lidia.96.sm', user_data, 'test', 'Instagram')

def test6_add_user_data():
    """Test to check the method which inserts user data into the collection 'test' of the
        MongoDB database. In order to do that, first, a MongoDB object will be created to
        connect to the Mongo database and the 'test' collection in the local system.
        Then, the documents of the 'test' collection will be removed in order to prevent
        exceptions if the user data is already inserted in the same day."""
    # Connection to the 'test' collection in MongoDB
    test_connection = MongoDB('test')
    try:
        test_connection.empty_collection()
    except EmptyCollection:
        print("Empty collection")
        
    profile = {"userid" : 123456789, "name" : "Lidia Sánchez", "username" : "lidia.96.sm", 
                   "biography" : "\"Si eres valiente para empezar, eres fuerte para acabar.\" Ingeniería Informática.", 
                   "gender" : "None", "profile_pic" : "https://instagram_example", 
                   "location" : "None", "birthday" : "None", "date_joined" : "None", 
                   "n_followers" : 61, "n_medias" : 6, "id" : "lidia.96.sm", "date" : "14-07-2020", "social_media" : "Instagram" }

    posts = [{'id_post': '1', 'likes': 29, 'comments': 14}, {'id_post': '2', 'likes': 18, 'comments': 0}]
    comments = [{'id_post': '1', 'comments': [
                      {'user': 'user1', 'comment': 'Alcohollll alcohol te quiero amigo♥️'}, 
                      {'user': 'user2', 'comment': '🤤🤤🤤'}]},
                  {'id_post': '2', 'comments': [
                      {'user': 'user3', 'comment': 'quien volviera'}, 
                      {'user': 'user2', 'comment': 'Guapo 😍'}]}]
    
    user_data = {'profile':profile, 'posts':posts, 'comments':comments}
    data = commondata.CommonData(test_collection)
    result = data.add_user_data('lidia.96.sm', user_data, 'test', 'Instagram')
    assert type(result[0]) == str and type(result[1] == dict)
        
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
    """Test to check the behaviour of the get method without providing a valid MongoDB
        object. It should raise an exception."""
    data = commondata.CommonData()
    with pytest.raises(InvalidMongoDbObject):
        assert data.get_user_data('lidia.96.sm')
        
def test4_get_user_data():
    """Test to check the behaviour of the get method when the username exists."""
    data = commondata.CommonData(test_collection)
    result = data.get_user_data('lidia.96.sm')
    assert type(result) == dict