#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests to check the right behaviour of the methods included in the class CommonData.

@author: Lidia Sánchez Mérida
"""
import sys
import pytest
sys.path.append("src")
from mongodb import MongoDB
sys.path.append("src/data")
import commondata 
from exceptions import InvalidMongoDbObject, ProfileDictNotFound, UsernameNotFound \
    , ContactDictNotFound, MediaListNotFound, MediaDictNotFound, LikerListNotFound \
    , TextListNotFound, TextDictNotFound, UserDataNotFound, CollectionNotFound \
    , InvalidQuery, InvalidSocialMediaSource, InvalidUserId
    
# Creates a object to connect to the database.
test_collection = MongoDB('test')

def test1_set_mongodb_connection():
    """
    Test to check the method which sets the connection to the Mongo database
    without providing a MongoDB object. It will raise an exception.
    """
    data = commondata.CommonData()
    with pytest.raises(InvalidMongoDbObject):
        data.set_mongodb_connection("Mongodb object")
    
def test2_set_mongodb_connection():
    """
    Test to set a connection to the 'test' collection in the Mongo database.
    """
    data = commondata.CommonData()
    result = data.set_mongodb_connection(test_collection)
    assert type(result) == MongoDB
    
def test1_preprocess_profile():
    """
    Test to check the method which preprocesses the user profile without 
    providing it. It'll raise an exception.
    """
    data = commondata.CommonData()
    with pytest.raises(ProfileDictNotFound):
        assert data.preprocess_profile([], None)

def test2_preprocess_profile():
    """
    Test to check the method which preprocesses the user profile without 
    providing the username. It'll raise an exception.
    """
    profile = {'name':'Lidia'}
    data = commondata.CommonData()
    with pytest.raises(UsernameNotFound):
        assert data.preprocess_profile(profile, None)

def test3_preprocess_profile():
    """
    Test to check the method which preprocesses the user profile without 
    providing a valid username. It'll raise an exception.
    """
    profile = {'username':1234, 'name':'Lidia'}
    data = commondata.CommonData()
    with pytest.raises(UsernameNotFound):
        assert data.preprocess_profile(profile, None)
        
def test4_preprocess_profile():
    """
    Test to check the method which preprocesses the user profile without 
    providing a valid social media source. It'll raise an exception.
    """
    profile = {'username':'Lidia', 'name':'Lidia', 'gender':None}
    data = commondata.CommonData()
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_profile(profile, None)

def test5_preprocess_profile():
    """
    Test to check the method which preprocesses the user profile without 
    providing a valid social media source. It'll raise an exception.
    """
    profile = {'username':'Lidia', 'name':'Lidia', 'gender':None}
    data = commondata.CommonData()
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_profile(profile, "Random Social Media")
        
def test6_preprocess_profile():
    """
    Test to check the method which preprocesses the user profile in which there
    are some 'None' values. These will be transform to strings.
    """
    profile = {'username':'Lidia', 'name':'Lidia', 'gender':None}
    data = commondata.CommonData()
    result = data.preprocess_profile(profile, 'Instagram')
    assert type(result) == dict
        
def test7_preprocess_profile():
    """
    Test to check the method which preprocesses the user profile in which there
    are some non-required fields. They will be removed of the preprocessed profile.
    """
    profile = {'username':'Lidia', 'name':'Lidia', 'pets':'No'}
    data = commondata.CommonData()
    result = data.preprocess_profile(profile, 'Instagram')
    assert type(result) == dict

def test1_preprocess_contacts():
    """
    Test to check the method which preprocesses the followers and followings 
    of an user account without providing them. It will raise an exception.
    """
    data = commondata.CommonData()
    with pytest.raises(ContactDictNotFound):
        assert data.preprocess_contacts({}, None, None)

def test2_preprocess_contacts():
    """
    Test to check the method which preprocesses the followers and followings of
    an user account without providing a valid dict of contacts. It will raise an exception.
    """
    data = commondata.CommonData()
    with pytest.raises(ContactDictNotFound):
        assert data.preprocess_contacts({'id':'1'}, None, None)
        
def test3_preprocess_contacts():
    """
    Test to check the method which preprocesses the followers and followings of
    an user account without providing a valid dict of contacts. It will raise an exception.
    """
    data = commondata.CommonData()
    contacts = {'followers':(), 'followings':['user1']}
    with pytest.raises(ContactDictNotFound):
        assert data.preprocess_contacts(contacts, None, None)

def test4_preprocess_contacts():
    """
    Test to check the method which preprocesses the followers and followings of
    an user account without providing a valid social media source. It will raise an exception.
    """
    contacts = {'followers':['user2'], 'followings':['user1']}
    data = commondata.CommonData()
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_contacts(contacts, None, None)

def test5_preprocess_contacts():
    """
    Test to check the method which preprocesses the followers and followings of
    an user account without providing a valid social media source. It will raise an exception.
    """
    contacts = {'followers':['user2'], 'followings':['user1']}
    data = commondata.CommonData()
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_contacts(contacts, "Random", None)

def test6_preprocess_contacts():
    """
    Test to check the method which preprocesses the followers and followings of
    an user account without providing a valid user id. It will raise an exception.
    """
    contacts = {'followers':['user2'], 'followings':['user1']}
    data = commondata.CommonData()
    with pytest.raises(InvalidUserId):
        assert data.preprocess_contacts(contacts, "Instagram", None)
        
def test7_preprocess_contacts():
    """
    Test to check the method which preprocesses the followers and followings of 
    a specific user.
    """
    data = commondata.CommonData()
    contacts = {'followers':[1, 'user1', 'user2', 'user3'], 
                'followings':['user1',' user2', 4, 5]}
    preprocessed_contacts = data.preprocess_contacts(contacts, "Instagram", 123456)
    assert len(preprocessed_contacts['followers']) == 3 and len(preprocessed_contacts['followings']) == 2

def test1_preprocess_medias():
    """
    Test to check the method which preprocesses the medias of a specific user
    without providing them. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(MediaListNotFound):
        assert data.preprocess_medias({}, None, None)

