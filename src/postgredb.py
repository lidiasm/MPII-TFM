#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which represents the Single Source of Truth and contains the operations
which can be done in the PostgreSQL database.
    - Insert a new item in a specific table, if it's not already.
    - Get the matched records related to a specific query.
    - Get the number of records or size from a table.

This class will be used by the classes which needs to operate with the PostgreSQL database.

@author: Lidia Sánchez Mérida
"""
import psycopg2
import os
from exceptions import InvalidDatabaseCredentials, InvalidTableName \
    , InvalidQuery, InvalidQueryValues

class PostgreDB:
    
    def __init__(self):
        """
        Creates a PostgreSQL object whose attributes are:
            - The name of the PostgreSQL database.
            - The tables of the database.
            - The connection and the cursor to make queries.
            - The avalaible queries to make.
            - The check queries to make in order to insert new data.

        Returns
        -------
        A PostgreSQL object with the connection to the PostgreSQL database.
        """
        # Database name
        self.database_name = "socialnetworksdb"
        # Tables of the database
        self.tables = ['contacts', 'profiles', 'posts', 'users', 'commoninteractions',
                       'twitterinteractions', 'commontexts', 'posttitles', 'posttexts',
                       'testparent', 'testchild', 'testfk']
        # Connect to the database
        self.connect_to_database()
        
        ## PREDEFINED QUERIES
        # Select queries, to get data from the database
        self.select_queries = {
            'check_test_parent':{
                'query':'SELECT id FROM testparent WHERE id=%s',
                'fields':['id']},
            'check_test_child':{
                'query':'SELECT id FROM testchild WHERE name=%s',
                'fields':['name']},
            'check_test_fk':{
                'query':'SELECT id_test_fk FROM testfk WHERE id=%s AND field_one=%s',
                'fields':['id', 'field_one']},
        }
        
        # Insert queries, to add new data to the database
        self.insert_queries = {
            'insert_test_parent':{
                'query':'INSERT INTO testparent (id, is_parent, name) VALUES (%s, %s, %s)',
                'fields':['id', 'is_parent', 'name']},
            'insert_test_child':{
                'query':'INSERT INTO testchild (id, is_parent, name) VALUES (%s, %s, %s)',
                'fields':['id', 'is_parent', 'name']},
            'insert_test_fk':{
                'query':'INSERT INTO testfk (id, field_one) VALUES (%s, %s)',
                'fields':['id', 'field_one']},
        }
        # Check queries to make before inserting new data
        self.check_queries = {
            'insert_test_parent':'check_test_parent',
            'insert_test_child':'check_test_child',
            'insert_test_fk':'check_test_fk',
            
            'delete_test_parent':'check_test_parent',
            'delete_test_child':'check_test_child',
            'delete_test_fk':'check_test_fk'
        }
    
    def connect_to_database(self):
        """
        Makes the connection to the database through the environment variables which
        contains the credentials.

        Raises
        ------
        InvalidDatabaseCredentials
            If the credentials are not non-empty strings or are incorrect.

        Returns
        -------
        The cursor object which allows to make the queries.
        """
        # Get the PostgreSQL credentials
        user = os.environ.get("POSTGRES_USER") 
        pswd = os.environ.get("POSTGRES_PSWD")
        # Check the provided credentials
        if (type(user) != str or user == "" or type(pswd) != str or pswd == ""):
            raise InvalidDatabaseCredentials("ERROR. The PostgreSQL credentials should be non-empty strings.")
        # Try to connect to the database        
        try:
            self.connection = psycopg2.connect(user=user, password=pswd, database=self.database_name)
            self.cursor = self.connection.cursor()
            return self.cursor
        except Exception: # pragma no cover
            raise InvalidDatabaseCredentials("ERROR. The provided PostgreSQL credentials are wrong.")
    
    def get_data(self, query, values={}):
        """
        Makes a predefined query in a specific table and returns the matched records.
        In order to prevent SQL injection, non-predefined queries will not be allowed.

        Parameters
        ----------
        query : str
            It's the predefined query to make.
        values : dict
            It's the dict which contains the values to make the provided query.
            It could be not provided if the query does not need any additional parameters.
        
        Raises
        ------
        InvalidQuery
            If the provided query is not a non-empty string or is not one of the defined queries.
        InvalidQueryValues
            If the provided values for the selected query are not valid.

        Returns
        -------
        A tuple of lists with the matched results and the values of the specific
        chosen fields.
        """
        # Check the provided predefined query
        if (type(query) != str or query == ""):
            raise InvalidQuery("ERROR. The query should be a non-empty string.")
        # Check if the provided query exists
        if (query not in self.select_queries):
            raise InvalidQuery("ERROR. The provided query does not exist.")
        # Check if the query needs some values and if they've been provided
        if (len(self.select_queries[query]['fields']) > 0 and (type(values) != dict or len(values) == 0)):
            raise InvalidQueryValues("ERROR. The selected query needs values and they've not been provided.")
            
        # Check if all the provided values are required
        query_fields = self.select_queries[query]['fields']
        value_fields = list(values.keys())
        if (query_fields != value_fields or not all(isinstance(value, str) for value in list(values.values()))):
            raise InvalidQueryValues("ERROR. Some of the required values are missing or are wrong.")
    
        # Make the final query
        try: 
            self.cursor.execute(self.select_queries[query]['query'], list(values.values()))
            matches = self.cursor.fetchall()
        except: #pragma no cover
            self.connect_to_database()
            self.cursor.execute(self.select_queries[query]['query'], list(values.values()))
            matches = self.cursor.fetchall()
        
        return matches
    
    def get_table_size(self, table):
        """
        Gets the number of records of the provided table. In order to do that, 
        'count()' operation will be used to make a query which returns the number
        of rows of the table.

        Parameters
        ----------
        table : str
            It's the table name whose size is going to be get.

        Raises
        ------
        TableNotFound
            If the table name is not a non-empty string or does not exist in the
            PostgreSQL database.

        Returns
        -------
        An integer which is the number of records of the specified table.
        """
        # Check the specified table name
        if (type(table) != str or table == ""):
            raise InvalidTableName("ERROR. The table name should be a non-empty string.")
        # Check if the provided table exists
        if (table.lower() not in self.tables):
            raise InvalidTableName("ERROR. The provided table name does not exist in the PostgreSQL database.")

        query = "SELECT count(*) FROM "+table
        try:
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        except: #pragma no cover
            self.connect_to_database()
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        
    def insert_data(self, query, new_values, check_values):
        """
        Inserts new records in a specific table if the new item does not already
        exist. Each table will have its own inserted conditions.

        Parameters
        ----------
        query : str
            It's the inserted query to make.
        new_values : list of dicts
            It's the list which contains the new items to insert in different dicts.
            In this way, one or multiple items could be inserted.
        check_values : dict
            It's the dict which contains the values to make the select query in
            order to check if the new item to add is already in the database.
        
        Raises
        ------
        InvalidQuery
            If the provided query is not a non-empty string or is not one of the insert queries.
        InvalidQueryValues
            If the provided values for the insert query are not valid.

        Returns
        -------
        True if the new item has been inserted, False if it's not.
        """
        # Check the provided inserted query
        if (type(query) != str or query == ""):
            raise InvalidQuery("ERROR. The provided query should be a non-empty string.")
        if (query not in self.insert_queries):
            raise InvalidQuery("ERROR. The provided query is not valid.")
        
        # Check the new values
        if (type(new_values) != list or len(new_values) == 0 or 
            not all(isinstance(item, dict) for item in new_values)):
            raise InvalidQueryValues("ERROR. There are not new data to insert.")
        # Check if each item has the required values
        query_fields = self.insert_queries[query]['fields']
        for item in new_values:
            # Check the data types of the values: str or bool
            check = list(set([True for value in list(item.values()) if type(value) == str or type(value) == bool]))
            ## IMPORTANT 
            if (list(item.keys()) != query_fields or len(check) > 1 or check[0] != True): 
                raise InvalidQueryValues("ERROR. The provided values for the insert query are wrong.")
        
        # Check the select values
        if (type(check_values) != dict or len(check_values) == 0):
            raise InvalidQueryValues("ERROR. The values to check if the new item could be inserted should be in a non-empty dict.")
        select_fields = self.select_queries[self.check_queries[query]]['fields']
        if (list(check_values.keys()) != select_fields):
            raise InvalidQueryValues("ERROR. Some check values are missing.")
        
        # Check if the new item to insert is already in the table
        if (not self.get_data(self.check_queries[query], check_values)):
            # Get the table to store the previous size befote the insertion         
            table = [table_name for table_name in self.tables if table_name in self.insert_queries[query]['query']]
            previous_size = self.get_table_size(table[0])
            for item in new_values:
                try:
                    self.cursor.execute(self.insert_queries[query]['query'], list(item.values()))
                    self.connection.commit()
                except: 
                    raise InvalidQueryValues("ERROR. The new data couldn't be inserted.")
                
            # Get the number of records after adding the new data
            after_size = self.get_table_size(table[0])
            return after_size == previous_size+len(new_values)
        
        return False
    
    def empty_table(self, table):
        """
        Deletes all the records stored in a specific table without removing it.
        In this way, the table will be empty.

        Parameters
        ----------
        table : str
            It's the table name to make empty.

        Raises
        ------
        InvalidTable
            If the provided table name is not a non-empty string or does not exist
            in the database.

        Returns
        -------
        True if the table is now empty, False if it's not.
        """
        # Check the table name provided
        if (type(table) != str or table == ""):
            raise InvalidTableName("ERROR. The table name should be a non-empty list.")
        # Check that the table exists
        if (table.lower() not in self.tables):
            raise InvalidTableName("ERROR. The provided table name does not exist in the database.")
        
        # Deletes all records from the table
        query = "DELETE FROM "+table
        self.cursor.execute(query)
        return self.get_table_size(table) == 0