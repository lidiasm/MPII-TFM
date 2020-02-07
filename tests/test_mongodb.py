#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests to check the right behaviour of the methods included to the Single Source
of Truth which has the operations with the database.

@author: Lidia Sánchez Mérida.
"""

import sys
sys.path.append("src")
import os
import pytest
from exceptions import CollectionNotFound, NewItemNotFound, EmptyCollection, ItemNotFound
from mongodb import MongoDB
"""Connection to a test database with a test collection."""
testConnection = MongoDB(os.environ.get("MONGODB_URI"), 'SocialNetworksDB', 'test')

def test1_empty_collection():
    """Test to check the delete method when the collection doesn't exist. In order
        to do that we create another connection and set it to None."""
    invalidTestConnection = MongoDB(os.environ.get("MONGODB_URI"), 'SocialNetworksDB', 'test')
    invalidTestConnection.collection = None
    with pytest.raises(CollectionNotFound):
        invalidTestConnection.empty_collection()
        
def test2_empty_collection():
    """Test to check the delete method which remove the documents of the
        current collection."""
    result = testConnection.empty_collection()
    assert result.acknowledged == True
    
def test3_empty_collection():
    """Test to check the delete method when the collection is already empty."""
    with pytest.raises(EmptyCollection):
        testConnection.empty_collection()
    
def test1_insert():
    """Test to check the insert method with a valid new item."""
    data = {'id':'1', 'data':{'profile':{'username':'lidia', 'name':'lidia', 'email':'lidia@lidia.es'},
            'followers':{'1':'lucia'}, 'following':{'1':'lucia'}}}
    id_new_item = testConnection.insert(data)
    assert id_new_item != None

def test2_insert():
    """Test to check the insert method without a valid new item."""
    data = {}
    with pytest.raises(NewItemNotFound):
        testConnection.insert(data)
      
def test3_insert():
    """Test to check the insert method without a valid collection. In order to
        do that we create another connection and modify to make it invalid."""
    invalidTestConnection = MongoDB(os.environ.get("MONGODB_URI"), 'SocialNetworksDB', 'test')
    invalidTestConnection.collection = None
    data = {'id':'1', 'data':{'profile':{'username':'lidia', 'name':'lidia', 'email':'lidia@lidia.es'},
            'followers':{'1':'lucia'}, 'following':{'1':'lucia'}}}
    with pytest.raises(CollectionNotFound):
        invalidTestConnection.insert(data)

def test1_get_item():
    """Test to chech the get item method. In order to do that we insert a new item
        to get it after."""
    new_item = {'id':'2', 'data':{'profile':{'username':'mariadb', 'name':'maria', 'email':'maria@gmail.es'},
            'followers':{'1':'lidia'}, 'following':{'1':'lidia'}}}
    testConnection.insert(new_item)
    item = testConnection.get_item('id', '2')
    assert type(item) == dict
    
def test2_get_item():
    """Test to chech the get item method without a valid key."""
    item = testConnection.get_item('whatever', '2')
    assert item == None

def test3_get_item():
    """Test to chech the get item method without a valid value for the specified key."""
    item = testConnection.get_item('id', '-1')
    assert item == None
    
def test4_get_item():
    """Test to check the get item method without a valid collection. In order to
        do that we create another connection and modify to make it invalid."""
    invalidTestConnection = MongoDB(os.environ.get("MONGODB_URI"), 'SocialNetworksDB', 'test')
    invalidTestConnection.collection = None
    with pytest.raises(CollectionNotFound):
        invalidTestConnection.get_item('id', '1')

def test1_get_collection():
    """Test to check the get collection method with the current collection."""
    collection = testConnection.get_collection()
    assert type(collection) == dict

def test2_get_collection():
    """Test to check the get collection method with an empty collection. In order
        to do that we create another connection."""
    newConnection = MongoDB(os.environ.get("MONGODB_URI"), 'SocialNetworksDB', 'DB')
    with pytest.raises(EmptyCollection):
        newConnection.get_collection()

def test3_get_collection():
    """Test to check the get collection method with an invalid connection. In order
        to do that we create another connection and we set the collection None."""
    newConnection = MongoDB(os.environ.get("MONGODB_URI"), 'SocialNetworksDB', 'test')
    newConnection.collection = None
    with pytest.raises(CollectionNotFound):
        newConnection.get_collection()
    
def test1_delete_item():
    """Test to check the delete item method to remove an existing item."""
    result = testConnection.delete_item('id', '1')
    assert result.acknowledged == True 

def test2_delete_item():
    """Test to check the delete item method when the item to delete doesn't exist."""
    with pytest.raises(ItemNotFound):
        testConnection.delete_item('id', '-1')

def test3_delete_item():
    """Test to check the delete item method when the item to delete doesn't exist."""
    with pytest.raises(ItemNotFound):
        testConnection.delete_item('whatever', '1')

def test4_delete_item():
    """Test to check the delete item method when the collection doesn't exist.
        In order to do that we create another connection and set it to None."""
    newConnection = MongoDB(os.environ.get("MONGODB_URI"), 'SocialNetworksDB', 'test')
    newConnection.collection = None
    with pytest.raises(CollectionNotFound):
        newConnection.delete_item('whatever', '1')