#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains all methods used to analyze media social data from a specific user.
These methods are:
    - Sentiment analyzer for post comments.

@author: Lidia Sánchez Mérida
"""

import os
from monkeylearn import MonkeyLearn # MonkeyLearn cloud to access to a Sentiment Classifier
from exceptions import APIKeyNotFound, ModelIdNotFound, CommentsListNotFound \
    , CommentsDictNotFound

class DataAnalyzer:
    
    def sentiment_analyzer(self, data):
        """Method to analyze the sentiments of the post comments of a specific user.
            It counts the number of positive, neutral and negative comments for each
            user who has written a comment. Example of the result:
                {'user1':{'positive':4, 'neutral':2, 'negative':1} """
        # Check the API Key for the MonkeyLearn API
        api_key = os.environ.get("API_KEY_MONKEYLEARN")
        if (type(api_key) != str or api_key == ""):
            raise APIKeyNotFound("ERROR. The MonkeyLearn API key should be a non empty string.")
        # Check the model id
        model_id = os.environ.get("MODEL_ID_MONKEYLEARN")
        if (type(model_id) != str or model_id == ""):
            raise ModelIdNotFound("ERROR. The model id of the MonkeyLearn API should be a non empty string.")
        # Check the list of comments
        if (type(data) != list or len(data) == 0):
            raise CommentsListNotFound("ERROR. The comments to analyze should be a non empty list.")
        # Check each comment (user, preproc_comment)
        list_users = []
        shown_users = []
        list_comments = []
        for comment in data:
            if ('user' not in comment or 'preproc_comment' not in comment):
                raise CommentsDictNotFound("ERROR. Each comment should be a dict like {'user':'username', 'preproc_comment:'text'}")
            
            """Initialize the list of the users with the number of positive, neutral and
                negative comments to 0 without duplicates."""
            list_comments.append(comment['preproc_comment'])
            if (comment['user'] not in shown_users):
                shown_users.append(comment['user'])
                list_users.append({comment['user']:{'positive':0, 'neutral':0, 'negative':0}})
    
        """Post comments Sentiment Analysis"""
        ml = MonkeyLearn(api_key)
        results = (ml.classifiers.classify(model_id, list_comments)).body # Body of the response
        
        """Count the number of positive, neutral and negative comments for each user in order
            to get 'haters', friends, and so on."""
        for i in range(0, len(list_comments)):
            user = data[i]['user']
            sentiment = (results[i]['classifications'][0]['tag_name']).lower()
            for record in list_users:
                if (user in record):
                    record[user][sentiment] += 1
            
        return list_users
