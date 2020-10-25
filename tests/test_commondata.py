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
from exceptions import InvalidMongoDbObject, ProfileDictNotFound, InvalidTextList \
    , ContactDictNotFound, MediaListNotFound, MediaDictNotFound, LikerListNotFound \
    , TextListNotFound, TextDictNotFound, UserDataNotFound, CollectionNotFound \
    , InvalidQuery, InvalidSocialMediaSource, InvalidUserId, InvalidMediaId, LikerDictNotFound
    
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
    providing all the required values. It'll raise an exception.
    """
    profile = {'name':'Lidia'}
    data = commondata.CommonData()
    with pytest.raises(ProfileDictNotFound):
        assert data.preprocess_profile(profile, None)
        
def test3_preprocess_profile():
    """
    Test to check the method which preprocesses the user profile without 
    providing a valid social media source. It'll raise an exception.
    """
    profile = {'userid':123456, 'username':'lidia06', 'name':'Lidia', 'biography':None, 
               'gender':None, 'profile_pic':None, 'location':'Granada', 'birthday':None, 
               'date_joined':None, 'n_followers':123, 'n_followings':452, 'n_medias':45}
    data = commondata.CommonData()
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_profile(profile, None)

def test4_preprocess_profile():
    """
    Test to check the method which preprocesses the user profile without 
    providing a valid social media source. It'll raise an exception.
    """
    profile = {'userid':123456, 'username':'lidia06', 'name':'Lidia', 'biography':None, 
               'gender':None, 'profile_pic':None, 'location':'Granada', 'birthday':None, 
               'date_joined':None, 'n_followers':123, 'n_followings':452, 'n_medias':45}
    data = commondata.CommonData()
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_profile(profile, "Random Social Media")
        
def test5_preprocess_profile():
    """
    Test to check the method which preprocesses the user profile without 
    providing a valid user id, so an exception will be raised.
    """
    profile = {'userid':-5, 'username':'lidia06', 'name':'Lidia', 'biography':None, 
               'gender':None, 'profile_pic':None, 'location':'Granada', 'birthday':None, 
               'date_joined':None, 'n_followers':123, 'n_followings':452, 'n_medias':45}
    data = commondata.CommonData()
    with pytest.raises(InvalidUserId):
        assert data.preprocess_profile(profile, "Instagram")
        
def test6_preprocess_profile():
    """
    Test to check the method which preprocesses the user profile in which there
    are some 'None' values. These will be transform to strings. All the preprocessed values will be strings.
    """
    profile = {'userid':123456, 'username':'lidia06', 'name':'Lidia', 'biography':None, 
               'gender':None, 'profile_pic':None, 'location':'Granada', 'birthday':None, 
               'date_joined':None, 'n_followers':123, 'n_followings':452, 'n_medias':45}
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
    a specific user. All the preprocessed values will be strings.
    """
    data = commondata.CommonData()
    contacts = {'followers':[1, 'user1', 'user2', 'user3'], 
                'followings':['user1',' user2', 4, 5]}
    preprocessed_contacts = data.preprocess_contacts(contacts, "Instagram", '123456')
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
    with pytest.raises(MediaDictNotFound):
        assert data.preprocess_medias([1,2,3,4], None, None)
        
def test3_preprocess_medias():
    """
    Test to check the method which preprocesses the medias of a specific user
    without providing the social media source. An exception will be raised.
    """
    data = commondata.CommonData()
    medias = [{"id_media":1, "like_count":54, "comment_count":5}]
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_medias(medias, '', None)

def test4_preprocess_medias():
    """
    Test to check the method which preprocesses the medias of a specific user
    without providing a valid social media source. An exception will be raised.
    """
    data = commondata.CommonData()
    medias = [{"id_media":1, "like_count":54, "comment_count":5}]
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_medias(medias, 'Random', None)

def test5_preprocess_medias():
    """
    Test to check the method which preprocesses the medias of a specific user
    without providing a valid user id. An exception will be raised.
    """
    data = commondata.CommonData()
    medias = [{"id_media":1, "like_count":54, "comment_count":5}]
    with pytest.raises(InvalidUserId):
        assert data.preprocess_medias(medias, 'Instagram', None)
        