def test2_preprocess_medias():
    """
    Test to check the method which preprocesses the medias of a specific user
    without providing a valid social media source. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_medias([1,2,3,4], None, None)
        
def test3_preprocess_medias():
    """
    Test to check the method which preprocesses the medias of a specific user
    without providing a valid social media source. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_medias([1,2,3,4], 'Random', None)

def test4_preprocess_medias():
    """
    Test to check the method which preprocesses the medias of a specific user
    without providing a valid user id. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(InvalidUserId):
        assert data.preprocess_medias([1,2,3,4], 'Instagram', None)
        
def test5_preprocess_medias():
    """
    Test to check the method which preprocesses the medias of a specific user
    without providing a valid list of medias. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(MediaDictNotFound):
        assert data.preprocess_medias([1,2,3,4], 'Instagram', 123456)
        
def test6_preprocess_medias():
    """
    Test to check the method which preprocesses the medias of a specific user
    without providing the required keys for the dict of medias. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(MediaDictNotFound):
        assert data.preprocess_medias([{'id_media':'1', 'title':''}], 'Instagram', 123456)
        
def test7_preprocess_medias():
    """
    Test to check the method which preprocesses the medias of a specific user
    without providing valid values for some keys. An exception will be raised.
    """
    data = commondata.CommonData()
    medias = [{'id_media':'1', 'title':'Title 1', 'like_count':-8, 'comment_count':0, 'social_media':'Instagram'}]
    with pytest.raises(MediaDictNotFound):
        assert data.preprocess_medias(medias, 'Instagram', 123456)

def test8_preprocess_medias():
    """
    Test to check the method which preprocesses the medias of a specific user.
    """
    data = commondata.CommonData()
    medias = [{'id_media':'1', 'title':'Title 1', 'like_count':5, 'comment_count':0, 'social_media':'Instagram'},
              {'id_media':'2', 'title':'Title 2', 'like_count':18, 'comment_count':12, 'social_media':'Instagram'},
              {'id_media':'3', 'title':'Title 3', 'like_count':7, 'comment_count':58, 'social_media':'Instagram'},]
    preprocessed_medias = data.preprocess_medias(medias, 'Instagram', 123456)
    assert type(preprocessed_medias) == dict and len(preprocessed_medias) > 0
    
def test1_preprocess_media_likers():
    """
    Test to check the method which preprocesses the people who liked the medias
    of an user without providing them. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(LikerListNotFound):
        assert data.preprocess_media_likers(None, None, None)
        
