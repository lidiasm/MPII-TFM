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
    result = test_connection.empty_table("TestParent")
    assert result == True
    
def test4_empty_table():
    """
    Test to check the method which deletes all the records from a specific table.
    In this test, the table 'TestChild' will be empty.
    """
    result = test_connection.empty_table("TestChild")
    assert result == True

def test5_empty_table():
    """
    Test to check the method which deletes all the records from a specific table.
    In this test, the table 'TestFK' will be empty.
    """
    result = test_connection.empty_table("TestFK")
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
    providing the new item. An exception will be raised.
    """
    with pytest.raises(InvalidQueryValues):
        test_connection.insert_data('insert_test_parent', None, None)

def test4_insert_data():
    """
    Test to check the method which inserts new data to a specific table without
    providing a valid new item with the required data. An exception will be raised.
    """
    with pytest.raises(InvalidQueryValues):
        test_connection.insert_data('insert_test_parent', [{'name':'name'}], None)
        
def test5_insert_data():
    """
    Test to check the method which inserts new data to a specific table without
    providing the values to check if the new item should be inserted. An exception will be raised.
    """
    new_parent = [{'id':'parent_one', 'is_parent':True, 'name':'Parent 1'}]
    with pytest.raises(InvalidQueryValues):
        test_connection.insert_data('insert_test_parent', new_parent, None)

def test6_insert_data():
    """
    Test to check the method which inserts new data to a specific table without
    providing valid values to check if the new item should be inserted. An exception will be raised.
    """
    new_parent = [{'id':'parent_one', 'is_parent':True, 'name':'Parent 1'}]
    invalid_check = {'name':'name'}
    with pytest.raises(InvalidQueryValues):
        test_connection.insert_data('insert_test_parent', new_parent, invalid_check)
    
def test7_insert_data():
    """
    Test to check the method which inserts new data to a specific table. In this test,
    a new parent item will be inserted into TestParent table.
    """
    new_parent = [{'id':'parent_one', 'is_parent':True, 'name':'Parent 1'}]
    check_values = {'id':'parent_one'}
    result = test_connection.insert_data('insert_test_parent', new_parent, check_values)
    assert result == True

def test8_insert_data():
    """
    Test to check the method which inserts new data to a specific table. In this test,
    the new parent is already in the TestParent table so it won't be inserted again.
    """
    new_parent = [{'id':'parent_one', 'is_parent':True, 'name':'Parent 1'}]
    check_values = {'id':'parent_one'}
    result = test_connection.insert_data('insert_test_parent', new_parent, check_values)
    assert result == False

def test9_insert_data():
    """
    Test to check the method which inserts new data to a specific table. In this test,
    a new child item will be inserted into TestChild table.
    """
    new_child = [{'id':'parent_one', 'is_parent':False, 'name':'Child 1'}]
    check_values = {'name':'Child 1'}
    result = test_connection.insert_data('insert_test_child', new_child, check_values)
    assert result == True
    
def test10_insert_data():
    """
    Test to check the method which inserts new data to a specific table. In this test,
    the new child item is already in the TestChild table so it won't be inserted again.
    """
    new_child = [{'id':'parent_one', 'is_parent':False, 'name':'Child 1'}]
    check_values = {'name':'Child 1'}
    result = test_connection.insert_data('insert_test_child', new_child, check_values)
    assert result == False

def test11_insert_data():
    """
    Test to check the method which inserts new data to a specific table. In this test,
    a new fk item will be inserted because it's not already in the table and the
    related parent item does exist.
    """
    new_fk = [{'id':'parent_one', 'field_one':'Any field'}]
    check_values = {'id':'parent_one', 'field_one':'Any field'}
    result = test_connection.insert_data('insert_test_fk', new_fk, check_values)
    assert result == True

def test12_insert_data():
    """
    Test to check the method which inserts new data to a specific table. In this test,
    the new fk item already exists so it won't be inserted.
    """
    new_fk = [{'id':'parent_one', 'field_one':'Any field'}]
    check_values = {'id':'parent_one', 'field_one':'Any field'}
    result = test_connection.insert_data('insert_test_fk', new_fk, check_values)
    assert result == False
    
def test13_insert_data():
    """
    Test to check the method which inserts new data to a specific table. In this test,
    the new fk item is related to a non-existing parent item so it won't be inserted.
    """
    new_fk = [{'id':'non-existing-parent', 'field_one':'Any field'}]
    check_values = {'id':'non-existing-parent', 'field_one':'Any field'}
    with pytest.raises(InvalidQueryValues):
        test_connection.insert_data('insert_test_fk', new_fk, check_values)
    
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