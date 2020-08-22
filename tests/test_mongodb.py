#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests to check the right behaviour of the methods included in the Single Source
of Truth which has the operations with the MongoDB database.

@author: Lidia Sánchez Mérida.
"""
import os 
import sys
sys.path.append("src")
import pytest
from exceptions import ConnectionNotFound, CollectionNotFound, NewItemNotFound \
    , InvalidDatabaseCredentials, InvalidQuery
from mongodb import MongoDB
from datetime import date

# Connection to a test database with a test collection.
test_connection = MongoDB('test')

def test1_constructor():
    """
    Test to check the constructor of the Mongo database class without providing 
    a valid MongoDB uri. An exception will be raised.
    """
    global uri
    uri = os.environ["MONGODB_URI"]
    os.environ["MONGODB_URI"] = ""
    with pytest.raises(InvalidDatabaseCredentials):
        MongoDB("test")
        
def test2_constructor():
    """
    Test to check the constructor of the Mongo database class without providing 
    a valid collection name to connect to. An exception will be raised. Also, the
    MongoDB uri is set again.
    """
    global uri
    os.environ["MONGODB_URI"] = uri
    with pytest.raises(InvalidDatabaseCredentials):
        MongoDB(1234)

def test1_set_collection():
    """
    Test to check the set_collection method without providing a valid collection name.
    So an exception will be raised.
    """
    with pytest.raises(CollectionNotFound):
        test_connection.set_collection('')

def test2_set_collection():
    """
    Test to check the set_collection method providing a valid collection name to
    connect with. In this test, the new collection to connect with is 'test'.
    """
    new_collection = "test"
    result = test_connection.set_collection(new_collection)
    assert result.name == new_collection
        
def test1_insert_item():
    """
    Test to check the insert method without connecting to the Mongo database 
    previously. An exception will be raised. In order to do that, the connection
    attribute will be set to None.
    """
    invalid_mongodb = MongoDB('test')
    invalid_mongodb.connection = None
    with pytest.raises(ConnectionNotFound):
       invalid_mongodb.insert_item(None)
       
def test2_insert_item():
    """
    Test to check the insert method without providing a valid new item to insert
    to the current collection in the Mongo database. An exception will be raised.
    """
    with pytest.raises(NewItemNotFound):
       test_connection.insert_item(None)
       
def test3_insert_item():
    """
    Test to check the insert method without providing a valid query dict to check if the
    new element is already in the database. An exception will be raised.
    """
    data = {'id':'1', 'date':(date.today()).strftime("%d-%m-%Y"), 
            'data':{'profile':{'username':'lidia06', 'name':'lidia'},
            'followers':{'1':'lucia'}, 'following':{'1':'lucia'}}}
    with pytest.raises(InvalidQuery):
       test_connection.insert_item(data, "")
       
def test4_insert_item():
    """
    Test to check the insert method without providing a valid query dict because
    its keys are not string to check if the new element is already in the database.
    An exception will be raised.
    """
    data = {'id':'1', 'date':(date.today()).strftime("%d-%m-%Y"), 
            'data':{'profile':{'username':'lidia06', 'name':'lidia'},
            'followers':{'1':'lucia'}, 'following':{'1':'lucia'}}}
    with pytest.raises(InvalidQuery):
       test_connection.insert_item(data, {1:5})
       
def test5_insert_item():
    """
    Test to check the insert method without providing a valid query because there
    are None values to check if the new element is already in the database. 
    An exception will be raised.
    """
    data = {'id':'1', 'date':(date.today()).strftime("%d-%m-%Y"), 
            'data':{'profile':{'username':'lidia06', 'name':'lidia'},
            'followers':{'1':'lucia'}, 'following':{'1':'lucia'}}}
    with pytest.raises(InvalidQuery):
       test_connection.insert_item(data, {'id':None})

def test6_insert_item():
    """
    Test to check the insert method adding a new element to the 'test' collection.
    A string will be returned with the item id.
    """
    data = {'id':'1', 'date':(date.today()).strftime("%d-%m-%Y"), 'name':'Lidia'}
    id_new_item = test_connection.insert_item(data)
    assert type(id_new_item) == str

def test7_insert_item():
    """
    Test to check the insert method trying to add a new item which already exists
    by the specified query. So the insert method won't add the new item and None
    will be returned.
    """
    data = {'id':'1', 'date':(date.today()).strftime("%d-%m-%Y"), 'name':'Lidia'}
    query = {'id':'1'}
    id_new_item = test_connection.insert_item(data, query)
    assert id_new_item == None
    
def test8_insert_item():
    """
    Test to check the insert method adding a new item and making a query in order
    to check if there are any items which matches with the specified conditions.
    In this case there aren't, so an string with the id of the added item will be returned.
    """
    data = {'id':'2', 'date':(date.today()).strftime("%d-%m-%Y"), 'name':'Anna'}
    query = {'id':'1', 'date':'01-05-2020'}
    id_new_item = test_connection.insert_item(data, query)
    assert type(id_new_item) == str

def test1_get_records():
    """
    Test to check the get method without connecting to the Mongo database 
    previously. An exception will be raised. In order to do that, the connection
    attribute will be set to None.
    """
    invalid_mongodb = MongoDB('test')
    invalid_mongodb.connection = None
    with pytest.raises(ConnectionNotFound):
       invalid_mongodb.get_records(None)
       
def test2_get_records():
    """
    Test to check the get method without providing a valid query, so an exception
    will be raised.
    """
    with pytest.raises(InvalidQuery):
       test_connection.get_records(None)
       
def test3_get_records():
    """
    Test to check the get method without providing a valid query whose keys are strings
    and there are not None values. An exception will be raised.
    """
    with pytest.raises(InvalidQuery):
       test_connection.get_records({'id':None})
       
def test4_get_records():
    """
    Test to check the get method getting the records related to the specified query.
    A dict will be returned with the matched items. In this test, we will search
    for the id of a previously added item in previous tests.
    """
    matched_items = test_connection.get_records({'id':'1'})
    assert type(matched_items) == dict and len(matched_items) > 0
    
def test5_get_records():
    """
    Test to check the get method getting all the documents of the current collection
    named 'test'. In order to do that, the query is not specified.
    """
    matched_items = test_connection.get_records()
    assert type(matched_items) == dict and len(matched_items) > 0

def test1_collection_size():
    """
    Test to check the method which returns the number of documents which are
    contained in the current collection.
    """
    assert type(test_connection.collection_size()) == int
    
def test1_delete_records():
    """
    Test to check the dekete method without connecting to the Mongo database 
    previously. An exception will be raised. In order to do that, the connection
    attribute will be set to None.
    """
    invalid_mongodb = MongoDB('test')
    invalid_mongodb.connection = None
    with pytest.raises(ConnectionNotFound):
       invalid_mongodb.delete_records(None)
       
def test2_delete_records():
    """
    Test to check the delete method without providing a valid query, so an exception
    will be raised.
    """
    with pytest.raises(InvalidQuery):
       test_connection.delete_records(None)
       
def test3_delete_records():
    """
    Test to check the delete method without providing a valid query whose keys are strings
    and there are not None values. An exception will be raised.
    """
    with pytest.raises(InvalidQuery):
       test_connection.delete_records({'id':None})
       
def test4_delete_records():
    """
    Test to check the delete method removing the records related to the specified query.
    In this test, we will search for the id of a previously added item in previous tests.
    """
    deleted_items = test_connection.delete_records({'id':'1'})
    assert type(deleted_items) == int and deleted_items > 0
    
def test5_delete_records():
    """
    Test to check the delete method getting all the documents of the current collection
    named 'test'. In order to do that, the query is not specified.
    """
    test_connection.delete_records()
    current_size = test_connection.collection_size()
    assert current_size == 0
