#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which represents the Single Source of Truth and contains the required
operations to work with a Mongo database. This class will be used for all the
classes which need to operate with the Mongo database.

@author: Lidia Sánchez Mérida.
"""
import os
import pymongo
import sys
sys.path.append('src/exceptions')
from exceptions import ConnectionNotFound, CollectionNotFound, NewItemNotFound \
    , InvalidDatabaseCredentials, InvalidQuery

class MongoDB:
    
    def __init__(self, collection):
        """
        Creates a MongoDB object whose attributes are:
            - The name of the database to connect with.
            - The Mongo database URI and credentials.
            - The connection to the specified collection in the Mongo database.

        Parameters
        ----------
        collection : str.
            The collection name to connect to in the Mongo database.

        Raises
        ------
        InvalidDatabaseCredentials
            If the provided URI or collection name to connect to in the Mongo database
            are wrong.

        Returns
        -------
        A MongoDB object with the connection made to the database.
        """
        if (type(collection) != str or collection == ""):
            raise InvalidDatabaseCredentials("ERROR. The collection name to connect to should be a non-empty string.")
        uri = os.environ.get("MONGODB_URI")
        if (type(uri) != str or uri == ""):
            raise InvalidDatabaseCredentials("ERROR. The MongoDB uri should be a non-empty string stored as a env variable.")
        # Connection
        self.client = pymongo.MongoClient(uri)
        self.db = "socialnetworksdb"
        self.connection = self.client[self.db][collection]
        
    def set_collection(self, new_collection):
        """
        Sets a new collection name to connect with in the Mongo database.

        Parameters
        ----------
        new_collection : str
            The new collection name to connect with.

        Raises
        ------
        CollectionNotFound
            If the provided collection name is not a non-empty string.

        Returns
        -------
        The connection made to the new collection in the Mongo database.
        """
        if (type(new_collection) != str or new_collection == ""):
            raise CollectionNotFound("ERROR. Invalid collection name.")
            
        self.connection = self.client[self.db][new_collection]
        return self.connection
    
    def get_records(self, query={}):
        """
        Gets the records related to the specified query. If there is not provided
        query, then all the documents of the current collection will be returned.

        Parameters
        ----------
        query : dict
            It's a dict whose keys are the fields in which the method will search
            and the values are the values to search for in the current collection
            in the Mongo database.
            If the dict is empty, the entire collection will be returned.

        Raises
        ------
        CollectionNotFound
            If the connection has not been made.

        Returns
        -------
        The matched records related to the specified query.
        """
        if (type(self.connection) != pymongo.collection.Collection):
            raise ConnectionNotFound("ERROR. There is not connection to the database.")
        # Check the provided query
        if (type(query) != dict):
            raise InvalidQuery("ERROR. The query should be a dict.")
        # Check the keys are string and the values exist
        if (len(query) > 0):
            if (not all(isinstance(key,str) for key in query) or None in query.values()):
                raise InvalidQuery("ERROR. The query should have string keys and non-None values.")
            
        # Make the query
        item_rows = self.connection.find(query)
        documents = {}
        document_index = 0
        for item_r in item_rows:
            # Transform the id from the database to string.
            item_r['_id'] = str(item_r['_id'])
            documents[document_index] = item_r
            document_index += 1
            
        return documents
    
    def insert_item(self, new_item, query=None):
        """
        Adds a new item to the current collection in the Mongo database, if 
        the PK is different (id, date).

        Parameters
        ----------
        new_item : dict
            It's a dict with the new data to insert to the current collection in the
            Mongo database. The keys should be non-empty strings and it can't contain
            None values.
        query : dict
            It's a dict which could contain the query to make in order to check
            if the new item already exists in the Mongo database. The keys should be non-empty strings and it can't contain
            None values.
            If it's None, then not checking will be done and the new item will
            be always inserted.

        Raises
        ------
        CollectionNotFound
            If the connection to the Mongo database has not been made.
        NewItemNotFound
            If the new item to insert does not exist.

        Returns
        -------
        A string which represents the id of the new added item.
        None if it hasn't been inserted.
        """
        items = {}
        if (type(self.connection) != pymongo.collection.Collection):
            raise ConnectionNotFound("ERROR. There is not connection to the database.")
        if (type(new_item) != dict or len(new_item) == 0):
            raise NewItemNotFound("ERROR. The new item does not exist.")
        # Check the provided query
        if (query != None):
            if (type(query) != dict or len(query) == 0):
                raise InvalidQuery("ERROR. The query should be a non-empty dict.")
            # Check the keys are string and the values exist
            if (not all(isinstance(key,str) for key in query) or None in query.values()):
                raise InvalidQuery("ERROR. The query should have string keys and non-None values.")
            # Searchs for items which have match with the specified query 
            items = self.get_records(query)
            
        # If there are not matched items, the new item can be inserted
        if (len(items) == 0):
            id_new_item = self.connection.insert_one(new_item.copy(), bypass_document_validation=True).inserted_id
            return str(id_new_item)
    
    def collection_size(self):
        """
        Gets the number of documents contained in the current collection.

        Returns
        -------
        An integer which represents the size of the current collection.
        """
        return self.connection.count_documents({})
    
    def delete_records(self, query={}):
        """
        Deletes the matched records related to the specified query in the current
        collection in the Mongo database. 
        If there is not provided query, every document of the current collection
        will be removed.

        Parameters
        ----------
        query : dict
            It's a dict which contains the query with string keys and non-None values
            to search for items with those features in order to remove them.
            If it's empty, the entire collection will be removed.
        
        Returns
        -------
        The number of deleted records.
        """
        if (type(self.connection) != pymongo.collection.Collection):
            raise ConnectionNotFound("ERROR. There is not connection to the database.")
        # Check the provided query
        if (type(query) != dict):
            raise InvalidQuery("ERROR. The query should be a dict.")
        # Check the keys are string and the values exist
        if (len(query) > 0):
            if (not all(isinstance(key,str) for key in query) or None in query.values()):
                raise InvalidQuery("ERROR. The query should have string keys and non-None values.")
        
        # Delete the matched items related to the specified query
        result = self.connection.delete_many(query)
        return result.deleted_count
    