#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests to check the right behaviour of the methods included in the Single Source
of Truth which has the operations with the MongoDB database.

@author: Lidia Sánchez Mérida.
"""
from datetime import datetime
import os 
import sys
sys.path.append("src")
import pytest
from exceptions import ConnectionNotFound, CollectionNotFound \
    , InvalidDatabaseCredentials, InvalidQuery, InvalidQueryValues, NewItemNotFound
from mongodb import MongoDB

# Connection to a test database with a test collection.
test_connection = MongoDB('test')

def test1_constructor():
    """
    Test to check the constructor which creates a MongoDB object without 
    providing a valid MongoDB URI, so an exception will be raised.
    """
    global uri
    uri = os.environ["MONGODB_URI"]
    os.environ["MONGODB_URI"] = ""
    with pytest.raises(InvalidDatabaseCredentials):
        MongoDB("test")
        
def test2_constructor():
    """
    Test to check the constructor which creates a MongoDB object without providing 
    a valid collection name to connect to so an exception will be raised. 
    The MongoDB URI is also set again.
    """
    global uri
    os.environ["MONGODB_URI"] = uri
    with pytest.raises(InvalidDatabaseCredentials):
        MongoDB(1234)

def test1_set_collection():
    """
    Test to check the method which connects to the specified collection in the
    Mongo database. In this test, the provided collection name is not valid so
    an exception will be raised.
    """
    with pytest.raises(CollectionNotFound):
        test_connection.set_collection('')

def test2_set_collection():
    """
    Test to check the method which connects to the specified collection in the
    Mongo database. In this test, the collection to connect with is 'test'
    """
    new_collection = "test"
    result = test_connection.set_collection(new_collection)
    assert result.name == new_collection
    
def test1_insert_item():
    """
    Test to check the method which inserts a new item into a specific collection
    contained in the Mongo database. In this test, the connection to the database
    has not been made so an exception will be raised.
    """
    invalid_mongodb = MongoDB('test')
    invalid_mongodb.connection = None
    with pytest.raises(ConnectionNotFound):
        invalid_mongodb.insert_item(None)
       
def test2_insert_item():
    """
    Test to check the method which inserts a new item into a specific collection
    contained in the Mongo database. In this test, the query to make is not 
    provided so an exception will be raised.
    """
    with pytest.raises(NewItemNotFound):
        test_connection.insert_item(None)
       
def test3_insert_item():
    """
    Test to check the method which inserts a new item into a specific collection
    contained in the Mongo database. In this test, the new item does not already
    exist so it will be inserted.
    """
    values = {"username" : "first user", "field_one" : "anything", 
              "date" : datetime.strptime("25-10-2020", "%d-%m-%Y"),
              "social_media" : "Instagram"}
    result = test_connection.insert_item(values)
    assert type(result) == str
    
def test4_insert_item():
    """
    Test to check the method which inserts a new item into a specific collection
    contained in the Mongo database. In this test, the new item already exists
    so it won't be inserted.
    """
    values = {"username" : "first user", "field_one" : "anything", 
              "date" : datetime.strptime("25-10-2020", "%d-%m-%Y"), 
              "social_media" : "Instagram"}
    result = test_connection.insert_item(values)
    assert result == None
    
def test1_get_records():
    """
    Test to check the method which gets data from a specific collection in the
    Mongo database. In this test, the connection to the database hasn't been
    made so an exception will be raised.
    """
    invalid_mongodb = MongoDB('test')
    invalid_mongodb.connection = None
    with pytest.raises(ConnectionNotFound):
        invalid_mongodb.get_records(None)
       
def test2_get_records():
    """
    Test to check the method which gets data from a specific collection in the
    Mongo database. In this test, the query to make is not provided so an 
    exception will be raised.
    """
    with pytest.raises(InvalidQuery):
        test_connection.get_records(None)
       
def test3_get_records():
    """
    Test to check the method which gets data from a specific collection in the
    Mongo database. In this test, the provided query to make is not valid so an 
    exception will be raised.
    """
    with pytest.raises(InvalidQuery):
        test_connection.get_records("invalid_query")
       
def test4_get_records():
    """
    Test to check the method which gets data from a specific collection in the
    Mongo database. In this test, the specified query needs some values which
    are not provided so an exception will be raised.
    """
    with pytest.raises(InvalidQueryValues):
        test_connection.get_records("get_test")
       
def test5_get_records():
    """
    Test to check the method which gets data from a specific collection in the
    Mongo database. In this test, the required values to make the query are not
    provided so an exception will be raised.
    """
    values = {"username":"user"}
    with pytest.raises(InvalidQueryValues):
        test_connection.get_records("get_test", values)

def test6_get_records():
    """
    Test to check the method which gets data from a specific collection in the
    Mongo database. In this test, the main goal is to get only the 'date' key
    from the 'test' collection.
    """
    # Delete the collection previously
    new_item1 = {"username" : "first user", "field_one" : "anything", 
              "date" : "26-10-2020", "social_media" : "Instagram"}
    test_connection.insert_item(new_item1)
    new_item2 = {"username" : "first user", "field_one" : "anything", 
                 "date" : "27-10-2020", "social_media" : "Instagram"}
    test_connection.insert_item(new_item2)
    new_item3 = {"username" : "first user", "field_one" : "anything", 
                 "date" : "28-10-2020", "social_media" : "Instagram"}
    test_connection.insert_item(new_item3)
    records = test_connection.get_records("get_dates")       
    assert type(records) == list and len(records) > 0
    
def test7_get_records():
    """
    Test to check the method which gets data from a specific collection in the
    Mongo database. 
    """
    values = {"username":"first user", "date_ini":"25-10-2020", 
              "date_fin":"27-10-2020", "social_media":"Instagram"}
    records = test_connection.get_records("get_test", values)
    assert type(records) == list and len(records) == 1

def test1_collection_size():
    """
    Test to check the method which returns the number of documents which are
    contained in the current collection.
    """
    assert type(test_connection.collection_size()) == int
    
def test1_delete_records():
    """
    Test to check the method which gets data from a specific collection in the
    Mongo database. In this test, the connection to the database hasn't been
    made so an exception will be raised.
    """
    invalid_mongodb = MongoDB('test')
    invalid_mongodb.connection = None
    with pytest.raises(ConnectionNotFound):
        invalid_mongodb.delete_records(None)
       
def test2_delete_records():
    """
    Test to check the method which gets data from a specific collection in the
    Mongo database. In this test, the query to make is not provided so an 
    exception will be raised.
    """
    with pytest.raises(InvalidQuery):
        test_connection.delete_records(None)
       
def test3_delete_records():
    """
    Test to check the method which gets data from a specific collection in the
    Mongo database. In this test, the provided query to make is not valid so an 
    exception will be raised.
    """
    with pytest.raises(InvalidQuery):
        test_connection.delete_records("invalid_query")
       
def test4_delete_records():
    """
    Test to check the method which gets data from a specific collection in the
    Mongo database. In this test, the specified query needs some values which
    are not provided so an exception will be raised.
    """
    with pytest.raises(InvalidQueryValues):
        test_connection.delete_records("delete_item")
       
def test5_delete_records():
    """
    Test to check the method which gets data from a specific collection in the
    Mongo database. In this test, the required values to make the query are not
    provided so an exception will be raised.
    """
    values = {"username":"user 1"}
    with pytest.raises(InvalidQueryValues):
        test_connection.delete_records("delete_item", values)
        
def test6_delete_records():
    """
    Test to check the method which gets data from a specific collection in the
    Mongo database. In this test, the required values to make the query are not
    provided so an exception will be raised.
    """
    values = {"username":"first user", "date" : "25-10-2020",
              "social_media":"Instagram"}
    result = test_connection.delete_records("delete_item", values)
    assert result == 1
        
def test7_delete_records():
    """
    Test to check the method which gets data from a specific collection in the
    Mongo database. In this test, the required values to make the query are not
    provided so an exception will be raised.
    """
    test_connection.delete_records("delete_all")
    current_size = test_connection.collection_size()
    assert current_size == 0