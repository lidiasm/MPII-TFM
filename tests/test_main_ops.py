#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests to check the methods of the class MainOperations.

@author: Lidia Sánchez Mérida
"""
import sys
import pytest
sys.path.append('src')
import main_ops 
from exceptions import UsernameNotFound, MaxRequestsExceed

def test1_get_user_instagram_data():
    """Test to check if the method can get, preprocess and store an Instagram user data."""
    try:
        mo = main_ops.MainOperations()
        username = "pabloalvarezss"
        result = mo.get_user_instagram_data(username)
        assert result['profile'] != None and result['contacts'] != None and result['posts'] != None
    except MaxRequestsExceed:
        print("Max requests exceed. Wait to send more.")

def test2_get_user_instagram_data():
    """Test to check if the method can get, preprocess and store an Instagram user
        data without specifing the username."""
    mo = main_ops.MainOperations()
    with pytest.raises(UsernameNotFound):
        assert mo.get_user_instagram_data('')