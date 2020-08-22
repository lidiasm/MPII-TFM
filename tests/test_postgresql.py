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
from postgresql import PostgreSQL
from exceptions import TableNotFound, NewItemNotFound \
    , InvalidDatabaseConditions, InvalidDatabaseFields, InvalidDatabaseCredentials

# Connection to test the PostgresSQL database operations.
test_connection = PostgreSQL()
# Tables to test the PostgreSQL methods
TABLE1 = "test1"
TABLE2 = "test2"

def test1_constructor():
    """
    Test to check the constructor of the PostgreSQL database class without providing 
    valid credentials. An exception will be raised.
    """
    global user
    user = os.environ.get("POSTGRES_USER") 
    global pswd
    pswd = os.environ.get("POSTGRES_PSWD")
    os.environ["POSTGRES_USER"] = ""
    os.environ["POSTGRES_PSWD"] = ""
    with pytest.raises(InvalidDatabaseCredentials):
        PostgreSQL()

def test1_insert_item():
    """
    Test to check the method which inserts a new item in a specific table of the
    PostgreSQL database without providing it. An exception will be raised.
    """
    with pytest.raises(NewItemNotFound):
        test_connection.insert_item(None, None)
        
def test2_insert_item():
    """
    Test to check the method which inserts a new item in a specific table of the
    PostgreSQL database without providing the table name. An exception will be raised.
    """
    with pytest.raises(TableNotFound):
        test_connection.insert_item({'id':'1'}, None)

def test3_insert_item():
    """
    Test to check the method which inserts a new item in a specific table of the
    PostgreSQL database without providing a existing table name. An exception will be raised.
    """
    with pytest.raises(TableNotFound):
        test_connection.insert_item({'id':'1'}, "InvalidTable")
        
def test4_insert_item():
    """
    Test to check the method which inserts a new item in a specific table of the
    PostgreSQL database without providing a valid set of table fields. An exception will be raised.
    """
    with pytest.raises(InvalidDatabaseFields):
        test_connection.insert_item({'id':'1'}, TABLE1, fields="Fields")
        
def test5_insert_item():
    """
    Test to check the method which inserts a new item in a specific table of the
    PostgreSQL database without providing a valid set of table fields. An exception will be raised.
    """
    with pytest.raises(InvalidDatabaseFields):
        test_connection.insert_item({'id':'1'}, TABLE1, fields=['fields', 'id', 'social_media'])

def test6_insert_item():
    """
    Test to check the method which inserts a new item in a specific table of the
    PostgreSQL database without providing valid query conditions. An exception will be raised.
    """
    with pytest.raises(InvalidDatabaseConditions):
        test_connection.insert_item({'id':'1'}, TABLE1, conditions=[1,2,3,4])

def test7_insert_item():
    """
    Test to check the method which inserts a new item in the 'test1' table without
    making any query. In order to run this test for pytest and codecov, the table
    deleted in order to insert this item always.
    """
    new_item = {'id':'456789_Instagram',
                'userid':456789,
                'username':'lidia',
                'date':'22-08-2020',
                'social_media':'Instagram'}
    # Delete the item whose id is '456789_Instagram'
    test_connection.delete_records(TABLE1, conditions="id='456789_Instagram'")
    result = test_connection.insert_item(new_item, TABLE1)
    assert result == True

def test8_insert_item():
    """
    Test to check the method which inserts a new item in the 'test1' table providing
    a condition to make a query in order to insert the new item if there aren't any matches.
    In this case, there are some matches so the new item couldn't be inserted.
    """
    new_item = {'id':'456789_Instagram',
                'userid':456789,
                'username':'lidia',
                'date':'22-08-2020',
                'social_media':'Instagram'}
    result = test_connection.insert_item(new_item, TABLE1, fields=["userid"], conditions="userid=456789")
    assert result == None

def test1_get_table_size():
    """
    Test to check the method which gets the number of records of a specific table
    without providing it, so an exception will be raised.
    """
    with pytest.raises(TableNotFound):
        test_connection.get_table_size(None)
        
def test2_get_table_size():
    """
    Test to check the method which gets the number of records of a specific table
    without providing an existing table name, so an exception will be raised.
    """
    with pytest.raises(TableNotFound):
        test_connection.get_table_size("InvalidTable")
        
def test3_get_table_size():
    """
    Test to check the method which gets the number of records of a specific table.
    """
    size = test_connection.get_table_size(TABLE1)
    assert type(size) == int