def test6_preprocess_medias():
    """
    Test to check the method which preprocesses the medias of a specific user
    without providing the required keys for the dict of medias. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(MediaDictNotFound):
        assert data.preprocess_medias([{'id_media':'1', 'title':''}], 'Instagram', '123456')

def test7_preprocess_medias():
    """
    Test to check the method which preprocesses the medias of a specific user
    without providing their valid user id. An exception will be raised.
    """
    data = commondata.CommonData()
    medias = [{"id_media":1, "like_count":54, "comment_count":5}]
    with pytest.raises(InvalidUserId):
        assert data.preprocess_medias(medias, 'Instagram', 23456)

def test8_preprocess_medias():
    """
    Test to check the method which preprocesses the medias of a specific user
    without providing valid media ids, so an exception will be raised.
    """
    data = commondata.CommonData()
    medias = [{"id_media":-1, "like_count":54, "comment_count":5}]
    with pytest.raises(InvalidMediaId):
        assert data.preprocess_medias(medias, 'Instagram', '23456')
                
def test9_preprocess_medias():
    """
    Test to check the method which preprocesses the medias of a specific user.
    In the provided data, there are some None values that will be replaced by
    its string way 'None'. All the preprocessed values will be strings.
    """                    
    data = commondata.CommonData()
    medias = [
        {"id_media":'123', "like_count":54, "comment_count":5},
        {"id_media":'456', "like_count":35, "comment_count":128},
        {"id_media":'789', "like_count":15, "comment_count":1}
        ]
    preprocessed_medias = data.preprocess_medias(medias, 'Instagram', '123456')
    check = []
    for record in preprocessed_medias['medias']:
        check.append(True if all(isinstance(item, str) for item in list(record.values())) else False)
 
    assert len(list(set(check))) == 1 and list(set(check))[0] == True

def test1_preprocess_media_likers():
    """
    Test to check the method which preprocesses the list of people who liked
    the medias of a specific user without providing any data. An exception will
    be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(LikerListNotFound):
        assert data.preprocess_media_likers({}, None, None)

def test2_preprocess_media_likers():
    """
    Test to check the method which preprocesses the list of people who liked
    the medias of a specific user without providing a valid list of media likers,
    so an exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(LikerListNotFound):
        assert data.preprocess_media_likers([1,2,3,4], None, None)
        
def test3_preprocess_media_likers():
    """
    Test to check the method which preprocesses the list of people who liked
    the medias of a specific user without providing the social media source. 
    An exception will be raised.
    """
    data = commondata.CommonData()
    likers = [{"id_media":1, "users":[]}]
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_media_likers(likers, '', None)

def test4_preprocess_media_likers():
    """
    Test to check the method which preprocesses the list of people who liked
    the medias of a specific user without providing a valid social media source. 
    An exception will be raised.
    """
    data = commondata.CommonData()
    likers = [{"id_media":1, "users":[]}]
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_media_likers(likers, 'Random', None)

def test5_preprocess_media_likers():
    """
    Test to check the method which preprocesses the list of people who liked
    the medias of a specific user without providing a valid user id. 
    An exception will be raised.
    """
    data = commondata.CommonData()
    likers = [{"id_media":1, "users":[]}]
    with pytest.raises(InvalidUserId):
        assert data.preprocess_media_likers(likers, 'Instagram', None)
        
def test6_preprocess_media_likers():
    """
    Test to check the method which preprocesses the list of people who liked
    the medias of a specific user without providing the required keys for the liker
    dict. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(LikerDictNotFound):
        assert data.preprocess_media_likers([{'id_media':'1'}], 'Instagram', '123456')

def test7_preprocess_media_likers():
    """
    Test to check the method which preprocesses the list of people who liked
    the medias of a specific user without providing a valid media id for each list
    of likers. An exception will be raised.
    """
    data = commondata.CommonData()
    likers = [{"id_media":-1, "users":['user1', 'user2', 'user3']}]
    with pytest.raises(InvalidMediaId):
        assert data.preprocess_media_likers(likers, 'Instagram', '23456')

