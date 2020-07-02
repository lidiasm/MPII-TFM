#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File in which there are many tests to check the behaviour of the methods contained
in the class DataAnalyzer. Each one performs a different type of data analysis.

@author: Lidia Sánchez Mérida
"""
import os
import sys
import pytest
sys.path.append("src")
sys.path.append("src/data")
import data_analyzer 
from exceptions import APIKeyNotFound, ModelIdNotFound, CommentsListNotFound \
    , CommentsDictNotFound

"""Store the right key and model id to connect to MonkeyLearn API and use their sentiment 
    classifier after set those variables to invalid values."""
api_key = os.environ["API_KEY_MONKEYLEARN"]
model_id = os.environ["MODEL_ID_MONKEYLEARN"]

"""DataAnalyzer object to run the data analyzer methods"""
da = data_analyzer.DataAnalyzer()

def test1_sentiment_analyzer():
    """Test to check the sentiment analyzer without providing the right API Key to
        use the MonkeyLearn sentiment classsifier. In order to do that, the env
        variable which stores the API key is set to a empty string. Then, it will raise an exception."""
    os.environ["API_KEY_MONKEYLEARN"] = ""
    with pytest.raises(APIKeyNotFound):
        assert da.sentiment_analyzer(None)

def test2_sentiment_analyzer():
    """Test to check the sentiment analyzer without providing the right model id to
        use the MonkeyLearn sentiment classsifier. In order to do that, the env
        variable which stores the model id is set to a empty string. Then, it will raise an exception."""
    # Set the right API Key for MonkeyLearn
    os.environ["API_KEY_MONKEYLEARN"] = api_key
    os.environ["MODEL_ID_MONKEYLEARN"] = ""
    with pytest.raises(ModelIdNotFound):
        assert da.sentiment_analyzer({})
        
def test3_sentiment_analyzer():
    """Test to check the sentiment analyzer without providing the right type of
        data to analyze. So it will raise an exception."""
    # Set the right model id for MonkeyLearn
    os.environ["MODEL_ID_MONKEYLEARN"] = model_id
    with pytest.raises(CommentsListNotFound):
        assert da.sentiment_analyzer({})
        
def test4_sentiment_analyzer():
    """Test to check the sentiment analyzer without providing the right type of
        data to analyze. So it will raise an exception."""
    comments = [{'user':'u1', 'preproc_comment':'alcohollll alcohol love friend'},
                {'user':'u2', 'comment':'drooling_face drooling_face drooling_face'}]
    with pytest.raises(CommentsDictNotFound):
        assert da.sentiment_analyzer(comments)
    
def test5_sentiment_analyzer():
    """Test to get the sentiments of the comments writen in the posts of a specific
        user in order to get different kinds of users, such as friends, haters, ...."""
    comments = [{'user':'u1', 'preproc_comment':'alcohollll alcohol love friend'},
                {'user':'u2', 'preproc_comment': 'drooling_face drooling_face drooling_face'},
                {'user':'u2', 'preproc_comment':'would come back'},
                {'user':'u2', 'preproc_comment':'handsome'},
                {'user':'u5', 'preproc_comment':'smiling_face_with_heart-eyes smiling_face_with_heart-eyes smiling_face_with_heart-eyes'}]
    result = da.sentiment_analyzer(comments)
    assert type(result) == list