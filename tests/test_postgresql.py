#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests to check the right behaviour of the methods included in the Single Source
of Truth which has the operations with the PostgreSQL database.

@author: Lidia Sánchez Mérida.
"""
import os
import sys
sys.path.append("src")
import pytest
from exceptions import NewItemNotFound, TableNotFound, DatabaseFieldsNotFound \
    , InvalidFieldsToGet, InvalidConditions, InvalidDatabaseCredentials
from postgresql import PostgreSQL

"""Connection to test the PostgresSQL database operations."""
test_connection = PostgreSQL()

"""Table which will be used to test the PostgresSQL class"""
TABLE = "test1"

def test1_constructor():
    """Test to check the constructor of the PostgreSQL database class without providing 
        valid credentials. An exception will be raised."""
    global user
    user = os.environ.get("POSTGRES_USER") 
    global pswd
    pswd = os.environ.get("POSTGRES_PSWD")
    os.environ["POSTGRES_USER"] = ""
    os.environ["POSTGRES_PSWD"] = ""
    with pytest.raises(InvalidDatabaseCredentials):
        PostgreSQL()
    
def test1_empty_table():
    """Test to check the delete table method when the table is not provided. It will
        raise an exception. Also, the PostgreSQL credentials will be set again."""
    global user
    os.environ["POSTGRES_USER"] = user
    global pswd
    os.environ["POSTGRES_PSWD"] = pswd
    with pytest.raises(TableNotFound):
        test_connection.empty_table(1234)

def test2_empty_table():
    """Test to check the delete method when the table does not exist in the database.
        It will raise an exception."""
    with pytest.raises(TableNotFound):
        test_connection.empty_table("Hi")

def test3_empty_table():
    """Test to delete the rows of a specific table."""
    result = test_connection.empty_table(TABLE)
    assert result == True

def test1_insert_item():
    """Test to check the insert method when there's not new item to insert.
        It will raise an exception."""
    with pytest.raises(NewItemNotFound):
        test_connection.insert_item(None, None)

def test2_insert_item():
    """Test to check the insert method when the table is not provided. It will
        raise an exception."""
    data = {'profile': {'username':'lidia'}}
    with pytest.raises(TableNotFound):
        test_connection.insert_item(data, None)

def test3_insert_item():
    """Test to check the insert method when the provided table does not exist
        in the database. It will raise an exception."""
    data = {'profile': {'username':'lidia'}}
    with pytest.raises(TableNotFound):
        test_connection.insert_item(data, 'InvalidTable')

def test4_insert_item():
    """Test to check the insert method when the provided new item does not contain
        all the required fields. It will raise an exception."""
    data = {'profile': {'username':'lidia'}}
    with pytest.raises(DatabaseFieldsNotFound):
        test_connection.insert_item(data, TABLE)

def test5_insert_item():
    """Test to insert a new item in a table called 'test' to check the behaviour
        of this method. The new item should be a dict which contains every table
        field in order to get all required values to insert them as a new row."""
    data = {"userid":2040068873, "name":"Lidia Sánchez", "username":"lidia.96.sm",
            "biography":"\"Si eres valiente para empezar, eres fuerte para acabar.\" Ingeniería Informática.",
            "gender":"None", "profile_pic":"https://instagram.fsvq2-1.fna.fbcdn.net/v/t51.2885-19/s150x150/41339801_165526391018445_41443638382690304_n.jpg?_nc_ht=instagram.fsvq2-1.fna.fbcdn.net&_nc_ohc=hW7KS56GF7gAX_uMtm4&oh=1e8b084cced54e7208f8d459cff3ed95&oe=5F1A6F0A",
            "location":"None", "birthday":"None", "n_followers":60, "n_followings":80,
            "date_joined":"None", "n_posts":6, "social_media":"Instagram", "id":"lidia.96.sm", "date":"2020-06-21" }
    result = test_connection.insert_item(data, TABLE)
    assert result == True

def test1_get_item_records():
    """Test to check the get item records method when the table is not provided. It will
        raise an exception."""
    with pytest.raises(TableNotFound):
        test_connection.get_item_records(1234)

def test2_get_item_records():
    """Test to check the get item records method when the table is not provided. It will
        raise an exception."""
    with pytest.raises(TableNotFound):
        test_connection.get_item_records("Hi")

def test3_get_item_records():
    """Test to check the get item records method when the fields to return are
        not stored in a list."""
    with pytest.raises(InvalidFieldsToGet):
        test_connection.get_item_records(TABLE, fields={})

def test4_get_item_records():
    """Test to check the get item records method when the fields to return are
        not strings."""
    with pytest.raises(InvalidFieldsToGet):
        test_connection.get_item_records(TABLE, fields=[1234, ""])

def test5_get_item_records():
    """Test to check the get item records method when the conditions are not in
        a dict."""
    with pytest.raises(InvalidConditions):
        test_connection.get_item_records(TABLE, fields=["username"], conditions=1234)

def test6_get_item_records():
    """Test to check the get item records method when the command condition is not allowed ."""
    with pytest.raises(InvalidConditions):
        test_connection.get_item_records(TABLE, fields=["username"], conditions={'COMMAND':{}})

def test7_get_item_records():
    """Test to check the get item records method when the type of each condition is
        not a dict."""
    with pytest.raises(InvalidConditions):
        test_connection.get_item_records(TABLE, fields=["username"], conditions={'WHERE':1234})

def test8_get_item_records():
    """Test to get all the rows of a specific table without any conditions."""
    result = test_connection.get_item_records(TABLE)
    assert type(result) == tuple

def test9_get_item_records():
    """Test to get some fields of a specific table without any conditions."""
    result = test_connection.get_item_records(TABLE, fields=["username", "n_followings", "n_followers"])
    assert type(result) == tuple

def test10_get_item_records():
    """Test to get some fields of a specific table with some conditions WHERE and ORDER BY"""
    result = test_connection.get_item_records(TABLE,
              fields=["username", "name", "n_followers"],
              conditions={'WHERE':{'and':'n_followers>50', '-':'n_followings>5'}, 'ORDER BY':'n_followers'})
    assert type(result) == tuple