def test2_preprocess_media_likers():
    """
    Test to check the method which preprocesses the people who liked the medias
    of an user without providing a valid list of usernames. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(LikerListNotFound):
        assert data.preprocess_media_likers([1,2,3,4], None, None)

def test3_preprocess_media_likers():
    """
    Test to check the method which preprocesses the people who liked the medias
    of an user without providing the social media source. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_media_likers([{'id_media':134, 'user':'user1'}], None, None)
        
def test4_preprocess_media_likers():
    """
    Test to check the method which preprocesses the people who liked the medias
    of an user without providing a valid social media source. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_media_likers([{'id_media':134, 'user':'user1'}], 'Random', None)

def test5_preprocess_media_likers():
    """
    Test to check the method which preprocesses the people who liked the medias
    of an user without providing a valid user id. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(InvalidUserId):
        assert data.preprocess_media_likers([{'id_media':134, 'user':'user1'}], 'Instagram', None)
        
def test6_preprocess_media_likers():
    """
    Test to check the method which preprocesses the people who liked the medias
    of an user without providing a valid list of usernames. An exception will be raised.
    """
    data = commondata.CommonData()
    invalid_likers = [{'id_media':134, 'user':'user1'}]
    with pytest.raises(LikerListNotFound):
        assert data.preprocess_media_likers(invalid_likers, 'Instagram', 123456)
        
def test7_preprocess_media_likers():
    """
    Test to check the method which preprocesses the people who liked the medias
    of an user without providing a valid list of usernames. An exception will be raised.
    """
    data = commondata.CommonData()
    invalid_likers = [{'id_media':134, 'users':'user1', 'social_media':'Instagram'}]
    with pytest.raises(LikerListNotFound):
        assert data.preprocess_media_likers(invalid_likers, 'Instagram', 123456)
        
def test8_preprocess_media_likers():
    """
    Test to check the method which preprocesses the people who liked the medias
    of an user without providing a valid list of usernames. An exception will be raised.
    """
    data = commondata.CommonData()
    invalid_likers = [{'id_media':'1', 'users':['user1', 'user2', 3], 'social_media':'Instagram'}]
    with pytest.raises(LikerListNotFound):
        assert data.preprocess_media_likers(invalid_likers, 'Instagram', 123456)
        
def test9_preprocess_media_likers():
    """
    Test to check the method which preprocesses the people who liked the medias
    of an user.
    """
    data = commondata.CommonData()
    likers = [{'id_media':'2', 'users':['user1', 'user2'], 'social_media':'Instagram'}]
    preprocessed_likers = data.preprocess_media_likers(likers, 'Instagram', 123456)
    assert type(preprocessed_likers) == dict and len(preprocessed_likers) > 0
    
def test1_preprocess_media_texts():
    """
    Test to check the method which preprocesses the comments written on the medias
    of an user without providing them. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(TextListNotFound):
        assert data.preprocess_media_texts(None, None, None)

def test2_preprocess_media_texts():
    """
    Test to check the method which preprocesses the comments written on the medias
    of an user without providing the social media source. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_media_texts([1], None, None)
        
def test3_preprocess_media_texts():
    """
    Test to check the method which preprocesses the comments written on the medias
    of an user without providing a valid social media source. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_media_texts([1], 'Random', None)
        
def test4_preprocess_media_texts():
    """
    Test to check the method which preprocesses the comments written on the medias
    of an user without providing a valid user id. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(InvalidUserId):
        assert data.preprocess_media_texts([1], 'Instagram', None)