def test8_preprocess_media_likers():
    """
    Test to check the method which preprocesses the list of people who liked
    the medias of a specific user without providing a valid media id for each list
    of likers. An exception will be raised.
    """
    data = commondata.CommonData()
    likers = [{"id_media":'1', "users":123456}]
    with pytest.raises(LikerListNotFound):
        assert data.preprocess_media_likers(likers, 'Instagram', '23456')

def test9_preprocess_media_likers():
    """
    Test to check the method which preprocesses the list of people who liked
    the medias of a specific user. All the preprocessed values will be strings.
    """
    data = commondata.CommonData()
    likers = [{"id_media":'1', "users":['user1', 5, 'user2', True, 'user3']}]
    preprocessed_likers = data.preprocess_media_likers(likers, 'Instagram', '23456')
    check = []
    for record in preprocessed_likers['likers']:
        check.append(True if type(record['id_media']) == str else False)
        for user in record['users']:
            check.append(True if type(user) == str else False)
            
    assert len(list(set(check))) == 1 and list(set(check))[0] == True

def test1_preprocess_media_comments():
    """
    Test to check the method which preprocesses the comments wrote on the posts
    of a specific user without providing any data. An exception will
    be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(TextListNotFound):
        assert data.preprocess_media_comments({}, None, None)

def test2_preprocess_media_comments():
    """
    Test to check the method which preprocesses the comments wrote on the posts
    of a specific user without providing a valid list of media texts,
    so an exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(TextListNotFound):
        assert data.preprocess_media_comments([1,2,3,4], None, None)
        
def test3_preprocess_media_comments():
    """
    Test to check the method which preprocesses the comments wrote on the posts
    of a specific user without providing the social media source. 
    An exception will be raised.
    """
    data = commondata.CommonData()
    texts = [{"id_media":1, "texts":{}}]
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_media_comments(texts, '', None)

def test4_preprocess_media_comments():
    """
    Test to check the method which preprocesses the comments wrote on the posts
    of a specific user without providing a valid social media source. 
    An exception will be raised.
    """
    data = commondata.CommonData()
    texts = [{"id_media":1, "texts":[]}]
    with pytest.raises(InvalidSocialMediaSource):
        assert data.preprocess_media_comments(texts, 'Random', None)

def test5_preprocess_media_comments():
    """
    Test to check the method which preprocesses the comments wrote on the posts
    of a specific user without providing a valid user id. 
    An exception will be raised.
    """
    data = commondata.CommonData()
    texts = [{"id_media":1, "texts":[]}]
    with pytest.raises(InvalidUserId):
        assert data.preprocess_media_comments(texts, 'Instagram', None)
        
