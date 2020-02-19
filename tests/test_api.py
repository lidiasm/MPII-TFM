#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests to check the right behaviour of the methods included in the singleton class
Api. 

@author: Lidia Sánchez Mérida
"""

import sys
import pytest
sys.path.append("src")
sys.path.append("src/data")
import api  
from exceptions import UsernameNotFound, MaxRequestsExceed, SingletonClass

"""Unique instance from a singleton class."""
apiClass = api.Api()

def test1_get_instance():
    """Test to check the singleton class. It can only create one instance."""
    with pytest.raises(SingletonClass):
        assert api.Api()

def test1_instagram_api():
    """Test to check the method which connects to an Instagram API and downloads
        profile data from a user which is not specified."""
    with pytest.raises(UsernameNotFound):
        assert apiClass.instagram_api("")

def test2_instagram_api():
    """Test to check the method which connects to an Instagram API and downloads
        profile data from a user which is not specified."""
    with pytest.raises(UsernameNotFound):
        assert apiClass.instagram_api(None)

def test3_instagram_api():
    """Test to check the method which connects to an Instagram API and downloads
        profile data from a user which is not specified."""
    with pytest.raises(UsernameNotFound):
        assert apiClass.instagram_api(1234)        

def test4_instagram_api():
    """Test to check the method which connects to an Instagram API and download
        data profile from a specific user."""
    try:
        assert type(apiClass.instagram_api("bodegasf")) == dict
    except MaxRequestsExceed:
        print("Maximum requests exceed. Please wait some time before sending more.")