def test5_preprocess_media_texts():
    """
    Test to check the method which preprocesses the comments written on the medias
    of an user without providing a valid list of texts. An exception will be raised.
    """
    data = commondata.CommonData()
    invalid_texts = [{'id_media':134, 'user':'user1', 'social_media':'Instagram'}]
    with pytest.raises(TextDictNotFound):
        assert data.preprocess_media_texts(invalid_texts, 'Instagram', 123456)
        
def test6_preprocess_media_texts():
    """
    Test to check the method which preprocesses the comments written on the medias
    of an user without providing a valid list of texts. An exception will be raised.
    """
    data = commondata.CommonData()
    invalid_texts = [{'id_media':134, 'texts':[], 'social_media':'Instagram'}]
    with pytest.raises(TextDictNotFound):
        assert data.preprocess_media_texts(invalid_texts, 'Instagram', 123456)
        
def test7_preprocess_media_texts():
    """
    Test to check the method which preprocesses the comments written on the medias
    of an user without providing a valid list of texts. An exception will be raised.
    """
    data = commondata.CommonData()
    invalid_texts = [{'id_media':'1', 'texts':[{'user':'user1'}], 'social_media':'Instagram'}]
    with pytest.raises(TextDictNotFound):
        assert data.preprocess_media_texts(invalid_texts, 'Instagram', 123456)
        
def test8_preprocess_media_texts():
    """
    Test to check the method which preprocesses the comments written on the medias
    of an user without providing a valid list of texts. An exception will be raised.
    """
    data = commondata.CommonData()
    invalid_texts = [{'id_media':'1', 'texts':[{'user':'user1', 'text':2}], 'social_media':'Instagram'}]
    with pytest.raises(TextDictNotFound):
        assert data.preprocess_media_texts(invalid_texts, 'Instagram', 123456)

def test9_preprocess_media_texts():
    """
    Test to check the method which preprocesses the comments written on the medias
    of an user.
    """
    data = commondata.CommonData()
    text_list = [{'id_media':'1', 'texts':[{'user':'user1', 'text':'hey'}], 'social_media':'Instagram'}]
    preprocessed_texts = data.preprocess_media_texts(text_list, 'Instagram', 123456)
    assert type(preprocessed_texts) == dict 
    
def test1_preprocess_user_data():
    """
    Test to check the method which preprocesses all user data with the previous
    tested methods.
    """
    profile = {'userid':123456, 'username':'Lidia', 'social_media':'Instagram'}
    medias = [{'id_media': '1', 'title':None, 'like_count': 29, 'comment_count': 14, 'social_media':'Instagram'}, 
              {'id_media': '2', 'title':'Title 2', 'like_count': 18, 'comment_count': 0, 'social_media':'Instagram'}]
    likers = [{'id_media':'2', 'users':['user1', 'user2'], 'social_media':'Instagram'}]
    texts = [{'id_media': '1', 
              'texts': [{'user': 'user1', 'text': 'aa'}, {'user': 'user2', 'text': 'ee'}], 
              'social_media':'Instagram'},
              {'id_media': '2', 
              'texts': [{'user': 'user3', 'text': 'ii'}, {'user': 'user2', 'text': 'oo'}], 
              'social_media':'Instagram'}]
    contacts = {'followers':['user1', 'user2'], 'followings':['user1', 'user3'], 'social_media':'Instagram'}
    user_data = {'profile':profile, 'medias':medias, 'likers':likers, 
                  'texts':texts, 'contacts':contacts}
    data = commondata.CommonData()
    result = data.preprocess_user_data(user_data, 'Instagram')
    assert type(result) == dict
        
def test1_transform_text():
    """
    Test to check the method which transforms and cleans the texts from medias
    of a specific user. A list of preprocessed texts will be returned.
    """
    texts = [{'id_media': '1', 'texts': [
                      {'user': 'user1', 'text': 'Alcohollll alcohol te quiero amigo♥️'}, 
                      {'user': 'user2', 'text': '🤤🤤🤤'}], 'social_media':'Instagram'},
            {'id_media': '2', 'texts': [
                      {'user': 'user3', 'text': 'quien volviera'}, 
                      {'user': 'user2', 'text': 'Guapo 😍'}], 'social_media':'Instagram'}]
    
    data = commondata.CommonData()
    preprocessed_texts = data.transform_text(texts, 'Instagram', 123456)
    assert type(preprocessed_texts) == list
    
