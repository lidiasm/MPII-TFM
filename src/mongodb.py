#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which represents the Single Source of Truth and contains the requested
operations to work with a MongoDB database. 

This class will be used for all the classes which need to operate with the 
MongoDB database.

@author: Lidia Sánchez Mérida.
"""
import os
import pymongo
import sys
sys.path.append('src/exceptions')
from exceptions import CollectionNotFound, NewItemNotFound, EmptyCollection, ItemNotFound, InvalidDatabaseCredentials
from datetime import date

class MongoDB:
    
    def __init__(self, collection):
        """MongoDB constructor. It creates an object whose attributes are:
            - The name of the database.
            - The Mongo database credentials.
            - The collection to connect to.
        """
        if (type(collection) != str or collection == ""):
            raise InvalidDatabaseCredentials("ERROR. The collection name to connect to should be a non-empty string.")
        uri = os.environ.get("MONGODB_URI")
        if (type(uri) != str or uri == ""):
            raise InvalidDatabaseCredentials("ERROR. The MongoDB uri should be a non-empty string stored as a env variable.")
        self.client = pymongo.MongoClient(uri)
        self.db = "SocialNetworksDB"
        self.collection = self.client[self.db][collection]
        
    def set_collection(self, new_collection):
        """Sets a new collection."""
        if (new_collection == None or new_collection == "" or type(new_collection) != str):
            raise CollectionNotFound("ERROR. Invalid collection name.")
        self.collection = self.client[self.db][new_collection]
        
        return self.collection
    
    def insert(self, new_item):
        """Inserts a new element into the specified collection, if the user data
            don't already exist in the same date."""
        if (self.collection == None or self.client == None):
            raise CollectionNotFound("There's no connection to the database.")
        if (new_item == None or len(new_item) == 0):
            raise NewItemNotFound("The new item doesn't exist.")
            
        """Search for user data in the same date in order to not insert the new data."""
        items = self.get_item_records('id', new_item['id'])
        item_exists = False
        today_date = (date.today()).strftime("%d-%m-%Y")
        for item in items:
            if (items[item]['id'] == new_item['id'] and items[item]['date'] == today_date):
                item_exists = True
                break
        
        if (items == None or not item_exists):
            id_new_item = self.collection.insert_one(new_item.copy(), bypass_document_validation=True).inserted_id
            return str(id_new_item)
    
    def get_item_records(self, key, value):
        """Gets the all records of an user."""
        if (self.collection == None or self.client == None):
            raise CollectionNotFound("There's no connection to the database.")
        """Return the rows related to an item."""
        item_rows = self.collection.find({key:value})
        documents = {}
        document_index = 0
        for item_r in item_rows:
            """Transform the id from the database to string."""
            item_r['_id'] = str(item_r['_id'])
            documents[document_index] = item_r
            document_index += 1
        return documents
    
    def delete_item_records(self, key, value):
        """Check the connection to the database."""
        if (self.collection == None or self.client == None):
            raise CollectionNotFound("There's no connection to the database.")
        """Delete the item."""
        result = self.collection.delete_many({key:value})
        if (result.deleted_count == 0): raise ItemNotFound("The item doesn't exist.")
        return result
        
    def get_collection(self):
        """Gets all records of a collection."""
        if (self.collection == None or self.client == None):
            raise CollectionNotFound("There's no connection to the database.")
        """Go down the documents of the collection."""
        documents = {}
        document_index = 0
        items = (self.collection).find({})
        for item in items:
            """Transform the id from the database to string."""
            item['_id'] = str(item['_id'])
            documents[document_index] = item
            document_index += 1

        if (len(documents) == 0): raise EmptyCollection('The collection is empty.')
        return documents
    
    def empty_collection(self):
        """Deletes all records of a collection."""
        if (self.collection == None or self.client == None):
            raise CollectionNotFound("There's no connection to the database.")
        """Delete the documents of the collection, not the collection itself."""
        result = self.collection.delete_many({})
        if (result.deleted_count == 0): raise EmptyCollection('The collection is already empty.')
        return result

    def collection_size(self):
        """Returns the size of a collection."""
        return self.collection.count_documents({})