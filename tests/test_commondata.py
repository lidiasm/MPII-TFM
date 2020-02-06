#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests to check the right behaviour of the methods included in the class CommonData.

@author: Lidia Sánchez Mérida
"""

import sys
import pytest
sys.path.append("src")
sys.path.append("src/data")
import commondata 
from exceptions import ProfileNotFound, BasicProfileDataNotFound

def test1_check_profile_field():
    """Test to check if the field 'birthay' exists in a JSON dict. In this case
        it doesn't so it will return None"""
    profile = {'username':'lidia', 'name':'Lidia', 'email':'lidia@lidia.es'}
    following = {'1':'Ana Ortiz', '2':'Eva García'}
    followers = {'1':'Ana Ortiz', '2':'Paloma Peña'}
    data1 = commondata.CommonData(profile, following, followers)
    assert data1.check_profile_field('birthday') == None

def test2_check_profile_field():
    """Test to check if the field 'username' exists in a JSON dict. In this case
        it does so it will return its value."""
    profile = {'username':'lidia', 'name':'Lidia', 'email':'lidia@lidia.es'}
    following = {'1':'Ana Ortiz', '2':'Eva García'}
    followers = {'1':'Ana Ortiz', '2':'Paloma Peña'}
    data1 = commondata.CommonData(profile, following, followers)
    assert type(data1.check_profile_field('username')) == str and data1.check_profile_field('username') != "None"

def test1_profile_preprocessing():
    """Test to check if the provided profile is valid. In this case it is so
        after the preprocessing it will be returned."""
    profile = {'username':'lidia', 'name':'Lidia', 'email':'lidia@lidia.es'}
    following = {'1':'Ana Ortiz', '2':'Eva García'}
    followers = {'1':'Ana Ortiz', '2':'Paloma Peña'}
    data1 = commondata.CommonData(profile, following, followers)
    assert type(data1.profile_preprocessing()) == dict

def test2_profile_preprocessing():
    """Test to check if the provided profile is valid. In this case it's not
        so the method will raise an exception."""
    profile = {'username':'lidia', 'name':None}
    following = {'1':'Ana Ortiz', '2':'Eva García'}
    followers = {'1':'Ana Ortiz', '2':'Paloma Peña'}
    data1 = commondata.CommonData(profile, following, followers)
    with pytest.raises(BasicProfileDataNotFound):
        assert data1.profile_preprocessing()
        
def test1_preprocessing():
    """Test to check if the data are correct. In this case, they are so the
        method will return them."""
    profile = {'username':'lidia', 'name':'Lidia', 'email':'lidia@lidia.es'}
    following = {'1':'Ana Ortiz', '2':'Eva García'}
    followers = {'1':'Ana Ortiz', '2':'Paloma Peña'}
    data1 = commondata.CommonData(profile, following, followers)
    assert type(data1.preprocessing()) == dict

def test2_preprocessing():
    """Test to check if the data are correct. In this case, they're not because
        the profile doesn't exist, so the method will raise an exception."""
    profile = {}
    following = {'1':'Ana Ortiz', '2':'Eva García'}
    followers = {'1':'Ana Ortiz', '2':'Paloma Peña'}
    data1 = commondata.CommonData(profile, following, followers)
    with pytest.raises(ProfileNotFound):
        assert data1.preprocessing()