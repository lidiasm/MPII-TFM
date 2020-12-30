#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which represents the Single Source of Truth and contains the operations
which can be done in the PostgreSQL database.
    - Insert a new item in a specific table, if it's not already.
    - Get the matched records related to a specific query.
    - Get the number of records or size from a table.

This class will be used by the classes which needs to operate with the PostgreSQL database.

@author: Lidia Sánchez Mérida
"""
import psycopg2
import os
from exceptions import InvalidDatabaseCredentials, InvalidTableName \
    , InvalidQuery, InvalidQueryValues

class PostgreDB:
    
    def __init__(self):
        """
        Creates a PostgreSQL object whose attributes are:
            - The name of the PostgreSQL database.
            - The tables of the database.
            - The connection and the cursor to make queries.
            - The avalaible queries to make.
            - The check queries to make in order to insert new data.

        Returns
        -------
        A PostgreSQL object with the connection to the PostgreSQL database.
        """
        # Database name
        self.database_name = "socialnetworksdb"
        # Tables of the database
        self.tables = ['testparent', 'testchild', 'testfk',
                       'testprofiles', 'testprofilesevolution','testprofilesactivity',
                       'testmedias', 'testmediasevolution', 'testmediaspopularity',
                       'testmediatitles', 'testmediacomments',
                       'testtextsentiments', 'testcommentsentiments', 'testuserbehaviours',
                       
                       'profiles', 'profilesevolution', 'profilesactivity',
                       'medias', 'mediasevolution', 'mediaspopularity',
                       'textsentiments', 'userbehaviours'
                       ]
        # Connect to the database
        self.connect_to_database()
        
        # Predefined queryies
        ## 1. SELECT QUERIES
        self.select_queries = {
            'check_test_parent':{
                'query':'SELECT id FROM testparent WHERE id=%s',
                'fields':['id']},
            'check_test_child':{
                'query':'SELECT id FROM testchild WHERE name=%s',
                'fields':['name']},
            'check_test_fk':{
                'query':'SELECT id_test_fk FROM testfk WHERE id=%s AND field_one=%s',
                'fields':['id', 'field_one']},
            
            ########################### TEST ANALYSIS ###################################
            # FOR PROFILES ANALYSIS
            ## Check if the profile to insert is already in the database
            'check_test_profile':{
                'query':"SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s AND date=%s",
                'fields':['username', 'social_media', 'date']},
            ## Get the required profiles for the ProfilesEvolution
            'test_get_profiles':{
                'query':'SELECT date, n_medias, n_followers, n_followings FROM testprofiles WHERE '+
                    'username=%s AND social_media=%s AND date>=%s AND date<=%s',
                'fields':['username', 'social_media', 'date_ini', 'date_fin']},
            ## Get the required profiles for the ProfilesActivity
            'test_get_nmedias_profiles':{
                'query':'SELECT date, n_medias FROM testprofiles WHERE '+
                    'username=%s AND social_media=%s AND date>=%s AND date<=%s',
                'fields':['username', 'social_media', 'date_ini', 'date_fin']},
            ## Check if the ProfilesEvolution analysis results are already in the database
            'check_test_profile_evolution':{
                'query':'SELECT id_profile_evolution FROM testprofilesevolution WHERE '+
                    'date_ini=%s AND date_fin=%s AND id_user=%s AND time=%s',
                'fields':["date_ini", "date_fin", "id_user", "time"]},
            ## Get the ProfilesEvolution analysis results of a specific range of dates and username
            'test_profile_evolution':{
                'query':'SELECT time, mean_followers, mean_followings, mean_medias FROM '+
                    'testprofilesevolution WHERE date_ini=%s AND date_fin=%s AND id_user=%s',
                'fields':["date_ini", "date_fin", "id_user"]
            },
            ## Check if the ProfilesActivity analysis results are already in the database
            'check_test_profile_activity':{
                'query':'SELECT id_profile_activity FROM testprofilesactivity WHERE '+
                    'date_ini=%s AND date_fin=%s AND id_user=%s AND time=%s',
                'fields':["date_ini", "date_fin", "id_user", "time"]},
            ## Get the ProfilesActivity analysis results of a specific range of dates and username
            'test_profile_activity':{
                'query':'SELECT time, mean_medias FROM testprofilesactivity WHERE '+
                    'date_ini=%s AND date_fin=%s AND id_user=%s',
                'fields':["date_ini", "date_fin", "id_user"]
            },
            
            # FOR MEDIAS ANALYSIS 
            ## Check if the media to insert is already in the database
            'check_test_media':{
                'query':'SELECT id_media_aut FROM testmedias WHERE id_media=%s AND date=%s',
                'fields':['id_media', 'date']
            },
            # Get the required medias to perform a MediasEvolution analysis
            'test_get_medias':{
                'query':"SELECT date, like_count, comment_count FROM testmedias "+
                    "WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s)",
                'fields':['date_ini', 'date_fin', 'username', 'social_media'],
            },
            # Get the required medias to perform a MediasPopularity analysis
            'test_get_medias_with_id':{
                'query':"SELECT id_media, like_count, comment_count FROM testmedias "+
                    "WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s)",
                'fields':['date_ini', 'date_fin', 'username', 'social_media'],
            },
            # Check if a specific comment is already in the database before inserting it
            'check_test_media_comment':{
                'query':"SELECT id_text FROM testmediacomments WHERE type='comment' AND original_text=%s AND author=%s AND id_media_aut=%s",
                'fields':["original_text", "author", "id_media_aut"]
            },
            # Get the required comments to perform a CommentsSentiments analysis
            'test_get_media_comments':{
                'query':"SELECT id_text, preprocessed_text, original_text FROM testmediacomments WHERE type='comment' AND date >= %s AND date <= %s AND id_media_aut IN "+
                    "(SELECT id_media_aut FROM testmedias WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s))",
                'fields':["comment_date_ini", "comment_date_fin", "media_date_ini", "media_date_fin", "username", "social_media"]
            },
            # Check if the media title to insert is already in the database
            'check_test_media_title':{
                'query':"SELECT id_text FROM testmediatitles WHERE type='title' AND id_media_aut=%s AND original_text=%s AND author=%s",
                'fields':['id_media_aut', 'original_text', 'author']
            },
            # Get the required comments to perform a CommentsSentiments analysis
            'test_get_media_titles':{
                'query':"SELECT id_text, preprocessed_text, original_text FROM testmediatitles WHERE type='title' AND date >= %s AND date <= %s AND id_media_aut IN "+
                    "(SELECT id_media_aut FROM testmedias WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s))",
                'fields':["comment_date_ini", "comment_date_fin", "media_date_ini", "media_date_fin", "username", "social_media"]
            },
            # Check if there are any MediasEvolution analysis results which are similar to
            # the new results to insert
            'check_test_media_evolution':{
                'query':'SELECT id_media_evolution FROM testmediasevolution WHERE '+
                    'date_ini=%s AND date_fin=%s AND id_user=%s AND time=%s',
                'fields':['date_ini', 'date_fin', "id_user", "time"]
            },
            # Get the MediasEvolution analysis results to plot them directly
            'test_media_evolution':{
                'query':'SELECT time, mean_likes, mean_comments FROM testmediasevolution '+
                    'WHERE date_ini=%s AND date_fin=%s AND id_user=%s',
                'fields':['date_ini', 'date_fin', 'id_user']
            },
            # Check if there are any MediasPopularity analysis results which are similar to
            # the new results to insert
            'check_test_media_popularity':{
                'query':'SELECT id_media_popularity FROM testmediaspopularity WHERE '+
                    'date_ini=%s AND date_fin=%s AND id_user=%s AND id_media=%s',
                'fields':['date_ini', 'date_fin', "id_user", "id_media"]
            },
            # Get the MediasPopularity analysis results to plot them directly
            'test_media_popularity':{
                'query':'SELECT mean_likes, mean_comments FROM testmediaspopularity '+
                    'WHERE date_ini=%s AND date_fin=%s AND id_user=%s',
                'fields':['date_ini', 'date_fin', 'id_user']
            },
            # Check if there is a similar SentimentAnalysis before inserting the new one
            'check_test_sentiment_analysis':{
                'query':"SELECT id_text_sentiment FROM testtextsentiments WHERE "+
                    "date_ini=%s AND date_fin=%s AND id_user=%s AND type=%s",
                'fields':["date_ini", "date_fin", "id_user", "type"]
            },
            # Get the CommentSentiment analysis results to plot them directly
            'test_comment_sentiment_analysis':{
                'query':"SELECT n_pos, n_neu, n_neg, pos_degree, neu_degree, neg_degree FROM testtextsentiments "+
                    "WHERE date_ini=%s AND date_fin=%s AND id_user=%s AND type='comments'",
                'fields':["date_ini", "date_fin", "id_user"]
            },
            # Check if a text sentiment analysis already exists
            'check_test_comment_sentiment':{
                'query':'SELECT id_comment_sentiment FROM testcommentsentiments WHERE original_text=%s',
                'fields':["original_text"]
            },
            # Get the CommentSentiment analysis results to plot them directly
            'test_title_sentiment_analysis':{
                'query':"SELECT n_pos, n_neu, n_neg, pos_degree, neu_degree, neg_degree FROM testtextsentiments "+
                    "WHERE date_ini=%s AND date_fin=%s AND id_user=%s AND type='titles'",
                'fields':["date_ini", "date_fin", "id_user"]
            },
            # Get the analysed comments as well as their authors to study their behaviours
            'test_get_comments_and_authors':{
                'query':"SELECT date, author, original_text FROM testmediacomments WHERE type='comment' "+
                    "AND date>=%s AND date<=%s AND id_media_aut IN "+
                    "(SELECT id_media_aut FROM testmedias WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s))",
                'fields':["comment_date_ini", "comment_date_fin", "media_date_ini", "media_date_fin",
                          "username", "social_media"]
            },
            # Get the sentiment from a analysed comment 
            'test_get_comment_sentiment':{
                'query':"SELECT sentiment FROM testcommentsentiments WHERE original_text=%s",
                'fields':["original_text"]
            },
            # Check if there are similar UserBehaviours analysis before inserting a new one
            'check_test_user_behaviour':{
                'query':"SELECT id_user_behaviour FROM testuserbehaviours WHERE "+
                    "date_ini=%s AND date_fin=%s AND id_user=%s AND time=%s",
                'fields':["date_ini", "date_fin", "id_user", "time"]
            },
            # Get the UserBehaviours analysis results to plot them directly
            'test_user_behaviours':{
                'query':'SELECT time, n_likers, n_haters FROM testuserbehaviours WHERE '+
                    'date_ini=%s AND date_fin=%s AND id_user=%s',
                'fields':['date_ini', 'date_fin', 'id_user']
            },
            
            ############################### REAL ANALYSIS ##################################
            # FOR PROFILES_EVOLUTION AND PROFILES_ACTIVITY
            ## Check if the profile to insert is already in the database
            'check_profile':{
                'query':"SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s AND date=%s",
                'fields':['username', 'social_media', 'date']},
            ## Get the required profiles for the ProfilesEvolution
            'get_profiles':{
                'query':'SELECT date, n_medias, n_followers, n_followings FROM profiles WHERE '+
                    'username=%s AND social_media=%s AND date>=%s AND date<=%s',
                'fields':['username', 'social_media', 'date_ini', 'date_fin']},
            ## Get the required profiles for the ProfilesActivity
            'get_nmedias_profiles':{
                'query':'SELECT date, n_medias FROM profiles WHERE '+
                    'username=%s AND social_media=%s AND date>=%s AND date<=%s',
                'fields':['username', 'social_media', 'date_ini', 'date_fin']},
            ## Check if the ProfilesEvolution analysis results are already in the database
            'check_profile_evolution':{
                'query':'SELECT id_profile_evolution FROM profilesevolution WHERE '+
                    'date_ini=%s AND date_fin=%s AND id_user=%s AND time=%s',
                'fields':["date_ini", "date_fin", "id_user", "time"]},
            ## Get the ProfilesEvolution analysis results of a specific range of dates and username
            'profile_evolution':{
                'query':'SELECT time, mean_followers, mean_followings, mean_medias FROM '+
                    'profilesevolution WHERE date_ini=%s AND date_fin=%s AND id_user=%s',
                'fields':["date_ini", "date_fin", "id_user"]
            },
            ## Check if the ProfilesActivity analysis results are already in the database
            'check_profile_activity':{
                'query':'SELECT id_profile_activity FROM profilesactivity WHERE '+
                    'date_ini=%s AND date_fin=%s AND id_user=%s AND time=%s',
                'fields':["date_ini", "date_fin", "id_user", "time"]},
            ## Get the ProfilesActivity analysis results of a specific range of dates and username
            'profile_activity':{
                'query':'SELECT time, mean_medias FROM profilesactivity WHERE '+
                    'date_ini=%s AND date_fin=%s AND id_user=%s',
                'fields':["date_ini", "date_fin", "id_user"]
            },
            
            # FOR MEDIAS ANALYSIS 
            ## Check if the media to insert is already in the database
            'check_media':{
                'query':'SELECT id_media_aut FROM medias WHERE id_media=%s AND date=%s',
                'fields':['id_media', 'date']
            },
            # Get the required medias to perform a MediasEvolution analysis
            'get_medias':{
                'query':"SELECT date, like_count, comment_count FROM medias "+
                    "WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s)",
                'fields':['date_ini', 'date_fin', 'username', 'social_media'],
            },
            # Get the required medias to perform a MediasPopularity analysis
            'get_medias_with_id':{
                'query':"SELECT id_media, like_count, comment_count FROM medias "+
                    "WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s)",
                'fields':['date_ini', 'date_fin', 'username', 'social_media'],
            },
            # Check if a specific comment is already in the database before inserting it
            'check_media_comment':{
                'query':"SELECT id_text FROM mediacomments WHERE type='comment' AND original_text=%s AND author=%s AND id_media_aut=%s",
                'fields':["original_text", "author", "id_media_aut"]
            },
            # Get the required comments to perform a CommentsSentiments analysis
            'get_media_comments':{
                'query':"SELECT id_text, preprocessed_text, original_text FROM mediacomments WHERE type='comment' AND date >= %s AND date <= %s AND id_media_aut IN "+
                    "(SELECT id_media_aut FROM medias WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s))",
                'fields':["comment_date_ini", "comment_date_fin", "media_date_ini", "media_date_fin", "username", "social_media"]
            },
            # Check if the media title to insert is already in the database
            'check_media_title':{
                'query':"SELECT id_text FROM mediatitles WHERE type='title' AND id_media_aut=%s AND original_text=%s AND author=%s",
                'fields':['id_media_aut', 'original_text', 'author']
            },
            # Get the required comments to perform a CommentsSentiments analysis
            'get_media_titles':{
                'query':"SELECT id_text, preprocessed_text, original_text FROM mediatitles WHERE type='title' AND date >= %s AND date <= %s AND id_media_aut IN "+
                    "(SELECT id_media_aut FROM medias WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s))",
                'fields':["comment_date_ini", "comment_date_fin", "media_date_ini", "media_date_fin", "username", "social_media"]
            },
            # Check if there are any MediasEvolution analysis results which are similar to
            # the new results to insert
            'check_media_evolution':{
                'query':'SELECT id_media_evolution FROM mediasevolution WHERE '+
                    'date_ini=%s AND date_fin=%s AND id_user=%s AND time=%s',
                'fields':['date_ini', 'date_fin', "id_user", "time"]
            },
            # Get the MediasEvolution analysis results to plot them directly
            'media_evolution':{
                'query':'SELECT time, mean_likes, mean_comments FROM mediasevolution '+
                    'WHERE date_ini=%s AND date_fin=%s AND id_user=%s',
                'fields':['date_ini', 'date_fin', 'id_user']
            },
            # Check if there are any MediasPopularity analysis results which are similar to
            # the new results to insert
            'check_media_popularity':{
                'query':'SELECT id_media_popularity FROM mediaspopularity WHERE '+
                    'date_ini=%s AND date_fin=%s AND id_user=%s AND id_media=%s',
                'fields':['date_ini', 'date_fin', "id_user", "id_media"]
            },
            # Get the MediasPopularity analysis results to plot them directly
            'media_popularity':{
                'query':'SELECT mean_likes, mean_comments FROM mediaspopularity '+
                    'WHERE date_ini=%s AND date_fin=%s AND id_user=%s',
                'fields':['date_ini', 'date_fin', 'id_user']
            },
            # Check if there is a similar SentimentAnalysis before inserting the new one
            'check_sentiment_analysis':{
                'query':"SELECT id_text_sentiment FROM textsentiments WHERE "+
                    "date_ini=%s AND date_fin=%s AND id_user=%s AND type=%s",
                'fields':["date_ini", "date_fin", "id_user", "type"]
            },
            # Get the CommentSentiment analysis results to plot them directly
            'comment_sentiment_analysis':{
                'query':"SELECT n_pos, n_neu, n_neg, pos_degree, neu_degree, neg_degree FROM textsentiments "+
                    "WHERE date_ini=%s AND date_fin=%s AND id_user=%s AND type='comments'",
                'fields':["date_ini", "date_fin", "id_user"]
            },
            # Check if a text sentiment analysis already exists
            'check_comment_sentiment':{
                'query':'SELECT id_comment_sentiment FROM commentsentiments WHERE original_text=%s',
                'fields':["original_text"]
            },
            # Get the CommentSentiment analysis results to plot them directly
            'title_sentiment_analysis':{
                'query':"SELECT n_pos, n_neu, n_neg, pos_degree, neu_degree, neg_degree FROM textsentiments "+
                    "WHERE date_ini=%s AND date_fin=%s AND id_user=%s AND type='titles'",
                'fields':["date_ini", "date_fin", "id_user"]
            },
            # Get the analysed comments as well as their authors to study their behaviours
            'get_comments_and_authors':{
                'query':"SELECT date, author, original_text FROM mediacomments WHERE type='comment' "+
                    "AND date>=%s AND date<=%s AND id_media_aut IN "+
                    "(SELECT id_media_aut FROM medias WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s))",
                'fields':["comment_date_ini", "comment_date_fin", "media_date_ini", "media_date_fin",
                          "username", "social_media"]
            },
            # Get the sentiment from a analysed comment 
            'get_comment_sentiment':{
                'query':"SELECT sentiment FROM commentsentiments WHERE original_text=%s",
                'fields':["original_text"]
            },
            # Check if there are similar UserBehaviours analysis before inserting a new one
            'check_user_behaviour':{
                'query':"SELECT id_user_behaviour FROM userbehaviours WHERE "+
                    "date_ini=%s AND date_fin=%s AND id_user=%s AND time=%s",
                'fields':["date_ini", "date_fin", "id_user", "time"]
            },
            # Get the UserBehaviours analysis results to plot them directly
            'user_behaviours':{
                'query':'SELECT time, n_likers, n_haters FROM userbehaviours WHERE '+
                    'date_ini=%s AND date_fin=%s AND id_user=%s',
                'fields':['date_ini', 'date_fin', 'id_user']
            },
        }
        
        ## 2. INSERT QUERIES
        self.insert_queries = {
            'insert_test_parent':{
                'query':'INSERT INTO testparent (id, is_parent, name) VALUES (%s, %s, %s) RETURNING id',
                'fields':['id', 'is_parent', 'name'],
                'table':'testparent'},
            'insert_test_child':{
                'query':'INSERT INTO testchild (id, is_parent, name) VALUES (%s, %s, %s) RETURNING id',
                'fields':['id', 'is_parent', 'name'],
                'table':'testchild'},
            'insert_test_fk':{
                'query':'INSERT INTO testfk (id, field_one) VALUES (%s, %s) RETURNING id_test_fk',
                'fields':['id', 'field_one'],
                'table':'testfk'},
            
            ############################ TEST ANALYSIS ####################################
            # FOR PROFILES_EVOLUTION AND PROFILES_ACTIVITY
            ## Insert the data of a specific user profile
            'insert_test_profile':{
                'query':"INSERT INTO testprofiles (biography, birthday, date, date_joined, "+
                    "gender, location, n_followers, n_followings, n_medias, name, profile_pic, "+
                    "social_media, userid, username) VALUES (%s, %s, %s, %s, %s, "+
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_profile",
                'fields':['biography', 'birthday', 'date', 'date_joined', 'gender', 
                          'location', 'n_followers', 'n_followings', 'n_medias', 
                          'name', 'profile_pic', 'social_media', 'userid', 'username'],
                'table':'testprofiles' 
            },
            # Insert the results of a specific ProfilesEvolution analysis
            'insert_test_profile_evolution':{
                'query':"INSERT INTO testprofilesevolution (date_fin, date_ini, id_user, mean_followers, "+
                         " mean_followings, mean_medias, time) VALUES (TO_DATE(%s,'DD-MM-YYYY'), "+
                         "TO_DATE(%s,'DD-MM-YYYY'), %s, %s, %s, %s, %s) RETURNING id_profile_evolution",
                'fields':['date_fin', 'date_ini', 'id_user', 'mean_followers', 'mean_followings', 'mean_medias', 'time'],
                'table':'testprofilesevolution'
            },
            # Insert the results of a specific ProfilesActivity analysis
            'insert_test_profile_activity':{
                'query':"INSERT INTO testprofilesactivity (date_fin, date_ini, id_user, mean_medias, time) "+
                         "VALUES (TO_DATE(%s,'DD-MM-YYYY'), TO_DATE(%s,'DD-MM-YYYY'), %s, %s, %s) RETURNING id_profile_activity",
                'fields':['date_fin', 'date_ini', 'id_user', 'mean_medias', 'time'],
                'table':'testprofilesactivity'
            },
            # Insert the data of the specific medias
            'insert_test_medias':{
                'query':"INSERT INTO testmedias (comment_count, date, id_media, id_profile, like_count, uploaded_date, type) "+
                    "VALUES (%s, %s, %s, %s, %s, TO_DATE(%s,'DD-MM-YYYY'), 'common') RETURNING id_media_aut",
                'fields':['comment_count', 'date', 'id_media', 'id_profile', 'like_count', 'uploaded_date'],
                'table':'testmedias'
            },
            # Insert the title of a specific media
            'insert_test_media_titles':{
                'query':"INSERT INTO testmediatitles (author, date, id_media_aut, original_text, preprocessed_text, type) "+
                    "VALUES (%s, %s, %s, %s, %s, 'title') RETURNING id_text",
                'fields':['author', 'date', 'id_media_aut', 'original_text', 'preprocessed_text'],
                'table':'testmediatitles'
            },
            # Insert a comment from a media
            'insert_test_media_comments':{
                'query':"INSERT INTO testmediacomments (author, date, id_media_aut, original_text, preprocessed_text, type) "+
                    "VALUES (%s, %s, %s, %s, %s, 'comment') RETURNING id_text",
                'fields':['author', 'date', 'id_media_aut', 'original_text', 'preprocessed_text'],
                'table':'testmediacomments'
            },
            # Insert the results of a specific MediasEvolution analysis
            'insert_test_medias_evolution':{
                'query':'INSERT INTO testmediasevolution (date_fin, date_ini, id_user, '+
                    'mean_comments, mean_likes, time) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_media_evolution',
                'fields':['date_fin', 'date_ini', 'id_user', 'mean_comments', 'mean_likes', 'time'],
                'table':'testmediasevolution'
            },
            # Insert the results of a specific MediasEvolution analysis
            'insert_test_medias_popularity':{
                'query':'INSERT INTO testmediaspopularity (date_fin, date_ini, id_media, id_user, '+
                    'mean_comments, mean_likes) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_media_popularity',
                'fields':['date_fin', 'date_ini', 'id_media', 'id_user', 'mean_comments', 'mean_likes'],
                'table':'mediasevolution'
            },
            # Insert the results of a specific CommentSentiment analysis
            'insert_test_sentiment_analysis':{
                'query':"INSERT INTO testtextsentiments (date_fin, date_ini, id_user, n_neg, n_neu, n_pos, neg_degree, neu_degree, pos_degree, type) "+
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_text_sentiment",
                'fields':['date_fin', 'date_ini', 'id_user', 'n_neg', 'n_neu', 'n_pos', 'neg_degree', 'neu_degree', 'pos_degree', 'type'],
                'table':"testtextsentiments"
            },
            # Insert the result of a specific CommentSentiment analysis
            'insert_test_comment_sentiment_analysis':{
                'query':"INSERT INTO testcommentsentiments (original_text, sentiment, degree) "+
                    "VALUES (%s, %s, %s) RETURNING id_comment_sentiment",
                'fields':['original_text', 'sentiment', 'degree'],
                'table':"testcommentsentiments"
            },
            # Insert the results of a new UserBehaviours analysis
            'insert_test_user_behaviour':{
                'query':"INSERT INTO testuserbehaviours (date_fin, date_ini, "+
                    "id_user, n_haters, n_likers, time) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_user_behaviour",
                'fields':["date_fin", "date_ini", "id_user", "n_haters", "n_likers", "time"],
                'table':"testuserbehaviours"
            },
            
            ###################################### REAL ANALYSIS ##################################
            # FOR PROFILES_EVOLUTION AND PROFILES_ACTIVITY
            ## Insert the data of a specific user profile
            'insert_profile':{
                'query':"INSERT INTO profiles (biography, birthday, date, date_joined, "+
                    "gender, location, n_followers, n_followings, n_medias, name, profile_pic, "+
                    "social_media, userid, username) VALUES (%s, %s, %s, %s, %s, "+
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_profile",
                'fields':['biography', 'birthday', 'date', 'date_joined', 'gender', 
                          'location', 'n_followers', 'n_followings', 'n_medias', 
                          'name', 'profile_pic', 'social_media', 'userid', 'username'],
                'table':'profiles' 
            },
            # Insert the results of a specific ProfilesEvolution analysis
            'insert_profile_evolution':{
                'query':"INSERT INTO profilesevolution (date_fin, date_ini, id_user, mean_followers, "+
                         " mean_followings, mean_medias, time) VALUES (TO_DATE(%s,'DD-MM-YYYY'), "+
                         "TO_DATE(%s,'DD-MM-YYYY'), %s, %s, %s, %s, %s) RETURNING id_profile_evolution",
                'fields':['date_fin', 'date_ini', 'id_user', 'mean_followers', 'mean_followings', 'mean_medias', 'time'],
                'table':'profilesevolution'
            },
            # Insert the results of a specific ProfilesActivity analysis
            'insert_profile_activity':{
                'query':"INSERT INTO profilesactivity (date_fin, date_ini, id_user, mean_medias, time) "+
                         "VALUES (TO_DATE(%s,'DD-MM-YYYY'), TO_DATE(%s,'DD-MM-YYYY'), %s, %s, %s) RETURNING id_profile_activity",
                'fields':['date_fin', 'date_ini', 'id_user', 'mean_medias', 'time'],
                'table':'profilesactivity'
            },
            # Insert the data of the specific medias
            'insert_medias':{
                'query':"INSERT INTO medias (comment_count, date, id_media, id_profile, like_count, uploaded_date, type) "+
                    "VALUES (%s, %s, %s, %s, %s, TO_DATE(%s,'DD-MM-YYYY'), 'common') RETURNING id_media_aut",
                'fields':['comment_count', 'date', 'id_media', 'id_profile', 'like_count', 'uploaded_date'],
                'table':'medias'
            },
            # Insert the title of a specific media
            'insert_media_titles':{
                'query':"INSERT INTO mediatitles (author, date, id_media_aut, original_text, preprocessed_text, type) "+
                    "VALUES (%s, %s, %s, %s, %s, 'title') RETURNING id_text",
                'fields':['author', 'date', 'id_media_aut', 'original_text', 'preprocessed_text'],
                'table':'mediatitles'
            },
            # Insert a comment from a media
            'insert_media_comments':{
                'query':"INSERT INTO mediacomments (author, date, id_media_aut, original_text, preprocessed_text, type) "+
                    "VALUES (%s, %s, %s, %s, %s, 'comment') RETURNING id_text",
                'fields':['author', 'date', 'id_media_aut', 'original_text', 'preprocessed_text'],
                'table':'mediacomments'
            },
            # Insert the results of a specific MediasEvolution analysis
            'insert_medias_evolution':{
                'query':'INSERT INTO mediasevolution (date_fin, date_ini, id_user, '+
                    'mean_comments, mean_likes, time) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_media_evolution',
                'fields':['date_fin', 'date_ini', 'id_user', 'mean_comments', 'mean_likes', 'time'],
                'table':'mediasevolution'
            },
            # Insert the results of a specific MediasEvolution analysis
            'insert_medias_popularity':{
                'query':'INSERT INTO mediaspopularity (date_fin, date_ini, id_media, id_user, '+
                    'mean_comments, mean_likes) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_media_popularity',
                'fields':['date_fin', 'date_ini', 'id_media', 'id_user', 'mean_comments', 'mean_likes'],
                'table':'mediasevolution'
            },
            # Insert the results of a specific CommentSentiment analysis
            'insert_sentiment_analysis':{
                'query':"INSERT INTO textsentiments (date_fin, date_ini, id_user, n_neg, n_neu, n_pos, neg_degree, neu_degree, pos_degree, type) "+
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_text_sentiment",
                'fields':['date_fin', 'date_ini', 'id_user', 'n_neg', 'n_neu', 'n_pos', 'neg_degree', 'neu_degree', 'pos_degree', 'type'],
                'table':"textsentiments"
            },
            # Insert the result of a specific CommentSentiment analysis
            'insert_comment_sentiment_analysis':{
                'query':"INSERT INTO commentsentiments (original_text, sentiment, degree) "+
                    "VALUES (%s, %s, %s) RETURNING id_comment_sentiment",
                'fields':['original_text', 'sentiment', 'degree'],
                'table':"commentsentiments"
            },
            # Insert the results of a new UserBehaviours analysis
            'insert_user_behaviour':{
                'query':"INSERT INTO userbehaviours (date_fin, date_ini, "+
                    "id_user, n_haters, n_likers, time) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_user_behaviour",
                'fields':["date_fin", "date_ini", "id_user", "n_haters", "n_likers", "time"],
                'table':"userbehaviours"
            },
        }
        
        # 3. INSERT-SELECT QUERIES
        self.check_queries = {
            'insert_test_parent':'check_test_parent',
            'insert_test_child':'check_test_child',
            'insert_test_fk':'check_test_fk',
            
            ######################### TEST ANALYSIS #########################
            # FOR PROFILES ANALYSIS
            'insert_test_profile':'check_test_profile',
            'insert_test_profile_evolution':"check_test_profile_evolution",
            'insert_test_profile_activity':"check_test_profile_activity",
            # FOR MEDIAS ANALYSIS
            'insert_test_medias':'check_test_media',
            'insert_test_media_titles':'check_test_media_title',
            'insert_test_media_comments':'check_test_media_comment',
            'insert_test_medias_evolution':"check_test_media_evolution",
            'insert_test_medias_popularity':"check_test_media_popularity",
            # FOR SENTIMENT ANALYSIS
            'insert_test_comment_sentiment_analysis':'check_test_comment_sentiment',
            'insert_test_sentiment_analysis':'check_test_sentiment_analysis',
            # FOR USER BEHAVIOURS ANALYSIS
            'insert_test_user_behaviour':'check_test_user_behaviour',
            
            ######################### REAL ANALYSIS #########################
            # FOR PROFILES ANALYSIS
            'insert_profile':'check_profile',
            'insert_profile_evolution':"check_profile_evolution",
            'insert_profile_activity':"check_profile_activity",
            # FOR MEDIAS ANALYSIS
            'insert_medias':'check_media',
            'insert_media_titles':'check_media_title',
            'insert_media_comments':'check_media_comment',
            'insert_medias_evolution':"check_media_evolution",
            'insert_medias_popularity':"check_media_popularity",
            # FOR SENTIMENT ANALYSIS
            'insert_comment_sentiment_analysis':'check_comment_sentiment',
            'insert_sentiment_analysis':'check_sentiment_analysis',
            # FOR USER BEHAVIOURS ANALYSIS
            'insert_user_behaviour':'check_user_behaviour',
        }
        
    def connect_to_database(self):
        """
        Makes the connection to the database through the environment variables which
        contains the credentials.

        Raises
        ------
        InvalidDatabaseCredentials
            If the credentials are not non-empty strings or are incorrect.

        Returns
        -------
        The cursor object which allows to make the queries.
        """
        # Get the PostgreSQL credentials
        user = os.environ.get("POSTGRES_USER") 
        pswd = os.environ.get("POSTGRES_PSWD")
        # Check the provided credentials
        if (type(user) != str or user == "" or type(pswd) != str or pswd == ""):
            raise InvalidDatabaseCredentials("ERROR. The PostgreSQL credentials should be non-empty strings.")
        # Try to connect to the database        
        try:
            self.connection = psycopg2.connect(host="localhost", user=user, 
                               password=pswd, database=self.database_name, port="5433")
            self.cursor = self.connection.cursor()
            return self.cursor
        except Exception: # pragma no cover
            raise InvalidDatabaseCredentials("ERROR. The provided PostgreSQL credentials are wrong.")
    
    def get_data(self, query, values={}):
        """
        Makes a predefined query in a specific table and returns the matched records.
        In order to prevent SQL injection, non-predefined queries will not be allowed.

        Parameters
        ----------
        query : str
            It's the predefined query to make.
        values : dict
            It's the dict which contains the values to make the provided query.
            It could be not provided if the query does not need any additional parameters.
        
        Raises
        ------
        InvalidQuery
            If the provided query is not a non-empty string or is not one of the defined queries.
        InvalidQueryValues
            If the provided values for the selected query are not valid.

        Returns
        -------
        A tuple of lists with the matched results and the values of the specific
        chosen fields.
        """
        # Check the provided predefined query
        if (type(query) != str or query == ""):
            raise InvalidQuery("ERROR. The query should be a non-empty string.")
        # Check if the provided query exists
        if (query not in self.select_queries):
            raise InvalidQuery("ERROR. The provided query does not exist.")
        # Check if the query needs some values and if they've been provided
        if (len(self.select_queries[query]['fields']) > 0 and (type(values) != dict or len(values) == 0)):
            raise InvalidQueryValues("ERROR. The selected query needs values and they've not been provided.")
            
        # Check if all the provided values are required
        query_fields = self.select_queries[query]['fields']
        value_fields = list(values.keys())
        if (query_fields != value_fields):
            raise InvalidQueryValues("ERROR. Some of the required values are missing or are wrong.")
    
        # Make the final query
        try: 
            self.cursor.execute(self.select_queries[query]['query'], list(values.values()))
            matches = self.cursor.fetchall()
        except: #pragma no cover
            self.connect_to_database()
            self.cursor.execute(self.select_queries[query]['query'], list(values.values()))
            matches = self.cursor.fetchall()
        
        return matches
    
    def get_table_size(self, table):
        """
        Gets the number of records of the provided table. In order to do that, 
        'count()' operation will be used to make a query which returns the number
        of rows of the table.

        Parameters
        ----------
        table : str
            It's the table name whose size is going to be get.

        Raises
        ------
        TableNotFound
            If the table name is not a non-empty string or does not exist in the
            PostgreSQL database.

        Returns
        -------
        An integer which is the number of records of the specified table.
        """
        # Check the specified table name
        if (type(table) != str or table == ""):
            raise InvalidTableName("ERROR. The table name should be a non-empty string.")
        # Check if the provided table exists
        if (table.lower() not in self.tables):
            raise InvalidTableName("ERROR. The provided table name does not exist in the PostgreSQL database.")

        query = "SELECT count(*) FROM "+table
        try:
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        except: #pragma no cover
            self.connect_to_database()
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        
    def insert_data(self, query, new_values, check_values=[]):
        """
        Inserts new records in a specific table if the new item does not already
        exist. Each table will have its own inserted conditions.

        Parameters
        ----------
        query : str
            It's the inserted query to make.
        new_values : list of dicts
            It's the list which contains the new items to insert in different dicts.
            In this way, one or multiple items could be inserted.
        check_values : list of dicts
            It's the list which contains the values related to each data sample to
            insert in order to check if it's already in the database.
        
        Raises
        ------
        InvalidQuery
            If the provided query is not a non-empty string or is not one of the insert queries.
        InvalidQueryValues
            If the provided values for the insert query are not valid.

        Returns
        -------
        A list of tuples which contains the id or the several ids returned from the
        inserted queries in a specific table in the Postgres database.
        """
        # Check the provided query
        if (type(query) != str or query == ""):
            raise InvalidQuery("ERROR. The provided query should be a non-empty string.")
        # Check if the provided query exists
        if (query not in self.insert_queries):
            raise InvalidQuery("ERROR. The provided query is not valid.")
        # Check the new values    
        if (type(new_values) != list or len(new_values) == 0 or 
            not all(isinstance(item, dict) for item in new_values)):
            raise InvalidQueryValues("ERROR. The new values should be a non-empty list of dicts")
        keys_new_values = [True for item in new_values if (list(item.keys()) == self.insert_queries[query]['fields'])]
        if (len(keys_new_values) != len (new_values)):
            raise InvalidQueryValues("ERROR. There are some missing keys in the new values.")
        
        # Check the check values, if they are provided
        data_to_insert = new_values
        if (len(check_values) > 0):
            if (type(check_values) != list or not all(isinstance(item, dict) for item in check_values)):
                raise InvalidQueryValues("ERROR. The new and select values should be non-empty list of dicts.")
            # Check if the new values has the same length than the check values
            if (len(new_values) != len(check_values)):
                raise InvalidQueryValues("ERROR. The new and select values should have the same size.")
            # Check the keys for the new values
            keys_check_values = [True for item in check_values if (list(item.keys()) == self.select_queries[self.check_queries[query]]['fields'])]
            if (len(keys_check_values) != len(check_values)):
                raise InvalidQueryValues("ERROR. There are some missing keys in the select values.")
            
            # Check if the new item to insert is already in the table
            data_to_insert = []
            for i in range(0, len(check_values)):
                result = self.get_data(self.check_queries[query], check_values[i])
                if (len(result) == 0):
                    data_to_insert.append(new_values[i])
                
        ## IMPORTANT!!
        # Insert only the data samples which are not already in the database
        new_ids = []
        for item in data_to_insert:
            try:
                self.cursor.execute(self.insert_queries[query]['query'], list(item.values()))
                self.connection.commit()
                result = list(self.cursor.fetchone())
                new_ids.extend(result)
            except: 
                raise InvalidQueryValues("ERROR. The new data couldn't be inserted.")
        
        return new_ids
    
    def empty_table(self, table):
        """
        Deletes all the records stored in a specific table without removing it.
        In this way, the table will be empty.

        Parameters
        ----------
        table : str
            It's the table name to make empty.

        Raises
        ------
        InvalidTable
            If the provided table name is not a non-empty string or does not exist
            in the database.

        Returns
        -------
        True if the table is now empty, False if it's not.
        """
        # Check the table name provided
        if (type(table) != str or table == ""):
            raise InvalidTableName("ERROR. The table name should be a non-empty list.")
        # Check that the table exists
        if (table.lower() not in self.tables):
            raise InvalidTableName("ERROR. The provided table name does not exist in the database.")
        
        # Deletes all records from the table
        query = "DELETE FROM "+table
        self.cursor.execute(query)
        return self.get_table_size(table) == 0