def test1_get_records():
    """
    Test to check the method which gets the matched records related to a specific
    query without providing the table name. An exception will be raised.
    """
    with pytest.raises(TableNotFound):
        test_connection.get_records(None)

def test2_get_records():
    """
    Test to check the method which gets the matched records related to a specific
    query without providing a valid table name. An exception will be raised.
    """
    with pytest.raises(TableNotFound):
        test_connection.get_records("InvalidTable")

def test3_get_records():
    """
    Test to check the method which gets the matched records related to a specific
    query without providing a valid list of table fields. An exception will be raised.
    """
    with pytest.raises(InvalidDatabaseFields):
        test_connection.get_records(TABLE1, "Fields")

def test4_get_records():
    """
    Test to check the method which gets the matched records related to a specific
    query without providing a valid list of table fields. An exception will be raised.
    """
    with pytest.raises(InvalidDatabaseFields):
        test_connection.get_records(TABLE1, ["userid", "invalid_field"])
        
def test5_get_records():
    """
    Test to check the method which gets the matched records related to a specific
    query without providing valid query conditions. An exception will be raised.
    """
    with pytest.raises(InvalidDatabaseConditions):
        test_connection.get_records(TABLE1, conditions=["condition1"])

def test6_get_records():
    """
    Test to check the method which gets the matched records related to a specific
    query without providing any fields or conditions. So the method will return
    all table records.
    """
    result = test_connection.get_records(TABLE1)
    size = test_connection.get_table_size(TABLE1)
    assert type(result) == tuple and len(result) == size

def test7_get_records():
    """
    Test to check the method which gets the matched records related to a specific
    query providing two fields. So the method will only return two values per
    table record.
    """
    result = test_connection.get_records(TABLE1, fields=['id', 'userid'])
    size_checked = [True for item in result if (len(item)==2)]
    assert len(result) == len(size_checked)

def test8_get_records():
    """
    Test to check the method which gets the matched records related to a specific
    query providing the list of fields to return as well as one condition. So the
    method will only return two values of the records which matched the condition.
    """
    result = test_connection.get_records(TABLE1, fields=['id', 'userid'], conditions="username='lidia'")
    size_checked = [True for item in result if (len(item)==2)]
    assert len(result) == len(size_checked)

def test9_get_records():
    """
    Test to check the method which gets the matched records related to a specific
    query providing only a condition. So the method will return all table fields
    of the records which matches the condition.
    """
    result = test_connection.get_records(TABLE1, conditions="userid=456789")
    assert type(result) == tuple and len(result) > 0

def test1_delete_records():
    """
    Test to check the method which deletes records related to a specific query
    or deletes all records of the provided table. In this case, the table name
    is not provided so an exception will be raised.
    """
    with pytest.raises(TableNotFound):
        test_connection.delete_records(None)

def test2_delete_records():
    """
    Test to check the method which deletes records related to a specific query
    or deletes all records of the provided table. In this case, a valid table name
    is not provided so an exception will be raised.
    """
    with pytest.raises(TableNotFound):
        test_connection.delete_records("InvalidTable")

def test3_delete_records():
    """
    Test to check the method which deletes records related to a specific query
    or deletes all records of the provided table without providing valid query
    conditions. An exception will be raised.
    """
    with pytest.raises(InvalidDatabaseConditions):
        test_connection.delete_records(TABLE1, conditions=[1,2,3])

def test4_delete_records():
    """
    Test to check the method which deletes records related to a specific query
    or deletes all records of the provided table. In this case, a new item is 
    inserted in the table 'test2', which was empty, in order to delete it then.
    """
    new_item = {'id':'1',
                'id_test1':'456789_Instagram',
                'like_count':154,
                'text_count':23}
    test_connection.insert_item(new_item, TABLE2)
    result = test_connection.delete_records(TABLE2)
    assert result == True

def test5_delete_records():
    """
    Test to check the method which deletes records related to a specific query
    or deletes all records of the provided table. In this case, a new item is inserted
    in the table 'test2', which was empty, in order to delete all records of the
    table 'test1' taking into account that the 'test2' table has a foreign key to
    the 'id' field of the 'test1' table. So the method will delete all records
    from the two tables.
    """
    new_item = {'id':'1',
                'id_test1':'456789_Instagram',
                'like_count':154,
                'text_count':23}
    test_connection.insert_item(new_item, TABLE2)
    result = test_connection.delete_records(TABLE1)
    size_test1 = test_connection.get_table_size(TABLE1)
    size_test2 = test_connection.get_table_size(TABLE2)
    assert result == True and size_test1 == 0 and size_test2 == 0
    