def test1_insert_user_data():
    """
    Test to check the method which inserts user data in a collection of a Mongo
    database without providing the data. An exception will be raised.
    """
    data = commondata.CommonData(test_collection)
    with pytest.raises(UserDataNotFound):
        assert data.insert_user_data(None, None)
        
def test2_insert_user_data():
    """
    Test to check the method which inserts user data in a collection of a Mongo
    database without providing the collection name. An exception will be raised.
    """
    data = commondata.CommonData(test_collection)
    with pytest.raises(UserDataNotFound):
        assert data.insert_user_data({123}, None)
        
def test3_insert_user_data():
    """
    Test to check the method which inserts user data in a collection of a Mongo
    database without providing the collection name. An exception will be raised.
    """
    data = commondata.CommonData(test_collection)
    with pytest.raises(CollectionNotFound):
        assert data.insert_user_data({'userid':'2'}, None)
        
def test4_insert_user_data():
    """
    Test to check the method which inserts user data in a collection of a Mongo
    database without initializing the database object. An exception will be raised.
    In order to do that, the database object will be set to None.
    """
    invalid_data = commondata.CommonData()
    with pytest.raises(InvalidMongoDbObject):
        assert invalid_data.insert_user_data({'userid':'2'}, 'test')
        
def test5_insert_user_data():
    """
    Test to check the method which inserts user data in a collection of a Mongo
    database without providing a valid query. An exception will be raised.
    """
    data = commondata.CommonData(test_collection)
    with pytest.raises(InvalidQuery):
        assert data.insert_user_data({'userid':'1'}, 'test', "")

def test6_insert_user_data():
    """
    Test to check the method which inserts user data in a collection of a Mongo
    database. In this case, there's no query to make so the new item will be inserted directly.
    """
    data = commondata.CommonData(test_collection)
    result = data.insert_user_data({'userid':'1', 'social_media':'SM'}, 'test')
    assert type(result) == str
    
def test7_insert_user_data():
    """
    Test to check the method which inserts user data in a collection of a Mongo
    database. In this case, there's a specific query to make and as a result, the
    new item won't be inserted because there are other items like it.
    """
    data = commondata.CommonData(test_collection)
    result = data.insert_user_data({'userid':'1', 'social_media':'SM'}, 'test', {'userid':'1'})
    assert result == None
    
def test8_insert_user_data():
    """
    Test to check the method which inserts user data in a collection of a Mongo
    database. In this case, there's a specific query but there are not matches
    so the new item will be inserted.
    """
    data = commondata.CommonData(test_collection)
    result = data.insert_user_data({'userid':'2', 'social_media':'SM'}, 'test', {'userid':'3'})
    assert type(result) == str

def test1_get_user_data():
    """
    Test to check the method which gets user data from a collection of a Mongo
    database specifying a query. In this case, the query is not provided so an
    exception will be raised.
    """
    data = commondata.CommonData(test_collection)
    with pytest.raises(InvalidQuery):
        assert data.get_user_data(None, None)

def test2_get_user_data():
    """
    Test to check the method which gets user data from a collection of a Mongo
    database specifying a query. In this case, the collection name is not provided so an
    exception will be raised.
    """
    data = commondata.CommonData(test_collection)
    with pytest.raises(CollectionNotFound):
        assert data.get_user_data({'userid':'2'}, None)
        
def test3_get_user_data():
    """
    Test to check the method which gets user data from a collection of a Mongo
    database specifying a query. In this case, the database object is set to None
    so an exception will be raised.
    """
    invalid_data = commondata.CommonData()
    with pytest.raises(InvalidMongoDbObject):
        assert invalid_data.get_user_data({'userid':'2'}, 'test')
        
def test4_get_user_data():
    """
    Test to check the method which gets user data from a collection of a Mongo
    database specifying a query.
    """
    data = commondata.CommonData(test_collection)
    result = data.get_user_data({'userid':'2'}, 'test')
    assert type(result) == dict and len(result) > 0
    