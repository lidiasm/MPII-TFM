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
        self.tables = ['profiles', 'medias', 'mediacomments', 'mediatitles', 'mediacontent',
                       
                       'profilesevolution', 'profiles_profilesevolution',
                       'profilesactivity', 'profiles_profilesactivity',
                       'mediasevolution', 'medias_mediasevolution', 'mediaspopularity',
                       'sentimentanalysis', 'titlesentimentanalysis',
                       
                       'testparent', 'testchild', 'testfk', 
                       'testprofiles', 'testprofilesevolution', 'testprofiles_testprofilesevolution',
                       'testprofilesactivity', 'testprofiles_testprofilesactivity',
                       'testmedias', 'testmediasevolution', 'testmedias_testmediasevolution', 
                       'testmediaspopularity', 'testmedias_testmediaspopularity',
                       'testmediacomments', 'testmediatitles', 'testmediacontent',
                       'testsentimentanalysis', 'testtitlesentimentanalysis']
        # Connect to the database
        self.connect_to_database()
        
        ## PREDEFINED QUERIES
        # Select queries, to get data from the database
        self.select_queries = {
            ########################### TEST TABLES ###########################
            'check_test_parent':{
                'query':'SELECT id FROM testparent WHERE id=%s',
                'fields':['id']},
            'check_test_child':{
                'query':'SELECT id FROM testchild WHERE name=%s',
                'fields':['name']},
            'check_test_fk':{
                'query':'SELECT id_test_fk FROM testfk WHERE id=%s AND field_one=%s',
                'fields':['id', 'field_one']},
            
            # Test Profiles
            'check_test_profile':{
                'query':"SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s AND date=%s",
                'fields':['username', 'social_media', 'date']},
            'test_get_profiles':{
                'query':'SELECT id_profile, date, n_medias, n_followers, n_followings FROM testprofiles WHERE '+
                    'username=%s AND social_media=%s AND date>=%s AND date<=%s',
                'fields':['username', 'social_media', 'date_ini', 'date_fin']},
            'test_get_profiles_activity':{
                'query':'SELECT id_profile, date, n_medias FROM testprofiles WHERE '+
                    'username=%s AND social_media=%s AND date>=%s AND date<=%s',
                'fields':['username', 'social_media', 'date_ini', 'date_fin']},
            # Test Profiles Evolution analysis
            'check_test_profile_evolution':{
                'query':'SELECT id_profile_evolution FROM testprofilesevolution WHERE date_ini=%s AND date_fin=%s',
                'fields':["date_ini", "date_fin"]},
            'check_test_profile_profile_evolution':{
                'query':'SELECT id_profile_evolution FROM testprofiles_testprofilesevolution WHERE '+
                'id_profile=%s AND id_profile_evolution=%s',
                'fields':["id_profile", "id_profile_evolution"]},
            'test_profile_evolution':{
                'query':'SELECT date_ini, date_fin, mean_medias, mean_followers, mean_followings '+
                        'FROM testprofilesevolution WHERE date_ini>=%s AND date_fin <= %s AND id_profile_evolution '+
                        'IN (SELECT id_profile_evolution FROM testprofiles_testprofilesevolution WHERE id_profile '+
                        'IN (SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s))',
                'fields':['date_ini', 'date_fin', 'username', 'social_media']},
            # Test Profiles Activity analysis
            'check_test_profile_activity':{
                'query':'SELECT id_profile_activity FROM testprofilesactivity WHERE date_ini=%s AND date_fin=%s',
                'fields':["date_ini", "date_fin"]},
            'check_test_profile_profile_activity':{
                'query':'SELECT id_profile_activity FROM testprofiles_testprofilesactivity WHERE '+
                'id_profile=%s AND id_profile_activity=%s',
                'fields':["id_profile", "id_profile_activity"]},
            'test_profile_activity':{
                'query':'SELECT date_ini, date_fin, mean_medias '+
                        'FROM testprofilesactivity WHERE date_ini>=%s AND date_fin <= %s AND id_profile_activity '+
                        'IN (SELECT id_profile_activity FROM testprofiles_testprofilesactivity WHERE id_profile '+
                        'IN (SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s))',
                'fields':['date_ini', 'date_fin', 'username', 'social_media']},
            
            # Test Medias
            'check_test_media':{
                'query':'SELECT id_media_aut FROM testmedias WHERE id_media=%s AND date=%s',
                'fields':['id_media', 'date']
            },
            'test_get_medias':{
                'query':"SELECT id_media_aut, date, like_count, comment_count FROM testmedias "+
                    "WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s)",
                'fields':['date_ini', 'date_fin', 'username', 'social_media'],
            },
            # Test MediaComments
            'check_test_medias_for_comment':{
                'query':"SELECT id_media_aut FROM testmedias WHERE type='common' AND id_media=%s AND date=%s AND id_profile IN "+
                    "(SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s)",
                'fields':['id_media', 'date', 'username', 'social_media'],
            },
            'check_test_media_comment':{
                'query':"SELECT id_text FROM testmediacomments WHERE type='comment' AND text=%s AND author=%s AND id_media_aut=%s",
                'fields':["text", "author", "id_media_aut"]
            },
            'test_get_media_comment':{
                'query':"SELECT id_text, text FROM testmediacomments WHERE type='comment' AND date >= %s AND date <= %s AND id_media_aut IN "+
                    "(SELECT id_media_aut FROM testmedias WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s))",
                'fields':["comment_date_ini", "comment_date_fin", "media_date_ini", "media_date_fin", "username", "social_media"]
            },
            # Test MediaTitles
            'check_test_media_title':{
                'query':"SELECT id_text FROM testmediatitles WHERE type='title' AND id_media_aut=%s AND text=%s AND author=%s",
                'fields':['id_media_aut', 'text', 'author']
            },
            'test_get_media_title':{
                'query':"SELECT id_text, text FROM testmediatitles WHERE type='title' AND id_media_aut=%s AND author=%s",
                'fields':['id_media_aut', 'author']
            },
            'test_get_media_title_for_sentiment':{
                'query':"SELECT id_text, text FROM testmediatitles WHERE type='title' AND date >= %s AND date <= %s AND id_media_aut IN "+
                    "(SELECT id_media_aut FROM testmedias WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s))",
                'fields':["comment_date_ini", "comment_date_fin", "media_date_ini", "media_date_fin", "username", "social_media"]
            },
            # Test Medias Evolution analysis
            'check_test_media_evolution':{
                'query':'SELECT id_media_evolution FROM testmediasevolution WHERE date_ini=%s AND date_fin=%s',
                'fields':['date_ini', 'date_fin']
            },
            'check_test_media_media_evolution':{
                'query':'SELECT id_media_aut FROM testmedias_testmediasevolution WHERE id_media_evolution=%s AND id_media_aut=%s',
                'fields':['id_media_evolution', 'id_media_aut']
            },
            'test_media_evolution':{
                'query':'SELECT date_ini, date_fin, mean_likes, mean_comments FROM testmediasevolution '+
                    'WHERE date_ini>=%s AND date_fin<=%s AND id_media_evolution IN '+
                    '(SELECT id_media_evolution FROM testmedias_testmediasevolution WHERE id_media_aut IN '+
                    '(SELECT id_media_aut FROM testmedias WHERE id_profile IN '+
                    '(SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s)))',
                'fields':['date_ini', 'date_fin', 'username', 'social_media']
            },
            # Test Medias Popularity analysis
            'check_test_media_media_popularity':{
                'query':'SELECT id_media_aut FROM testmedias_testmediaspopularity WHERE id_media_popularity=%s AND id_media_aut=%s',
                'fields':['id_media_popularity', 'id_media_aut']
            },
            'test_get_medias_popularity':{
                'query':"SELECT id_media_aut, id_media, like_count, comment_count FROM testmedias "+
                    "WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s)",
                'fields':['date_ini', 'date_fin', 'username', 'social_media'],
            },
            'test_get_medias_for_popularity':{
                'query':"SELECT id_media_aut, uploaded_date FROM testmedias WHERE id_media_aut=%s AND type='common'",
                'fields':['id_media_aut']
            },
            'test_media_popularity':{
                'query':'SELECT date_ini, date_fin, mean_likes, mean_comments FROM testmediaspopularity '+
                    'WHERE date_ini>=%s AND date_fin<=%s AND id_media_popularity IN '+
                    '(SELECT id_media_popularity from testmedias_testmediaspopularity WHERE id_media_aut IN '+
                    '(SELECT id_media_aut FROM testmedias WHERE id_profile IN '+
                    '(SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s)))',
                'fields':['date_ini', 'date_fin', 'username', 'social_media']
            },
            # Test Sentiment Analysis 
            'check_test_sentiment_analysis':{
                'query':"SELECT id_text FROM testsentimentanalysis WHERE id_text=%s",
                'fields':["id_text"]
            },
            'test_comment_sentiment_analysis':{
                'query':"SELECT GREATEST(pos_degree, neu_degree, neg_degree), sentiment FROM testsentimentanalysis WHERE id_text IN "+
                    "(SELECT id_text FROM testmediacomments WHERE type='comment' AND date>=%s AND date<=%s AND id_media_aut IN "+
                    "(SELECT id_media_aut FROM testmedias WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s)))",
                'fields':["media_date_ini", "media_date_fin", "comment_date_ini", "comment_date_fin", "username", "social_media"]
            },
            'check_test_title_sentiment_analysis':{
                'query':"SELECT id_text FROM testtitlesentimentanalysis WHERE id_text=%s",
                'fields':["id_text"]
            },
            'test_title_sentiment_analysis':{
                'query':"SELECT GREATEST(pos_degree, neu_degree, neg_degree), sentiment FROM testsentimentanalysis WHERE id_text IN "+
                    "(SELECT id_text FROM testmediatitles WHERE type='comment' AND date>=%s AND date<=%s AND id_media_aut IN "+
                    "(SELECT id_media_aut FROM testmedias WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s)))",
                'fields':["media_date_ini", "media_date_fin", "comment_date_ini", "comment_date_fin", "username", "social_media"]
            },
            # Test UsersBehaviours
            'test_comment_users_behaviours':{
                'query':"SELECT id_text, date, author FROM testmediacomments WHERE date>=%s AND date<=%s AND type='comment' AND id_media_aut IN "+
                    "(SELECT id_media_aut FROM testmedias WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM testprofiles WHERE username=%s AND social_media=%s))",
                'fields':["comment_date_ini", "comment_date_fin", "media_date_ini", "media_date_fin", "username", "social_media"],
            },
            'test_sentiment_users_behaviours':{
                'query':"SELECT sentiment FROM testsentimentanalysis WHERE id_text=%s",
                'fields':["id_text"]
            },
    
            ########################### REAL TABLES ###########################
            # For Profiles table
            'check_profile':{
                'query':'SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s AND date=%s',
                'fields':['username', 'social_media', 'date']},
            'get_profiles':{
                'query':'SELECT id_profile, date, n_medias, n_followers, n_followings FROM profiles WHERE '+
                    'username=%s AND social_media=%s AND date>=%s AND date<=%s',
                'fields':['username', 'social_media', 'date_ini', 'date_fin']},
            'get_profiles_activity':{
                'query':'SELECT id_profile, date, n_medias FROM profiles WHERE '+
                    'username=%s AND social_media=%s AND date>=%s AND date<=%s',
                'fields':['username', 'social_media', 'date_ini', 'date_fin']},
            # For ProfilesEvolution tables
            'check_profile_evolution':{
                'query':'SELECT id_profile_evolution FROM profilesevolution WHERE date_ini=%s AND date_fin=%s',
                'fields':["date_ini", "date_fin"]},
            'check_profile_profile_evolution':{
                'query':'SELECT id_profile_evolution FROM profiles_profilesevolution WHERE '+
                'id_profile=%s AND id_profile_evolution=%s',
                'fields':["id_profile", "id_profile_evolution"]},
            'profile_evolution':{
                'query':'SELECT date_ini, date_fin, mean_medias, mean_followers, mean_followings '+
                        'FROM profilesevolution WHERE date_ini>=%s AND date_fin <= %s AND id_profile_evolution '+
                        'IN (SELECT id_profile_evolution FROM profiles_profilesevolution WHERE id_profile '+
                        'IN (SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s))',
                'fields':['date_ini', 'date_fin', 'username', 'social_media']},
            # For Profiles Activity tables
            'check_profile_activity':{
                'query':'SELECT id_profile_activity FROM profilesactivity WHERE date_ini=%s AND date_fin=%s',
                'fields':["date_ini", "date_fin"]},
            'check_profile_profile_activity':{
                'query':'SELECT id_profile_activity FROM profiles_profilesactivity WHERE '+
                'id_profile=%s AND id_profile_activity=%s',
                'fields':["id_profile", "id_profile_activity"]},
            'profile_activity':{
                'query':'SELECT date_ini, date_fin, mean_medias '+
                        'FROM profilesactivity WHERE date_ini>=%s AND date_fin <= %s AND id_profile_activity '+
                        'IN (SELECT id_profile_activity FROM profiles_profilesactivity WHERE id_profile '+
                        'IN (SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s))',
                'fields':['date_ini', 'date_fin', 'username', 'social_media']},
            # For Medias table
            'check_media':{
                'query':'SELECT id_media_aut FROM medias WHERE id_media=%s AND date=%s',
                'fields':['id_media', 'date']
            },
            'get_medias':{
                'query':"SELECT id_media_aut, date, like_count, comment_count FROM medias "+
                    "WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s)",
                'fields':['date_ini', 'date_fin', 'username', 'social_media'],
            },
            # For MediaComments
            'check_medias_for_comment':{
                'query':"SELECT id_media_aut FROM medias WHERE type='common' AND id_media=%s AND date=%s AND id_profile IN "+
                    "(SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s)",
                'fields':['id_media', 'date', 'username', 'social_media'],
            },
            'check_media_comment':{
                'query':"SELECT id_text FROM mediacomments WHERE type='comment' AND text=%s AND author=%s AND id_media_aut=%s",
                'fields':["text", "author", "id_media_aut"]
            },
            'get_media_comment':{
                'query':"SELECT id_text, text FROM mediacomments WHERE type='comment' AND date >= %s AND date <= %s AND id_media_aut IN "+
                    "(SELECT id_media_aut FROM medias WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s))",
                'fields':["comment_date_ini", "comment_date_fin", "media_date_ini", "media_date_fin", "username", "social_media"]
            },
            # For MediaTitles table
            'check_media_title':{
                'query':"SELECT id_text FROM mediatitles WHERE type='comment' AND id_media_aut=%s AND text=%s AND author=%s",
                'fields':['id_media_aut', 'text', 'author']
            },
            'get_media_title':{
                'query':"SELECT id_text, text FROM mediatitles WHERE type='title' AND id_media_aut=%s AND author=%s",
                'fields':['id_media_aut', 'author']
            },
            # For Medias Evolution tables
            'check_media_evolution':{
                'query':'SELECT id_media_evolution FROM mediasevolution WHERE date_ini=%s AND date_fin=%s',
                'fields':['date_ini', 'date_fin']
            },
            'check_media_media_evolution':{
                'query':'SELECT id_media_aut FROM medias_mediasevolution WHERE id_media_evolution=%s AND id_media_aut=%s',
                'fields':['id_media_evolution', 'id_media_aut']
            },
            'media_evolution':{
                'query':'SELECT date_ini, date_fin, mean_likes, mean_comments FROM mediasevolution '+
                    'WHERE date_ini>=%s AND date_fin<=%s AND id_media_evolution IN '+
                    '(SELECT id_media_evolution FROM medias_mediasevolution WHERE id_media_aut IN '+
                    '(SELECT id_media_aut FROM medias WHERE id_profile IN '+
                    '(SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s)))',
                'fields':['date_ini', 'date_fin', 'username', 'social_media']
            },
            # For Medias Popularity tables
            'check_media_media_popularity':{
                'query':'SELECT id_media_aut FROM medias_mediaspopularity WHERE id_media_popularity=%s AND id_media_aut=%s',
                'fields':['id_media_popularity', 'id_media_aut']
            },
            'get_medias_popularity':{
                'query':"SELECT id_media_aut, id_media, like_count, comment_count FROM medias "+
                    "WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s)",
                'fields':['date_ini', 'date_fin', 'username', 'social_media'],
            },
            'get_medias_for_popularity':{
                'query':"SELECT id_media_aut, uploaded_date FROM medias WHERE id_media_aut=%s AND type='common'",
                'fields':['id_media_aut']
            },
            'media_popularity':{
                'query':'SELECT date_ini, date_fin, mean_likes, mean_comments FROM mediaspopularity '+
                    'WHERE date_ini>=%s AND date_fin<=%s AND id_media_popularity IN '+
                    '(SELECT id_media_popularity from medias_mediaspopularity WHERE id_media_aut IN '+
                    '(SELECT id_media_aut FROM medias WHERE id_profile IN '+
                    '(SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s)))',
                'fields':['date_ini', 'date_fin', 'username', 'social_media']
            },
            # For Comment Sentiment Analysis
            'check_sentiment_analysis':{
                'query':"SELECT id_text FROM sentimentanalysis WHERE id_text=%s",
                'fields':["id_text"]
            },
            'comment_sentiment_analysis':{
                'query':"SELECT GREATEST(pos_degree, neu_degree, neg_degree), sentiment FROM sentimentanalysis WHERE id_text IN "+
                    "(SELECT id_text FROM mediacomments WHERE type='comment' AND date>=%s AND date<=%s AND id_media_aut IN "+
                    "(SELECT id_media_aut FROM medias WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s)))",
                'fields':["media_date_ini", "media_date_fin", "comment_date_ini", "comment_date_fin", "username", "social_media"]
            },
            # For Title Sentiment Analysis
            'check_title_sentiment_analysis':{
                'query':"SELECT id_text FROM titlesentimentanalysis WHERE id_text=%s",
                'fields':["id_text"]
            },
            'get_media_title_for_sentiment':{
                'query':"SELECT id_text, text FROM mediatitles WHERE type='title' AND date >= %s AND date <= %s AND id_media_aut IN "+
                    "(SELECT id_media_aut FROM medias WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s))",
                'fields':["comment_date_ini", "comment_date_fin", "media_date_ini", "media_date_fin", "username", "social_media"]
            },
            'title_sentiment_analysis':{
                'query':"SELECT GREATEST(pos_degree, neu_degree, neg_degree), sentiment FROM titlesentimentanalysis WHERE id_text IN "+
                    "(SELECT id_text FROM mediacomments WHERE type='comment' AND date>=%s AND date<=%s AND id_media_aut IN "+
                    "(SELECT id_media_aut FROM medias WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s)))",
                'fields':["media_date_ini", "media_date_fin", "comment_date_ini", "comment_date_fin", "username", "social_media"]
            },
            # For Users Behaviours
            'comment_users_behaviours':{
                'query':"SELECT id_text, date, author FROM mediacomments WHERE date>=%s AND date<=%s AND type='comment' AND id_media_aut IN "+
                    "(SELECT id_media_aut FROM medias WHERE type='common' AND date>=%s AND date<=%s AND id_profile IN "+
                    "(SELECT id_profile FROM profiles WHERE username=%s AND social_media=%s))",
                'fields':["comment_date_ini", "comment_date_fin", "media_date_ini", "media_date_fin", "username", "social_media"],
            },
            'sentiment_users_behaviours':{
                'query':"SELECT sentiment FROM sentimentanalysis WHERE id_text=%s",
                'fields':["id_text"]
            }
        }
        # Insert queries, to add new data to the database
        self.insert_queries = {
            ########################### TEST TABLES ###########################
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
            # Insert into TestProfiles table
            'insert_test_profile':{
                'query':"INSERT INTO testprofiles (biography, birthday, date, date_joined, "+
                    "gender, location, n_followers, n_followings, n_medias, name, profile_pic, "+
                    "social_media, userid, username) VALUES (%s, %s, %s, %s, %s, "+
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_profile",
                'fields':['biography', 'birthday', 'date', 'date_joined', 'gender', 
                          'location', 'n_followers', 'n_followings', 'n_medias', 
                          'name', 'profile_pic', 'social_media', 'userid', 'username'],
                'table':'testprofiles'},
            # Insert into TestProfilesEvolution tables
            'insert_test_profile_evolution':{
                'query':"INSERT INTO testprofilesevolution (date_fin, date_ini, mean_followers, "+
                         " mean_followings, mean_medias) VALUES (TO_DATE(%s,'DD-MM-YYYY'), TO_DATE(%s,'DD-MM-YYYY'), %s, %s, %s) RETURNING id_profile_evolution",
                'fields':['date_fin', 'date_ini', 'mean_followers', 'mean_followings', 'mean_medias'],
                'table':'testprofilesevolution'
                },
            'insert_test_profile_test_profile_evolution':{
                'query':"INSERT INTO testprofiles_testprofilesevolution (id_profile, id_profile_evolution) "+
                         "VALUES (%s, %s) RETURNING id_profile, id_profile_evolution",
                'fields':["id_profile", "id_profile_evolution"],
                'table':'testprofiles_testprofilesevolution'
                },
            # Insert into TestProfilesActivity tables
            'insert_test_profile_activity':{
                'query':"INSERT INTO testprofilesactivity (date_fin, date_ini, mean_medias) "+
                         "VALUES (TO_DATE(%s,'DD-MM-YYYY'), TO_DATE(%s,'DD-MM-YYYY'), %s) RETURNING id_profile_activity",
                'fields':['date_fin', 'date_ini', 'mean_medias'],
                'table':'testprofilesactivity'
                },
            'insert_test_profile_test_profile_activity':{
                'query':"INSERT INTO testprofiles_testprofilesactivity (id_profile, id_profile_activity) "+
                         "VALUES (%s, %s) RETURNING id_profile, id_profile_activity",
                'fields':["id_profile", "id_profile_activity"],
                'table':'testprofiles_testprofilesactivity'
                },
            # Insert into TestMedias table
            'insert_test_medias':{
                'query':"INSERT INTO testmedias (comment_count, date, id_media, id_profile, like_count, uploaded_date, type) "+
                    "VALUES (%s, %s, %s, %s, %s, TO_DATE(%s,'DD-MM-YYYY'), 'common') RETURNING id_media_aut",
                'fields':['comment_count', 'date', 'id_media', 'id_profile', 'like_count', 'uploaded_date'],
                'table':'testmedias'
            },
            # Insert into TestMediaComments table
            'insert_test_media_comments':{
                'query':"INSERT INTO testmediacomments (author, date, id_media_aut, text, type) VALUES (%s, %s, %s, %s, 'comment') "+
                    "RETURNING id_text",
                'fields':['author', 'date', 'id_media_aut', 'text'],
                'table':'testmediacomments'
            },
            # Insert into TestMediaTitles table
            'insert_test_media_titles':{
                'query':"INSERT INTO testmediatitles (author, date, id_media_aut, text, type) VALUES (%s, %s, %s, %s, 'title') "
                    "RETURNING id_text",
                'fields':['author', 'date', 'id_media_aut', 'text'],
                'table':'testmediatitles'
            },
            # Insert into TestMediasEvolution tables
            'insert_test_medias_evolution':{
                'query':'INSERT INTO testmediasevolution (date_fin, date_ini, mean_comments, mean_likes) '+
                    'VALUES (%s, %s, %s, %s) RETURNING id_media_evolution',
                'fields':['date_fin', 'date_ini', 'mean_comments', 'mean_likes'],
                'table':'testmediasevolution'
            },
            'insert_test_medias_test_medias_evolution':{
                'query':'INSERT INTO testmedias_testmediasevolution (id_media_aut, id_media_evolution) '+
                    'VALUES (%s, %s) RETURNING id_media_aut, id_media_evolution',
                'fields':['id_media_aut', 'id_media_evolution'],
                'table':'testmedias_testmediasevolution'
            },
            # Insert into TestMediasPopularity table
            'insert_test_medias_popularity':{
                'query':"INSERT INTO testmediaspopularity (date_fin, date_ini, mean_likes, mean_comments) "+
                    "VALUES (TO_DATE(%s,'DD-MM-YYYY'), TO_DATE(%s,'DD-MM-YYYY'), %s, %s) RETURNING id_media_popularity",
                'fields':['date_fin', 'date_ini', 'mean_comments', 'mean_likes'],
                'table':'testmediaspopularity'
            },
            'insert_test_medias_test_medias_popularity':{
                'query':'INSERT INTO testmedias_testmediaspopularity (id_media_aut, id_media_popularity) '+
                    'VALUES (%s, %s) RETURNING id_media_aut, id_media_popularity',
                'fields':['id_media_aut', 'id_media_popularity'],
                'table':'testmedias_testmediaspopularity'
            },
            # Insert into TestSentimentAnalysis
            'insert_test_sentiment_analysis':{
                'query':"INSERT INTO testsentimentanalysis (id_text, neg_degree, neu_degree, pos_degree, sentiment) "+
                    "VALUES (%s, %s, %s, %s, %s) RETURNING id_text",
                'fields':["id_text", "neg_degree", "neu_degree", "pos_degree", "sentiment"],
                'table':"testsentimentanalysis"
            },
            'insert_test_title_sentiment_analysis':{
                'query':"INSERT INTO testtitlesentimentanalysis (id_text, neg_degree, neu_degree, pos_degree, sentiment) "+
                    "VALUES (%s, %s, %s, %s, %s) RETURNING id_text",
                'fields':["id_text", "neg_degree", "neu_degree", "pos_degree", "sentiment"],
                'table':"testtitlesentimentanalysis"
            },
            
            ########################### REAL TABLES ###########################
            'insert_profile':{
                'query':"INSERT INTO profiles (biography, birthday, date, date_joined, "+
                    "gender, location, n_followers, n_followings, n_medias, name, profile_pic, "+
                    "social_media, userid, username) VALUES (%s, %s, %s, %s, %s, "+
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_profile",
                'fields':['biography', 'birthday', 'date', 'date_joined', 'gender', 
                          'location', 'n_followers', 'n_followings', 'n_medias', 
                          'name', 'profile_pic', 'social_media', 'userid', 'username'],
                'table':'profiles'},
            'insert_profile_evolution':{
                'query':"INSERT INTO profilesevolution (date_fin, date_ini, mean_followers, "+
                         " mean_followings, mean_medias) VALUES (TO_DATE(%s,'DD-MM-YYYY'), TO_DATE(%s,'DD-MM-YYYY'), %s, %s, %s) RETURNING id_profile_evolution",
                'fields':['date_fin', 'date_ini', 'mean_followers', 'mean_followings', 'mean_medias'],
                'table':'profilesevolution'
                },
            'insert_profile_profile_evolution':{
                'query':"INSERT INTO profiles_profilesevolution (id_profile, id_profile_evolution) "+
                         "VALUES (%s, %s) RETURNING id_profile, id_profile_evolution",
                'fields':["id_profile", "id_profile_evolution"],
                'table':'profiles_profilesevolution'
                },
            # Insert into ProfilesActivity tables
            'insert_profile_activity':{
                'query':"INSERT INTO profilesactivity (date_fin, date_ini, mean_medias) "+
                         "VALUES (TO_DATE(%s,'DD-MM-YYYY'), TO_DATE(%s,'DD-MM-YYYY'), %s) RETURNING id_profile_activity",
                'fields':['date_fin', 'date_ini', 'mean_medias'],
                'table':'profilesactivity'
                },
            'insert_profile_profile_activity':{
                'query':"INSERT INTO profiles_profilesactivity (id_profile, id_profile_activity) "+
                         "VALUES (%s, %s) RETURNING id_profile, id_profile_activity",
                'fields':["id_profile", "id_profile_activity"],
                'table':'profiles_profilesactivity'
                },
            # Insert into Medias table
            'insert_medias':{
                'query':"INSERT INTO medias (comment_count, date, id_media, id_profile, like_count, uploaded_date, type) "+
                    "VALUES (%s, %s, %s, %s, %s, TO_DATE(%s,'DD-MM-YYYY'), 'common') RETURNING id_media_aut",
                'fields':['comment_count', 'date', 'id_media', 'id_profile', 'like_count', 'uploaded_date'],
                'table':'medias'
            },
            # Insert into MediaTitles table
            'insert_media_titles':{                
                'query':"INSERT INTO mediatitles (author, date, id_media_aut, text, type) VALUES (%s, %s, %s, %s, 'title') "
                    "RETURNING id_text",
                'fields':['author', 'date', 'id_media_aut', 'text'],
                'table':'mediatitles'
            },
            # Insert into MediaComments table
            'insert_media_comments':{
                'query':"INSERT INTO mediacomments (author, date, id_media_aut, text, type) VALUES (%s, %s, %s, %s, 'comment') "+
                    "RETURNING id_text",
                'fields':['author', 'date', 'id_media_aut', 'text'],
                'table':'mediacomments'
            },
            # Insert into MediasEvolution tables
            'insert_medias_evolution':{
                'query':'INSERT INTO mediasevolution (date_fin, date_ini, mean_comments, mean_likes) '+
                    'VALUES (%s, %s, %s, %s) RETURNING id_media_evolution',
                'fields':['date_fin', 'date_ini', 'mean_comments', 'mean_likes'],
                'table':'mediasevolution'
            },
            'insert_medias_medias_evolution':{
                'query':'INSERT INTO medias_mediasevolution (id_media_aut, id_media_evolution) '+
                    'VALUES (%s, %s) RETURNING id_media_aut, id_media_evolution',
                'fields':['id_media_aut', 'id_media_evolution'],
                'table':'medias_mediasevolution'
            },
            # Insert into MediasPopularity table
            'insert_medias_popularity':{
                'query':"INSERT INTO mediaspopularity (date_fin, date_ini, mean_likes, mean_comments) "+
                    "VALUES (TO_DATE(%s,'DD-MM-YYYY'), TO_DATE(%s,'DD-MM-YYYY'), %s, %s) RETURNING id_media_popularity",
                'fields':['date_fin', 'date_ini', 'mean_comments', 'mean_likes'],
                'table':'mediaspopularity'
            },
            'insert_medias_medias_popularity':{
                'query':'INSERT INTO medias_mediaspopularity (id_media_aut, id_media_popularity) '+
                    'VALUES (%s, %s) RETURNING id_media_aut, id_media_popularity',
                'fields':['id_media_aut', 'id_media_popularity'],
                'table':'medias_mediaspopularity'
            },
            # Insert into SentimentAnalysis
            'insert_sentiment_analysis':{
                'query':"INSERT INTO sentimentanalysis (id_text, neg_degree, neu_degree, pos_degree, sentiment) "+
                    "VALUES (%s, %s, %s, %s, %s) RETURNING id_text",
                'fields':["id_text", "neg_degree", "neu_degree", "pos_degree", "sentiment"],
                'table':"sentimentanalysis"
            },
            'insert_title_sentiment_analysis':{
                'query':"INSERT INTO titlesentimentanalysis (id_text, neg_degree, neu_degree, pos_degree, sentiment) "+
                    "VALUES (%s, %s, %s, %s, %s) RETURNING id_text",
                'fields':["id_text", "neg_degree", "neu_degree", "pos_degree", "sentiment"],
                'table':"titlesentimentanalysis"
            },
        }
        # Check queries to make before inserting new data
        self.check_queries = {
            ## Test queries
            'insert_test_parent':'check_test_parent',
            'insert_test_child':'check_test_child',
            'insert_test_fk':'check_test_fk',
            # For Profiles
            'insert_test_profile':'check_test_profile',
            # For ProfileEvolution
            'insert_test_profile_evolution':"check_test_profile_evolution",
            'insert_test_profile_test_profile_evolution':"check_test_profile_profile_evolution",
            # For ProfileActivity
            'insert_test_profile_activity':'check_test_profile_activity',
            'insert_test_profile_test_profile_activity':"check_test_profile_profile_activity",
            # For Medias
            'insert_test_medias':'check_test_media',
            # For MediaEvolution
            'insert_test_medias_evolution':"check_test_media_evolution",
            'insert_test_medias_test_medias_evolution':"check_test_media_media_evolution",
            # For MediaPopularity
            'insert_test_medias_test_medias_popularity':"check_test_media_media_popularity",
            # For MediaTitles
            'insert_test_media_titles':'check_test_media_title',
            # For MediaComments
            'insert_test_media_comments':'check_test_media_comment',
            # For SentimentAnalysis
            'insert_test_sentiment_analysis':'check_test_sentiment_analysis',
            'insert_test_title_sentiment_analysis':'check_test_title_sentiment_analysis',
            
            'delete_test_parent':'check_test_parent',
            'delete_test_child':'check_test_child',
            'delete_test_fk':'check_test_fk',
            
            ## Real queries
            # For Profiles
            'insert_profile':'check_profile',
            'insert_profile_evolution':"check_profile_evolution",
            'insert_profile_profile_evolution':"check_profile_profile_evolution",
            'insert_profile_activity':'check_profile_activity',
            'insert_profile_profile_activity':"check_profile_profile_activity",
            # For Medias
            'insert_medias':'check_media',
            'insert_medias_evolution':"check_media_evolution",
            'insert_medias_medias_evolution':"check_media_media_evolution",
            'insert_medias_medias_popularity':"check_media_media_popularity",
            'insert_sentiment_analysis':'check_sentiment_analysis',
            'insert_title_sentiment_analysis':'check_title_sentiment_analysis',
            # For MediaTitles
            'insert_media_titles':'check_media_title',
            # For MediaComments
            'insert_media_comments':'check_media_comment',
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
        
        print("LONG", len(check_values))
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