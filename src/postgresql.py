#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which represents the Single Source of Truth which contains the operations
which can be done in the PostgreSQL database: insert a new element, make a select
query or delete all rows of a specific table.

This class will be used by all classes which operate with the PostgreSQL database.

@author: Lidia Sánchez Mérida.
"""
import os
import pg8000
import sys
sys.path.append('src/exceptions')
from exceptions import TableNotFound, NewItemNotFound, InvalidDatabaseConditions \
    , InvalidDatabaseFields, InvalidDatabaseCredentials

class PostgreSQL:
    
    def __init__(self):
        """
        Creates a PostgreSQL object whose attributes are:
            - The PostgreSQL database credentials.
            - The name of the PostgreSQL database.
            - The connection to the PostgreSQL database.
            - A cursor which can be used to make queries to the database.
            - The fiels of each table in the database.

        Raises
        ------
        InvalidDatabaseCredentials
            If the PostgreSQL database credentials are not non-empty strings, 
            are not stored in env variables or are wrong.

        Returns
        -------
        A PostgreSQL object with the connection to the PostgreSQL database.
        """
        user = os.environ.get("POSTGRES_USER") 
        pswd = os.environ.get("POSTGRES_PSWD")
        if (type(user) != str or user == "" or type(pswd) != str or pswd == ""):
            raise InvalidDatabaseCredentials("ERROR. The PostgreSQL credentials should be non-empty strings.")
        
        self.database_name = "socialnetworksdb"
        self.table_fields = {"test1":["id", "userid", "username", "date", "social_media"],
                             "test2":["id", "id_test1", "like_count", "text_count"]}
        # Connection to the database
        self.connection = pg8000.connect(user=user, password=pswd, database=self.database_name)
        self.cursor = self.connection.cursor()
    
    def get_records(self, table, fields=[], conditions=""):
        """
        Makes a query and returns the values of the fields from the matched records
        related to the specified query in a specific table.

        Parameters
        ----------
        table : str
            It's the table name in which the query is going to be made.
        fields : list, optional
            It's the list of fields to return.
            If it's empty, all values will be returned.
        conditions : str
            It's a string which specifies the conditions to make the query.
        
        Raises
        ------
        TableNotFound
            If the table name is not a non-empty string or does not exist.
        InvalidDatabaseFields
            If the provided fields are not non-empty strings or do not exist in the
            provided table.
        InvalidDatabaseConditions
            If the provided conditions are not in a non-empty string.

        Returns
        -------
        A tuple in which there are the matched records related to the made query.
        """
        # Check the provided table
        if (type(table) != str or table == ""):
            raise TableNotFound("ERROR. The table name should be a non-empty string.")
        # Check if the provided table exists
        if (table not in self.table_fields):
            raise TableNotFound("ERROR. The provided table name does not exist in the PostgreSQL database.")
        # Check the provided fields
        if (len(fields) > 0):
            # Check if they are in a list
            if (type(fields) != list):
                raise InvalidDatabaseFields("ERROR. The database fields should be in a list.")
            # Check that each element is a non-empty string and exist in the provided table
            result = [True for field in fields if (type(field) == str and field != ""
                           and field in self.table_fields[table])]
            if (len(result) != len(fields)):
                raise InvalidDatabaseFields("ERROR. All database fields should"
                        +" be non-empty strings and must exist in the provided table.")
        # Check the provided conditions
        if (len(conditions) > 0):
            if (type(conditions) != str):
                raise InvalidDatabaseConditions("ERROR. The query conditions should be in a non-empty strings.")
            
        # Build the query
        query = "SELECT "
        query += " * " if (len(fields) == 0) else ','.join(fields)
        query += " FROM " + table
        if (conditions != ""):
            query += " WHERE " + conditions
        
        # Make the query
        self.cursor.execute(query)
        matches = self.cursor.fetchall()
        return matches
    
    def insert_item(self, new_item, table, fields=[], conditions=""):
        """
        Inserts a new item in an existing table of the PostgreSQL database. A
        query can be provided in order to check if there are any items which are
        similar to the new item in order to insert it.

        Parameters
        ----------
        new_item : dict
            It's the dict with the new item to insert.
        table : str
            It's the table name in which the new item could be inserted.
        fields : list, optional
            It's the list of fields to make the query. The default is [].
        conditions : str, optional
            It's the string which contains the conditions to make the query. 
            The default is "".
        
        Raises
        ------
        NewItemNotFound
            If the provided item is not a non-empty dict.
        TableNotFound
            If the table name is not a non-empty string or does not exist.
        InvalidDatabaseFields
            If the provided fields are not non-empty strings or do not exist in the
            provided table.
        InvalidDatabaseConditions
            If the provided conditions are not in a non-empty string.

        Returns
        -------
        The number of the new inserted items.
        """
        # Check the new item
        if (type(new_item) != dict or len(new_item) == 0):
            raise NewItemNotFound("ERROR. The new item should be a non-empty dict.")
        # Check the specified table name
        if (type(table) != str or table == ""):
            raise TableNotFound("ERROR. The table name should be a non-empty string.")
        # Check if the provided table exists
        if (table not in self.table_fields):
            raise TableNotFound("ERROR. The provided table name does not exist in the PostgreSQL database.")
        # Check the provided fields
        if (len(fields) > 0):
            # Check if they are in a list
            if (type(fields) != list):
                raise InvalidDatabaseFields("ERROR. The database fields should be in a list.")
            # Check that each element is a non-empty string and exist in the provided table
            result = [True for field in fields if (type(field) == str and field != "" 
                       and field in self.table_fields[table])]
            if (len(result) != len(fields)):
                raise InvalidDatabaseFields("ERROR. All database fields should"
                        +" be non-empty strings and must exist in the provided table.")
        # Check the provided conditions
        if (len(conditions) > 0):
            if (type(conditions) != str):
                raise InvalidDatabaseConditions("ERROR. The query conditions should be in a non-empty strings.")
            
        # Make the query if the fields or/and the conditions have been provided
        matches = ()
        if (len(fields) > 0 or len(conditions) > 0):
            matches = self.get_records(table, fields, conditions)
            
        # Check if there are any matches
        if (len(matches) == 0):
            # Make the query
            table_fields_str = '(' + ','.join(self.table_fields[table]) + ')'
            value_count = " VALUES("
            # Add the list of values
            list_values = []
            for f in self.table_fields[table]:
                list_values.append(new_item[f])
                value_count += "%s,"
            # Delete the last comma
            value_count = value_count[:-1]
            # Close the value section
            value_count += ")"
            # Query 
            insert_query = "INSERT INTO "+ table + " " + table_fields_str + value_count
            values = tuple(list_values)
            # Number of rows before the insertion
            before_size = self.get_table_size(table)
            self.cursor.execute(insert_query, values)
            self.connection.commit()
            # Number of rows after the insertion
            after_size = self.get_table_size(table)
            
            return before_size < after_size
        
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
        An integer which is the number of records of the provided table.
        """
        # Check the specified table name
        if (type(table) != str or table == ""):
            raise TableNotFound("ERROR. The table name should be a non-empty string.")
        # Check if the provided table exists
        if (table not in self.table_fields):
            raise TableNotFound("ERROR. The provided table name does not exist in the PostgreSQL database.")

        query = "SELECT count(*) FROM "+table
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    def delete_records(self, table, conditions=""):
        """
        Deletes the records which matched with the provided conditions.
        If there aren't any conditions, all records will be deleted of the
        specific table.

        Parameters
        ----------
        table : str
            It's the table whose records are going to be deleted.
        conditions : str, optional
            They are the conditions to match the records to delete.ç
            If there aren't any conditions, all records will be deleted.

        Raises
        ------
        TableNotFound
            If the table name is not a non-empty string or does not exist.

        Returns
        -------
        True if the records have been deleted, False if they have not.
        """
        # Check the specified table name
        if (type(table) != str or table == ""):
            raise TableNotFound("The table should be a non empty string.")
        # Check if the specified table name is in the database
        if (table not in self.table_fields):
            raise TableNotFound("The specified table does not exist in the database.")
        # Make the query
        query = "DELETE FROM " + table
        # Check the provided conditions
        if (len(conditions) > 0):
            if (type(conditions) != str):
                raise InvalidDatabaseConditions("ERROR. The query conditions should be in a non-empty strings.")
            # Add the conditions
            query += " WHERE " + conditions
            
        # Get the matches
        matches = self.get_records(table, conditions=conditions)
        # Get the size of the table before the deleting
        before_size = self.get_table_size(table)
        # Send the query
        self.cursor.execute(query)
        self.connection.commit()
        # Get the size of the table after the deleting
        after_size = self.get_table_size(table)

        return len(matches) == (before_size-after_size)