def test6_preprocess_media_comments():
    """
    Test to check the method which preprocesses the comments wrote on the posts
    of a specific user without providing the required keys for the text
    dict. An exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(TextDictNotFound):
        assert data.preprocess_media_comments([{'id_media':'1'}], 'Instagram', '123456')

def test7_preprocess_media_comments():
    """
    Test to check the method which preprocesses the comments wrote on the posts
    of a specific user without providing a valid media id for each list
    of texts. An exception will be raised.
    """
    data = commondata.CommonData()
    texts = [{"id_media":-1, "texts":[{'user1':'Text from user1', 'user2':'Text from user2'}]}]
    with pytest.raises(InvalidMediaId):
        assert data.preprocess_media_comments(texts, 'Instagram', '23456')

def test8_preprocess_media_comments():
    """
    Test to check the method which preprocesses the comments wrote on the posts
    of a specific user without providing a valid list of texts. An exception will
    be raised.
    """
    data = commondata.CommonData()
    texts = [{"id_media":'1', "texts":{}}]
    with pytest.raises(TextListNotFound):
        assert data.preprocess_media_comments(texts, 'Instagram', '23456')

def test9_preprocess_media_comments():
    """
    Test to check the method which preprocesses the comments wrote on the posts
    of a specific user without providing a valid list of texts. An exception will
    be raised.
    """
    data = commondata.CommonData()
    texts = [{"id_media":'1', "texts":[1,2]}]
    with pytest.raises(TextListNotFound):
        assert data.preprocess_media_comments(texts, 'Instagram', '23456')
        
def test10_preprocess_media_comments():
    """
    Test to check the method which preprocesses the comments wrote on the posts
    of a specific user without providing a valid all required keys. An exception
    will be raised.
    """
    data = commondata.CommonData()
    texts = [{"id_media":'1', "texts":[{'user':'user1', 'text':'text', 'id':55}]}]
    with pytest.raises(TextDictNotFound):
        assert data.preprocess_media_comments(texts, 'Instagram', '23456')

def test11_preprocess_media_comments():
    """
    Test to check the method which preprocesses the comments wrote on the posts
    of a specific user. All the preprocessed values will be strings.
    """
    data = commondata.CommonData()
    texts = [{"id_media":'1', "texts":[{'user':'user1', 'text':'Text from user1'}, 
                                       {'user':'user2', 'text':'Text from user2'},
                                       {'user':5, 'text':'Text from user3'}]
              }]
    preprocessed_texts = data.preprocess_media_comments(texts, 'Instagram', '23456')
    check = []
    for record in preprocessed_texts['comments']:
        check.append(True if type(record['id_media']) == str else False)
        for text_record in record['texts']:
            text_keys = list(text_record.keys())
            text_values = list(text_record.values())
            check.append(True if all(isinstance(key, str) for key in text_keys) and \
                         all (isinstance(value, str) for value in text_values) else False)
            
    assert len(list(set(check))) == 1 and list(set(check))[0] == True

def test1_preprocess_user_data():
    """
    Test to check the method which preprocesses all user data with the previous
    tested methods.
    """
    profile = {'userid':123456, 'username':'lidia06', 'name':'Lidia', 'biography':None, 
               'gender':None, 'profile_pic':None, 'location':'Granada', 'birthday':None, 
               'date_joined':None, 'n_followers':123, 'n_followings':452, 'n_medias':45}
    contacts = {'followers':[1, 'user1', 'user2', 'user3'], 
                'followings':['user1',' user2', 4, 5]}
    medias = [
        {"id_media":'123', "like_count":54, "comment_count":5},
        {"id_media":'456', "like_count":35, "comment_count":128},
        {"id_media":'789', "like_count":15, "comment_count":1}
        ]
    likers = [{"id_media":'1', "users":['user1', 5, 'user2', True, 'user3']}]
    comments = [{"id_media":'1', "texts":[{'user':'user1', 'text':'Text from user1'}, 
                                       {'user':'user2', 'text':'Text from user2'},
                                       {'user':5, 'text':'Text from user3'}]
              }]
    user_data = {'profile':profile, 'medias':medias, 'likers':likers, 
                  'comments':comments, 'contacts':contacts}
    data = commondata.CommonData()
    result = data.preprocess_user_data(user_data, 'Instagram')
    assert type(result) == dict

def test1_clean_texts():
    """
    Test to check the method which cleans a list of texts in order to delete the
    useless characters. In this test, the list of texts is not provided so an exception
    will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(TextListNotFound):
        assert data.clean_texts({})

def test2_clean_texts():
    """
    Test to check the method which cleans a list of texts in order to delete the
    useless characters. In this test, the provided list of texts is not valid so
    an exception will be raised.
    """
    data = commondata.CommonData()
    with pytest.raises(InvalidTextList):
        assert data.clean_texts(['text1', 'text2', 4, True])
        
def test3_clean_texts():
    """
    Test to check the method which cleans a list of texts in order to delete the
    useless characters.
    """
    data = commondata.CommonData()
    text_list = ['Alcohollll alcohol te quiero amigo♥️',
                 '🤤🤤🤤',
                 'quien volviera',
                 'Guapo 😍'
                 ]
    cleaned_texts = data.clean_texts(text_list)
    assert len(cleaned_texts) == len(text_list)
        
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
    