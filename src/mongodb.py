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
from datetime import datetime
import sys
sys.path.append('src/exceptions')
from exceptions import ConnectionNotFound, CollectionNotFound \
    , InvalidDatabaseCredentials, InvalidQuery, NewItemNotFound, InvalidQueryValues

class MongoDB:
    
    def __init__(self, collection):
        """
        Creates a MongoDB object whose attributes are:
            - The name of the database to connect with.
            - The Mongo database URI and credentials.
            - The queries to make in order to get some data.
            - The relationship between the insert and the get queries.
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
        # Check the provided collection to connect with
        if (type(collection) != str or collection == ""):
            raise InvalidDatabaseCredentials("ERROR. The collection name to connect to should be a non-empty string.")
        # Check the provided URI to connect to the database
        uri = os.environ.get("MONGODB_URI")
        if (type(uri) != str or uri == ""):
            raise InvalidDatabaseCredentials("ERROR. The MongoDB uri should be a non-empty string stored as a env variable.")
        
        # Queries to get data
        self.get_queries = {
            "get_dates":{
                "query":{"date":1},
                "fields":[]
            },
            "get_item":{
                "query":{"username":None, "social_media":None, "date":{"$gte":None, "$lte":None}},
                "fields":["username", "social_media", "date_ini", "date_fin"]
            },
            "get_test":{
                "query":{"username":None, "date":{"$gte":None, "$lte":None}, "social_media":None},
                "fields":["username", "date_ini", "date_fin", "social_media"]
            },
            "general_check":{
                "query":{"username":None, "date":None, "social_media":None},
                "fields":["username", "date", "social_media"]
            }
        }
        
        # Queries to delete some records from a specific collection
        self.delete_queries = {
            "delete_all":{
                "query":{}
            },
            "delete_item":{
                "query":{"username":None, "date":None, "social_media":None}
            }
        }
        
        # Make the connection
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
    
    def get_records(self, query, values={}):
        """
        Gets the records which matched with the specified query and values from
        the connected collection in the Mongo database.

        Parameters
        ----------
        query : str
            It's the query to make in order to get the data.
        values : dict, optional
            They are the required values to make the query, in case it has them. 
            The default is a empty dict.

        Raises
        ------
        ConnectionNotFound
            If the connection to the Mongo database has not been made.
        InvalidQuery
            If the provided query is not a non-empty string or does not exist.
        InvalidQueryValues
            If the provided values to make the query are not a non-empty dict
            or they haven't the required keys.

        Returns
        -------
        A list which contains the matched records as dicts.
        """
        # Check if the connection has been made
        if (type(self.connection) != pymongo.collection.Collection):
            raise ConnectionNotFound("ERROR. There is not connection to the database.")
        # Check the provided query
        if (type(query) != str or query == ""):
            raise InvalidQuery("ERROR. The query should be a non-empty string.")
        if (query not in self.get_queries):
            raise InvalidQuery("ERROR. The provided query does not exist.")
        # Check the provided values
        required_values = self.get_queries[query]["fields"]
        if (len(required_values) > 0 and (type(values) != dict or len(values) == 0)):
            raise InvalidQueryValues("ERROR. The specified query needs some values.")
        if (required_values != list(values.keys())):
            raise InvalidQueryValues("ERROR. The provided values to make the query are wrong.")
        
        # Complete the query
        final_query = self.get_queries[query]["query"]
        if (query == "get_dates"):
            item_rows = self.connection.find({}, final_query)
        elif (query == "general_check"):
            for key in final_query:
                final_query[key] = values[key]
            # Make the final query
            item_rows = self.connection.find(final_query)
        else:
            for key in required_values:
                if (key == "date_ini"):
                    final_query["date"]["$gte"] = datetime.strptime(values[key],"%d-%m-%Y")
                elif (key == "date_fin"):
                    final_query["date"]["$lte"] = datetime.strptime(values[key],"%d-%m-%Y") 
                else:
                    final_query[key] = values[key]
                    
            # Make the final query
            item_rows = self.connection.find(final_query)
        
        documents = []
        for item_r in item_rows:
            # Delete the Mongo id because it's useless
            del item_r["_id"]
            documents.append(item_r)
            
        return documents
    
    def insert_item(self, new_item):
        """
        Inserts a new record in a specific collection in the Mongo database if
        it doesn't already exist.

        Parameters
        ----------
        new_item : dict
            It's the new data to insert.

        Raises
        ------
        ConnectionNotFound
            If the connection to the Mongo database has not been made.
        NewItemNotFound
            If the provided values to make the query are not a non-empty dict.

        Returns
        -------
        A string id if the item could be inserted, None if it couldn't.
        """
        # Check if the connection has been made
        if (type(self.connection) != pymongo.collection.Collection):
            raise ConnectionNotFound("ERROR. There is not connection to the database.")
        # Check the provided new item
        if (type(new_item) != dict or len(new_item) == 0):
            raise NewItemNotFound("ERROR. The new item to insert should be a non-empty dict.")
        
        # Check if the item to insert already exists
        final_query = self.get_queries["general_check"]["query"]
        for key in self.get_queries["general_check"]["fields"]:
            final_query[key] = new_item[key]
        
        matched_records = self.get_records("general_check", final_query)
        # Insert the query if there are not equal records
        if (len(matched_records) == 0):
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
    
    def delete_records(self, query, values={}):
        """
        Deletes the matched records from a specific collection and related to
        the provided query.

        Parameters
        ----------
        query : str
            It's the query to make in order to remove the matched records.
        values : dict, optional
            They're the values to make the query. The default is {}.

        Raises
        ------
        ConnectionNotFound
            If the connection to the Mongo database has not been made.
        InvalidQuery
            If the provided query is not a non-empty string or does not exist.
        InvalidQueryValues
            If the provided values to make the query are not a non-empty dict
            or they haven't the required keys.

        Returns
        -------
        The number of deleted records.
        """
        # Check if the connection has been made
        if (type(self.connection) != pymongo.collection.Collection):
            raise ConnectionNotFound("ERROR. There is not connection to the database.")
        # Check the provided query
        if (type(query) != str or query == ""):
            raise InvalidQuery("ERROR. The query should be a non-empty string.")
        if (query not in self.delete_queries):
            raise InvalidQuery("ERROR. The provided query does not exist.")
        # Check the provided values
        required_values = list(self.delete_queries[query]["query"].keys())
        if (len(required_values) > 0 and (type(values) != dict or len(values) == 0)):
            raise InvalidQueryValues("ERROR. The specified query needs some values.")
        if (required_values != list(values.keys())):
            raise InvalidQueryValues("ERROR. The provided values to make the query are wrong.")
        
        # Complete the query
        final_query = self.delete_queries[query]["query"]
        if (len(required_values) > 0):
            for key in final_query:
                if (key == "date"):
                    final_query[key] = datetime.strptime(values[key],"%d-%m-%Y")
                else:
                    final_query[key] = values[key]
        
        # Delete the matched items related to the specified query
        result = self.connection.delete_many(final_query)
        return result.deleted_count