#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests to check the right behaviour of the methods included in the Single Source
of Truth which has the operations with the PostgreSQL database.

@author: Lidia Sánchez Mérida
"""
import os
import pytest
import sys
sys.path.append("src")
from postgredb import PostgreDB
from exceptions import InvalidDatabaseCredentials, InvalidTableName, InvalidQuery \
    , InvalidQueryValues

def test1_connect_to_database():
    """
    Test to check the method which connects to the Postgre database without providing
    valid credentials. An exception will be raised.
    """
    global env_user
    env_user = os.environ.get("POSTGRES_USER")
    os.environ['POSTGRES_USER'] = ""
    with pytest.raises(InvalidDatabaseCredentials):
        PostgreDB()

def test2_connect_to_database():
    """
    Test to check the method which connects to the Postgre database without providing
    valid credentials. An exception will be raised.
    """
    global env_pswd 
    env_pswd = os.environ.get("POSTGRES_PSWD")
    os.environ['POSTGRES_PSWD'] = "wrongpassword"
    with pytest.raises(InvalidDatabaseCredentials):
        PostgreDB()

def test3_connect_to_database():
    """
    Test to check the method which connects to the Postgre database without providing
    valid credentials. In order to do that, the valid credentials will be set again
    in environment variables.
    """
    os.environ["POSTGRES_USER"] = env_user 
    os.environ["POSTGRES_PSWD"] = env_pswd
    global test_connection
    test_connection = PostgreDB()
    
def test1_empty_table():
    """
    Test to check the method which deletes all the records from a specific table
    without providing its name. An exception will be raised.
    """
    with pytest.raises(InvalidTableName):
        test_connection.empty_table(None)

def test2_empty_table():
    """
    Test to check the method which deletes all the records from a specific table
    without providing a valid table name. An exception will be raised.
    """
    with pytest.raises(InvalidTableName):
        test_connection.empty_table("InvalidTable")
        
def test3_empty_table():
    """
    Test to check the method which deletes all the records from a specific table.
    In this test, the table 'TestParent' will be empty.
    """
    result = test_connection.empty_table("testparent")
    assert result == True
    
def test4_empty_table():
    """
    Test to check the method which deletes all the records from a specific table.
    In this test, the table 'TestChild' will be empty.
    """
    result = test_connection.empty_table("testchild")
    assert result == True

def test5_empty_table():
    """
    Test to check the method which deletes all the records from a specific table.
    In this test, the table 'TestFK' will be empty.
    """
    result = test_connection.empty_table("testfk")
    assert result == True
    
def test1_insert_data():
    """
    Test to check the method which inserts new data to a specific table without
    providing the insert query. An exception will be raised.
    """
    with pytest.raises(InvalidQuery):
        test_connection.insert_data(None, None, None)
        
def test2_insert_data():
    """
    Test to check the method which inserts new data to a specific table without
    providing a valid insert query. An exception will be raised.
    """
    with pytest.raises(InvalidQuery):
        test_connection.insert_data('non_existing_query', None, None)
        
def test3_insert_data():
    """
    Test to check the method which inserts new data to a specific table without
    providing the new values to insert and the select values to check if the
    new items are already in the database. An exception will be raised.
    """
    with pytest.raises(InvalidQueryValues):
        test_connection.insert_data('insert_test_parent', None, None)
        
def test4_insert_data():
    """
    Test to check the method which inserts new data to a specific table without
    providing valid new values to insert them in the database. An exception will be raised.
    """
    new_values = [{"id":"1", "is_parent":True},
                  {"id":"2", "is_parent":True, "name":"Second parent"}]
    check_values = [{"id":"1"}]
    with pytest.raises(InvalidQueryValues):
        test_connection.insert_data('insert_test_parent', new_values, check_values)
        
def test5_insert_data():
    """
    Test to check the method which inserts new data to a specific table without
    providing valid check values to know if the new items are already in the 
    database. An exception will be raised.
    """
    new_values = [{"id":"1", "is_parent":True, "name":"Second parent"}]
    with pytest.raises(InvalidQueryValues):
        test_connection.insert_data('insert_test_parent', new_values, [1,2,3])
        
def test6_insert_data():
    """
    Test to check the method which inserts new data to a specific table without
    providing the same number of new items and the check values, so an exception
    will be raised.
    """
    new_values = [{"id":"1", "is_parent":True, "name":"First parent"},
                  {"id":"2", "is_parent":True, "name":"Second parent"}]
    check_values = [{"id":"1"}]
    with pytest.raises(InvalidQueryValues):
        test_connection.insert_data('insert_test_parent', new_values, check_values)
        
def test7_insert_data():
    """
    Test to check the method which inserts new data to a specific table without
    providing the required keys for the check values to know if the new items
    are already in the database. So an exception will be raised.
    """
    new_values = [{"id":"1", "is_parent":True, "name":"First parent"},
                  {"id":"2", "is_parent":True, "name":"Second parent"}]
    check_values = [{"name":"1"}, {"name":"2"}]
    with pytest.raises(InvalidQueryValues):
        test_connection.insert_data('insert_test_parent', new_values, check_values)
        
def test8_insert_data():
    """
    Test to check the method which inserts new data to a specific table in the
    Postgres database. In this test, four new items will be inserted in the
    'TestParent' table because none of them are already in the database.
    """
    new_values = [{"id":"1", "is_parent":True, "name":"First parent"},
                  {"id":"2", "is_parent":True, "name":"Second parent"},
                  {"id":"3", "is_parent":True, "name":"Third parent"},
                  {"id":"4", "is_parent":True, "name":"Fourth parent"}]
    check_values = [{"id":"1"}, {"id":"2"}, {"id":"3"}, {"id":"4"}]
    ids = test_connection.insert_data('insert_test_parent', new_values, check_values)
    assert len(ids) == len(new_values)
    
def test9_insert_data():
    """
    Test to check the method which inserts new data to a specific table in the
    Postgres database. In this test, only two of the four new items will be inserted
    in the 'TestParent' table because the other two are already in the database.
    """
    new_values = [{"id":"1", "is_parent":True, "name":"First parent"},
                  {"id":"5", "is_parent":True, "name":"Fith parent"},
                  {"id":"3", "is_parent":True, "name":"Third parent"},
                  {"id":"6", "is_parent":True, "name":"Sixth parent"}]
    check_values = [{"id":"1"}, {"id":"5"}, {"id":"3"}, {"id":"6"}]
    ids = test_connection.insert_data('insert_test_parent', new_values, check_values)
    assert len(ids) < len(new_values)
    
def test10_insert_data():
    """
    Test to check the method which inserts new data to a specific table in the
    Postgres database. In this test, four new items will be inserted in the
    'TestChild' table because none of them are already in the database.
    """
    new_values = [{"id":"1", "is_parent":False, "name":"First child"},
                  {"id":"2", "is_parent":False, "name":"Second child"},
                  {"id":"3", "is_parent":False, "name":"Third child"},
                  {"id":"4", "is_parent":False, "name":"Fourth child"}]
    check_values = [{"name":"First child"}, {"name":"Second child"}, 
                    {"name":"Third child"}, {"name":"Fourth child"}]
    ids = test_connection.insert_data('insert_test_child', new_values, check_values)
    assert len(ids) == len(new_values)
    
def test11_insert_data():
    """
    Test to check the method which inserts new data to a specific table in the
    Postgres database. In this test, only one of the four new items will be inserted
    in the 'TestChild' table because the other two are already in the database.
    """
    new_values = [{"id":"1", "is_parent":False, "name":"First child"},
                  {"id":"2", "is_parent":False, "name":"Second child"},
                  {"id":"9", "is_parent":False, "name":"Nineth child"},
                  {"id":"4", "is_parent":False, "name":"Fourth child"}]
    check_values = [{"name":"First child"}, {"name":"Second child"}, 
                    {"name":"Nineth child"}, {"name":"Fourth child"}]
    ids = test_connection.insert_data('insert_test_child', new_values, check_values)
    assert len(ids) < len(new_values)
    
def test12_insert_data():
    """
    Test to check the method which inserts new data to a specific table in the
    Postgres database. In this test, four new items will be inserted in the
    'TestFK' table because none of them are already in the database.
    """
    new_values = [{"id":"1", "field_one":"First field"},
                  {"id":"2", "field_one":"Second field"},
                  {"id":"3", "field_one":"Third field"},
                  {"id":"4", "field_one":"Fourth field"}]
    check_values = new_values
    ids = test_connection.insert_data('insert_test_fk', new_values, check_values)
    assert len(ids) == len(new_values)
    
def test13_insert_data():
    """
    Test to check the method which inserts new data to a specific table in the
    Postgres database. In this test, only one of the four new items will be inserted
    in the 'TestFK' table because the other two are already in the database.
    """
    new_values = [{"id":"1", "field_one":"First field"},
                  {"id":"2", "field_one":"Second field"},
                  {"id":"6", "field_one":"Sixth field"},
                  {"id":"4", "field_one":"Fourth field"}]
    check_values = new_values
    ids = test_connection.insert_data('insert_test_fk', new_values, check_values)
    assert len(ids) < len(new_values)
    
def test14_insert_data():
    """
    Test to check the method which inserts new data to a specific table in the
    Postgres database. In this test, some of the items have non-existing values
    in the foreign keys so an exception will be raised.
    """
    new_values = [{"id":"100", "field_one":"Invalid field"},
                  {"id":"200", "field_one":"Invalid field"},
                  {"id":"600", "field_one":"Invalid field"},
                  {"id":"5", "field_one":"Fifth field"}]
    check_values = new_values
    with pytest.raises(InvalidQueryValues):
        test_connection.insert_data('insert_test_fk', new_values, check_values)
        
def test1_get_data():
    """
    Test to check the method which gets data from a specific table. In this test,
    there is not provided query so an exception will be raised.
    """
    with pytest.raises(InvalidQuery):
        test_connection.get_data(None, None)

def test2_get_data():
    """
    Test to check the method which gets data from a specific table. In this test,
    the provided query is not valid so an exception will be raised.
    """
    with pytest.raises(InvalidQuery):
        test_connection.get_data("invalid_query", None)

def test3_get_data():
    """
    Test to check the method which gets data from a specific table. In this test,
    there are not provided values which are required to make the query so an exception
    will be raised.
    """
    with pytest.raises(InvalidQueryValues):
        test_connection.get_data('check_test_parent', None)
        
def test4_get_data():
    """
    Test to check the method which gets data from a specific table. In this test,
    the provided values to make the query are wrong so an exception will be raised.
    """
    with pytest.raises(InvalidQueryValues):
        test_connection.get_data('check_test_parent', {'name':'name'})

def test1_get_table_size():
    """
    Test to check the method which counts the number of records of a specific table
    without providing it, so an exception will be raised.
    """
    with pytest.raises(InvalidTableName):
        test_connection.get_table_size(123456)

def test2_get_table_size():
    """
    Test to check the method which counts the number of records of a specific table
    without providing a valid table name, so an exception will be raised.
    """
    with pytest.raises(InvalidTableName):
        test_connection.get_table_size("InvalidTable")