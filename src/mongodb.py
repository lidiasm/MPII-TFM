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
from datetime import date

class MongoDB:
    
    def __init__(self, uri, db, collection):
        """Creates a new MongoDB client to access a specific collection."""
        self.client = pymongo.MongoClient(uri)
        self.collection = self.client[db][collection]
    
    def insert(self, new_item):
        """Inserts a new element into the specified collection, if the user data
            don't already exist in the same date."""
        if (self.collection == None or self.client == None):
            raise CollectionNotFound("There's no connection to the database.")
        if (new_item == None or len(new_item) == 0):
            raise NewItemNotFound("The new item doesn't exist.")
        
        """Insert the new element if it's not already in the collection. If it
            is, new data from the user can't be inserted in the same day."""
        items = self.get_item_records('id', new_item['id'])
        if (items == None or str(date.today()) not in items):
            id_new_item = self.collection.insert_one(new_item.copy()).inserted_id
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