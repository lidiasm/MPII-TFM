#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which represents the Single Source of Truth which contains the methods
to do things with the database. This common class could be used for all classes
of the project.

@author: Lidia Sánchez Mérida.
"""

import pymongo
import sys
sys.path.append('src/exceptions')
from exceptions import CollectionNotFound, NewItemNotFound, EmptyCollection, ItemNotFound

class MongoDB:
    
    def __init__(self, uri, db, collection):
        """Creates a new MongoDB client to access a specific collection."""
        self.client = pymongo.MongoClient(uri)
        self.collection = self.client[db][collection]
    
    def insert(self, new_item):
        """Check the connection to the database and the new element."""
        if (self.collection == None or self.client == None):
            raise CollectionNotFound("There's no connection to the database.")
        if (new_item == None or len(new_item) == 0):
            raise NewItemNotFound("The new item doesn't exist.")
        """Insert the new element if it's not already in the database."""
        if (self.get_item('id', new_item['id']) == None):
            id_new_item = self.collection.insert_one(new_item.copy()).inserted_id
            return str(id_new_item)
            
    def get_item(self, key, value):
        """Check the connection to the database."""
        if (self.collection == None or self.client == None):
            raise CollectionNotFound("There's no connection to the database.")
        """Return the item if the key exists."""
        item = self.collection.find_one({key:value})
        """Transform the id of the database to string."""
        if (item != None): item['_id'] = str(item['_id'])
        return item
    
    def get_collection(self):
        """Check the connection to the database."""
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
    
    def delete_item(self, key, value):
        """Check the connection to the database."""
        if (self.collection == None or self.client == None):
            raise CollectionNotFound("There's no connection to the database.")
        """Delete the item."""
        result = self.collection.delete_one({key:value})
        if (result.deleted_count == 0): raise ItemNotFound("The item doesn't exist.")
        return result
    
    def empty_collection(self):
        """Check the connection to the database."""
        if (self.collection == None or self.client == None):
            raise CollectionNotFound("There's no connection to the database.")
        """Delete the documents of the collection, not the collection itself."""
        result = self.collection.delete_many({})
        if (result.deleted_count == 0): raise EmptyCollection('The collection is already empty.')
        return result

    def collection_size(self):
        """Return the size of the collection."""
        return self.collection.count_documents({})