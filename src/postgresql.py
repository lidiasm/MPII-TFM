#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which represents the Single Source of Truth which contains the operations
which can be done in the PostgreSQL database: insert a new element, make a select
query or delete all rows of a specific table.

This class will be used by all classes which operate with the PostgreSQL database.

@author: Lidia Sánchez Mérida.
"""

import pg8000
import sys
sys.path.append('src/exceptions')
from exceptions import TableNotFound, NewItemNotFound, DatabaseFieldsNotFound \
    , InvalidConditions, InvalidFieldsToGet

class PostgreSQL:

    def __init__(self, db, user, pswd):
        """PostgreSQL constructor. It creates an object with two attributes:
            - A connection to the PostgreSQL database which contains Instagram data.
            - A cursor which can be used to make queries to the database.
            - The fields which are contained in each table of the database.
            - The allowed commands to use in select query conditions."""
        self.connection = pg8000.connect(user=user, password=pswd, database=db)
        self.cursor = self.connection.cursor()
        self.fields = {'profiles':['username', 'date', 'name', 'userid', 'biography',
                          'gender', 'profile_pic', 'location', 'birthday', 'date_joined',
                          'n_followers', 'n_followings', 'n_medias', 'social_media']}
        self.condition_commands = ['WHERE', 'ORDER BY']

    def insert_item(self, new_item, table):
        """Method which inserts a new item into a existing table of the database.
            The new item should have the same required fields that the table has
            in order to get a value for each field."""
        # Check the new item
        if (type(new_item) != dict or len(new_item) == 0):
            raise NewItemNotFound("The new item should be a dict.")
        # Check the specified table name
        if (type(table) != str or table == ""):
            raise TableNotFound("The table should be a non empty string.")
        # Check if the specified table name is in the database
        if (table not in self.fields):
            raise TableNotFound("The specified table does not exist in the database.")
        # Check the dict fields
        for f in self.fields[table]:
            if (f not in new_item):
                raise DatabaseFieldsNotFound("Some required fields are not in the new item, like: "+f)

        table_fields_str = '(' + ','.join(self.fields[table]) + ')'
        insert_query = "INSERT INTO "+ table + " " + table_fields_str \
            + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        list_values = []
        for f in self.fields[table]:
            list_values.append(new_item[f])

        values = tuple(list_values)
        prev_rowcount = self.cursor.rowcount
        self.cursor.execute(insert_query, values)
        self.connection.commit()

        return prev_rowcount < self.cursor.rowcount

    def get_item_records(self, table, fields=[], conditions={}):
        """Method to get the rows of a select query choosing:
            - All fields or some of them. They should be non empty strings, stored
                in a list and they should match to the fields of the specified table.
            - Some conditions to make the select query (WHERE / ORDER BY). The command
                will be the key and its value will be another dict with the conditions and
                the boolean operators to apply. The key of the last condition won't be taken into account."""
        # Check the specified table name
        if (type(table) != str or table == ""):
            raise TableNotFound("The table should be a non empty string.")
        # Check if the specified table name is in the database
        if (table not in self.fields):
            raise TableNotFound("The specified table does not exist in the database.")
        # Check the fields to return.
        if (type(fields) != list):
            raise InvalidFieldsToGet("The fields to return should be stored in a list.")
        for field in fields:
            if (type(field) != str or field not in self.fields[table]):
                raise InvalidFieldsToGet("The fields to return should be non empty.")
        # Check the conditions
        if (type(conditions) != dict):
            raise InvalidConditions("The conditions for getting items from the database should be a dict.")
        for command in conditions:
            if (command not in self.condition_commands):
                raise InvalidConditions("The allowed commands are: "+ ','.join(self.condition_commands))

        """Make and send the select query"""
        select_query = "SELECT "
        # Select every field
        if (len(fields) == 0):
            select_query += " * "
        # Select some fields
        else:
            select_query += ','.join(fields)
        # Specify the table
        select_query += " FROM " + table
        # Conditions
        if (len(conditions) > 0):
            if ('WHERE' in conditions):
                if (type(conditions['WHERE']) != dict):
                    raise InvalidConditions("Each WHERE condition should be a dict like this: {'bool operator':'condition}")
                select_query += " WHERE "
                n_wheres = 0
                for key in conditions['WHERE']:
                    select_query += conditions['WHERE'][key]
                    n_wheres += 1
                    if (n_wheres < len(conditions['WHERE'])):
                        select_query += " " + key + " "
            if ('ORDER BY' in conditions):
                select_query += " ORDER BY " + conditions['ORDER BY']

        # Send the select query
        self.cursor.execute(select_query)
        rows = self.cursor.fetchall()

        return rows

    def empty_table(self, table):
        """Method to delete all rows of a specific table without deleting it."""
        # Check the specified table name
        if (type(table) != str or table == ""):
            raise TableNotFound("The table should be a non empty string.")
        # Check if the specified table name is in the database
        if (table not in self.fields):
            raise TableNotFound("The specified table does not exist in the database.")

        prev_rowcount = self.cursor.rowcount
        delete_query = "TRUNCATE " + table
        self.cursor.execute(delete_query)
        self.connection.commit()

        return prev_rowcount-self.cursor.rowcount == 0