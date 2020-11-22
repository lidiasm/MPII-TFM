#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests to check the methods of the class MainOperations.

@author: Lidia Sánchez Mérida
"""
from datetime import datetime
import sys
import pytest
sys.path.append('src')
import main_ops 
from exceptions import UsernameNotFound, MaxRequestsExceed, UserDataNotFound \
    , InvalidMongoDbObject, InvalidSocialMediaSource, InvalidMode, InvalidAnalysis \
    , InvalidDates, CollectionNotFound, InvalidQuery, InvalidAnalysisResults
    
# MainOperations object to perform the tests
main_ops_object = main_ops.MainOperations()
# Username to get his user data from Instagram
username = "pablo_cuevas15"
        
def test1_get_user_instagram_common_data():
    """
    Test to check the method which gets, preprocesses and stores user data using the
    LevPasha Instagram API without providing the username. It will raise an exception.
    """
    with pytest.raises(UsernameNotFound):
        assert main_ops_object.get_user_instagram_common_data('', None)
        
def test2_get_user_instagram_common_data():
    """
    Test to check the method which gets, preprocesses and stores user data using the
    LevPasha Instagram API without providing a valid mode to insert the user data
    in the Mongo database. It will raise an exception.
    """
    with pytest.raises(InvalidMode):
        assert main_ops_object.get_user_instagram_common_data(username, "invalid_mode")
        
def test3_get_user_instagram_common_data():
    """
    Test to check the method which gets, preprocesses and stores user data using the
    LevPasha Instagram API. In this test, the collection to insert the user data
    will be the 'test' collection.
    """
    try:
        user_data = main_ops_object.get_user_instagram_common_data(username, "test")
        assert type(user_data) == dict
    except MaxRequestsExceed:
        print("Max requests exceed. Wait to send more.")
        
def test1_preprocess_and_store_common_data():
    """
    Test to check the method which preprocesses and stores user data from any
    social media source without providing the user data. An exception will be raised.
    """
    with pytest.raises(UserDataNotFound):
        assert main_ops_object.preprocess_and_store_common_data(None, None, None)
        
def test2_preprocess_and_store_common_data():
    """
    Test to check the method which preprocesses and stores user data from any
    social media source without providing the social media source. An exception will be raised.
    """
    with pytest.raises(InvalidSocialMediaSource):
        assert main_ops_object.preprocess_and_store_common_data({'id':'first id'}, None, None)
        
def test3_preprocess_and_store_common_data():
    """
    Test to check the method which preprocesses and stores user data from any
    social media source without providing a valid social media source. An exception will be raised.
    """
    with pytest.raises(InvalidSocialMediaSource):
        assert main_ops_object.preprocess_and_store_common_data({'id':'first id'}, 'Random', None)
        
def test4_preprocess_and_store_common_data():
    """
    Test to check the method which preprocesses and stores user data from any
    social media source without providing a valid mode to insert the user data
    in the Mongo database. An exception will be raised.
    """
    with pytest.raises(InvalidMode):
        assert main_ops_object.preprocess_and_store_common_data({'id':'first id'}, 'Instagram', 'invalid_mode')
        
def test5_preprocess_and_store_common_data():
    """
    Test to check the method which preprocesses and stores user data from any social
    media source without providing a valid MongoDB. In order to do that, the 
    MongoDB object is set to a invalid value, so an exception will be raised.
    """
    mo = main_ops.MainOperations()
    mo.mongodb_object = ""
    with pytest.raises(InvalidMongoDbObject):
        assert mo.preprocess_and_store_common_data({'id':'first id'}, 'Instagram', 'test')

def test6_preprocess_and_store_common_data():
    """
    Test to preprocess and store user data in the Mongo database from any 
    social media source.
    """
    profile = {"userid" : 123456789, "username" : "lidia.96.sm", "name" : "Lidia Sánchez",
                "biography" : "\"Si eres valiente para empezar, eres fuerte para acabar.\" Ingeniería Informática.",
                "gender" : "None", "profile_pic" : "https://instagram_example", 
                "location" : "None", "birthday" : "None", "date_joined" : "None", 
                "n_followers" : 61, "n_followings":45, "n_medias" : 6}
    medias = [{'id_media': '1', "taken_at":"24/10/2020", "title":None, 'url':None, 'like_count': 29, 'comment_count': 14}, 
              {'id_media': '2', "taken_at":"24/10/2020", "title":None, 'url':None,'like_count': 18, 'comment_count': 0}]
    texts = [{'id_media': '1', 
              'texts': [{'user': 'user1', 'text': 'aa'}, {'user': 'user2', 'text': 'ee'}]},
              {'id_media': '2', 
              'texts': [{'user': 'user3', 'text': 'ii'}, {'user': 'user2', 'text': 'oo'}]}]
    user_data = {'profile':profile, 'medias':medias, 'comments':texts}
    mo = main_ops.MainOperations()
    result = mo.preprocess_and_store_common_data(user_data, 'Instagram', 'test')
    assert type(result) == dict

def test1_get_data_from_mongodb():
    """
    Test to check the method which gets user data from the Mongo database depending on
    the provided range of dates. In this test, the username of the studied user is
    not provided so an exception will be raised.
    """
    with pytest.raises(UsernameNotFound):
        assert main_ops_object.get_data_from_mongodb(None, None, None, None)
        
def test2_get_data_from_mongodb():
    """
    Test to check the method which gets user data from the Mongo database depending on
    the provided range of dates. In this test, the social media source is
    not provided so an exception will be raised.
    """
    with pytest.raises(InvalidSocialMediaSource):
        assert main_ops_object.get_data_from_mongodb(username, None, None, None)
        
def test3_get_data_from_mongodb():
    """
    Test to check the method which gets user data from the Mongo database depending on
    the provided range of dates. In this test, the provided social media source is
    not valid so an exception will be raised.
    """
    with pytest.raises(InvalidSocialMediaSource):
        assert main_ops_object.get_data_from_mongodb(username, "InvalidSocialMedia", None, None)

def test4_get_data_from_mongodb():
    """
    Test to check the method which gets user data from the Mongo database depending on
    the provided range of dates. In this test, the range of dates is
    not provided so an exception will be raised.
    """
    with pytest.raises(CollectionNotFound):
        assert main_ops_object.get_data_from_mongodb(username, "Instagram", None, None)

def test5_get_data_from_mongodb():
    """
    Test to check the method which gets user data from the Mongo database depending on
    the provided range of dates. In this test, the provided range of date is not valid
    so an exception will be raised.
    """
    with pytest.raises(InvalidDates):
        assert main_ops_object.get_data_from_mongodb(username, "Instagram", "test", None)

def test6_get_data_from_mongodb():
    """
    Test to check the method which gets user data from the Mongo database depending on
    the provided range of dates. In this test, the provided range of date is not valid
    so an exception will be raised.
    """
    with pytest.raises(InvalidDates):
        assert main_ops_object.get_data_from_mongodb(username, "Instagram", "test", [(1,2,3)])

def test7_get_data_from_mongodb():
    """
    Test to check the method which gets user data from the Mongo database depending on
    the provided range of dates. In this test, the provided range of date is not valid
    so an exception will be raised.
    """
    with pytest.raises(InvalidDates):
        assert main_ops_object.get_data_from_mongodb(username, "Instagram", "test", [(1,2)])

def test8_get_data_from_mongodb():
    """
    Test to check the method which gets user data from the Mongo database depending on
    the provided range of dates. In this test, the provided range of date is not valid
    so an exception will be raised.
    """
    date_list = [("24-10-2020", "28/10/2020")]
    with pytest.raises(InvalidDates):
        assert main_ops_object.get_data_from_mongodb(username, "Instagram", "test", date_list)

def test9_get_data_from_mongodb():
    """
    Test to check the method which gets user data from the Mongo database depending on
    the provided range of dates. In this test, the provided range of date is not valid
    so an exception will be raised.
    """
    date_list = [("26-10-2020", "22-10-2020")]
    with pytest.raises(InvalidDates):
        assert main_ops_object.get_data_from_mongodb(username, "Instagram", "test", date_list)
        
def test10_get_data_from_mongodb():
    """
    Test to check the method which gets user data from the Mongo database depending on
    the provided range of dates. In this test, first a profile from a specific user is
    inserted in the Mongo database, if it's not already in, and then it's recovered
    by providing the username, the social media source, which in this case is Instagram,
    as well as the range of date, which in this case is only one day.
    """
    user_data = [
        {"userid" : "1121839441", "username" : "audispain", 
        "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", 
        "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=nS90OZW4faUAX9bEQzi&oh=fc5ceaaa72a7cc21a0185719616ea3b0&oe=5FCE818A", 
        "location" : "None", "birthday" : "None", "date_joined" : "None", 
        "n_followers" : "217094", "n_followings" : "430", "n_medias" : "1217", 
        "social_media" : "Instagram", "date" : datetime.strptime("05-11-2020",'%d-%m-%Y')},
        {"userid" : "1121839441", "username" : "audispain", 
        "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", 
        "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=nS90OZW4faUAX9bEQzi&oh=fc5ceaaa72a7cc21a0185719616ea3b0&oe=5FCE818A", 
        "location" : "None", "birthday" : "None", "date_joined" : "None", 
        "n_followers" : "217178", "n_followings" : "431", "n_medias" : "1219", 
        "social_media" : "Instagram", "date" : datetime.strptime("06-11-2020",'%d-%m-%Y')},
        {"userid" : "1121839441", "username" : "audispain", 
        "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", 
        "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=nS90OZW4faUAX9bEQzi&oh=fc5ceaaa72a7cc21a0185719616ea3b0&oe=5FCE818A", 
        "location" : "None", "birthday" : "None", "date_joined" : "None", 
        "n_followers" : "217299", "n_followings" : "431", "n_medias" : "1220", 
        "social_media" : "Instagram", "date" : datetime.strptime("07-11-2020",'%d-%m-%Y')}
        ]
    for item in user_data:
        main_ops_object.common_data_object.insert_user_data(item, "test")
        
    date_list = [("05-11-2020", "07-11-2020")]
    global mongo_data
    mongo_data = main_ops_object.get_data_from_mongodb("audispain", "Instagram", "test", date_list)
    assert type(mongo_data) == list and len(mongo_data) == 3
    
def test1_insert_data_to_postgres():
    """
    Test to check the method which inserts new user data to a specific table in
    the Postgres database. In this test, the related analysis to get the insert
    query is not provided so an exception will be raised.
    """
    with pytest.raises(InvalidQuery):
        assert main_ops_object.insert_data_to_postgres(None, None)
        
def test2_insert_data_to_postgres():
    """
    Test to check the method which inserts new user data to a specific table in
    the Postgres database. In this test, the user data is not provided so an 
    exception will be raised.
    """
    with pytest.raises(UserDataNotFound):
        assert main_ops_object.insert_data_to_postgres("test_profile_evolution", None)

def test3_insert_data_to_postgres():
    """
    Test to check the method which inserts new user data to a specific table in
    the Postgres database. In this test, there are three new user data samples to
    insert in the 'TestProfiles' table of the Postgres database. In order to always
    insert them, all the records of the table will be removed previously.
    """
    # Delete all the records of the Postgres table in order to insert the data
    main_ops_object.postgresdb_object.empty_table("testprofiles")
    global profile_ids
    profile_ids = main_ops_object.insert_data_to_postgres("insert_test_profile", mongo_data)
    assert len(profile_ids) == 3

def test1_get_data_from_postgresdb():
    """
    Test to check the method which gets user data from the Postgres database
    depending on the provided conditions. In this test, the select query is not
    provided so an exception will be raised.
    """
    with pytest.raises(InvalidQuery):
        assert main_ops_object.get_data_from_postgresdb(None, None)
        
def test2_get_data_from_postgresdb():
    """
    Test to check the method which gets user data from the Postgres database
    depending on the provided conditions. In this test, the select values are not
    provided so an exception will be raised.
    """
    with pytest.raises(UserDataNotFound):
        assert main_ops_object.get_data_from_postgresdb("test_get_profiles", None)
        
def test3_get_data_from_postgresdb():
    """
    Test to check the method which gets user data from the Postgres database
    depending on the provided conditions. In this test, the recovered data will be
    the same data samples which were inserted to the 'TestProfiles' table.
    """
    select_values = [{"username":"audispain", "social_media":"Instagram",
                      "date_ini":datetime.strptime("05-11-2020",'%d-%m-%Y'), 
                      "date_fin":datetime.strptime("07-11-2020",'%d-%m-%Y')}]
    matched_records = main_ops_object.get_data_from_postgresdb("test_get_profiles", select_values)
    assert len(matched_records["ids"]) == 3 and len(matched_records["data"]) == 3
    
def test1_insert_many_analysis_results():
    """
    Test to check the method which inserts the analysis results as well as the 
    ids from the involved data samples in the related tables of the Postgres database.
    In this test, none of the parameters are provided so an exception will be raised.
    """
    with pytest.raises(InvalidAnalysisResults):
        assert main_ops_object.insert_many_analysis_results(None, None, None, None)
        
def test2_insert_many_analysis_results():
    """
    Test to check the method which inserts the analysis results as well as the 
    ids from the involved data samples in the related tables of the Postgres database.
    In this test, the provided analysis results are not valid so an exception will be raised.
    """
    with pytest.raises(InvalidAnalysisResults):
        assert main_ops_object.insert_many_analysis_results("05-11-2020", "07-11-2020", 
                        "test_profile_evolution", {"id":"1"})

def test3_insert_many_analysis_results():
    """
    Test to check the method which inserts the analysis results as well as the 
    ids from the involved data samples in the related tables of the Postgres database.
    In this test, the provided analysis results will be inserted as well as the 
    involved profiles which helped to perform the 'ProfileEvolution' analysis.
    In order to run the test, the records of the two related tables will be deleted
    previously.
    """
    # Delete all the records of the Postgres table in order to insert the data
    main_ops_object.postgresdb_object.empty_table("testprofilesevolution")
    main_ops_object.postgresdb_object.empty_table("testprofiles_testprofilesevolution")
    analysis_results = {"data":{'date': ['First week', 'Second week', 'Third week'], 
                        'n_posts': ['1219', '1219', '1217'], 
                        'n_followers': ['217178', '217178', '217094'], 
                        'n_followings': ['431', '431', '430']},
                        "ids":profile_ids}
    result = main_ops_object.insert_many_analysis_results("05-11-2020", "07-11-2020", 
                "test_profile_evolution", analysis_results)
    assert len(result["id"])> 0 and len(result["relationships"]) == len(profile_ids)
    
def test4_insert_many_analysis_results():
    """
    Test to check the method which inserts the analysis results as well as the 
    ids from the involved data samples in the related tables of the Postgres database.
    In this test, the provided analysis results are already in the database so
    they won't be inserted and an exception will be raised.
    """
    analysis_results = {"data":{'date': ['First week', 'Second week', 'Third week'], 
                        'n_posts': ['1219', '1219', '1217'], 
                        'n_followers': ['217178', '217178', '217094'], 
                        'n_followings': ['431', '431', '430']},
                        "ids":profile_ids}
    with pytest.raises(InvalidAnalysisResults):
        main_ops_object.insert_many_analysis_results("05-11-2020", "07-11-2020", 
                "test_profile_evolution", analysis_results)
    
def test1_insert_media_popularity_results():
    """
    Test to check the method which inserts the Media Popularity analysis results
    in the database. In this test, the results are not provided so an exception
    will be raised.
    """
    with pytest.raises(InvalidAnalysisResults):
        assert main_ops_object.insert_media_popularity_results(None, None, None, None)
    
def test1_top_ten_medias_popularity():
    """
    Test to check the method which gets the ranking of the best or the worst
    medias based on the interactions, such as the number of likes and comments.
    In this test, the Medias Popularity analysis results are not provided so
    an exception will be raised.
    """
    with pytest.raises(InvalidAnalysisResults):
        assert main_ops_object.top_ten_medias_popularity(None, None, None, None, None, None,)

def test1_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the username of the studied user is not provided so an exception
    will be raised.
    """
    with pytest.raises(UsernameNotFound):
        assert main_ops_object.perform_analysis(None, None, None, None, None)
        
def test2_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the analysis to perform is not provided so an exception
    will be raised.
    """
    with pytest.raises(InvalidAnalysis):
        assert main_ops_object.perform_analysis("audispain", None, None, None, None)
        
def test3_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the provided analysis is not valid so an exception
    will be raised.
    """
    with pytest.raises(InvalidAnalysis):
        assert main_ops_object.perform_analysis("audispain", "invalid-analysis", None, None, None)
        
def test4_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the social media source is not provided so an exception will
    be raised.
    """
    with pytest.raises(InvalidSocialMediaSource):
        assert main_ops_object.perform_analysis("audispain", "test_profile_evolution", None, None, None)
        
def test5_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the provided social media source is not valid so an exception
    will be raised.
    """
    with pytest.raises(InvalidSocialMediaSource):
        assert main_ops_object.perform_analysis("audispain", "test_profile_evolution", 
                                            "invalid-social-media", None, None)
        
def test6_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the range of dates is not provided so an exception will be raised.
    """
    with pytest.raises(InvalidDates):
        assert main_ops_object.perform_analysis("audispain", "test_profile_evolution",
                                                "Instagram", None, None)

def test7_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the provided range of dates is not valid so an exception will
    be raised.
    """
    with pytest.raises(InvalidDates):
        assert main_ops_object.perform_analysis("audispain", 
                "test_profile_evolution", "Instagram", "24-10-2020", "2020-10-28")
        
def test8_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the provided range of dates is not valid so an exception will
    be raised.
    """
    with pytest.raises(InvalidDates):
        assert main_ops_object.perform_analysis("audispain", 
            "test_profile_evolution", "Instagram", "24-10-2020", "08-10-2020")
        
def test9_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the analysis to perform is Profiles Evolution on a set of three-days
    user data.
    """
    # Delete all the records of the Postgres table in order to insert the data
    main_ops_object.postgresdb_object.empty_table("testprofiles")
    result = main_ops_object.perform_analysis("audispain", "test_profile_evolution",
              "Instagram", "05-11-2020", "07-11-2020")
    assert type(result) == dict and result["state"] == True 
    
def test10_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the analysis to perform is Profiles Evolution on a set of more
    than 7 days of user data.
    """
    user_data = [{"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-1.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-1.fna.fbcdn.net&_nc_ohc=7VcHYzwWrZYAX-ACgjV&oh=d6e3cf37b9107352388a633c20cd1124&oe=5FC6988A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "215994", "n_followings" : "427", "n_medias" : "1213", "social_media" : "Instagram", "date" : datetime.strptime("31-10-2020",'%d-%m-%Y'), "username" : "audispain" },
                  {"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=IuH2NUq_6kwAX9bbldK&oh=ef15ba238a712f447fa8ce1ad68e7ae1&oe=5FC6988A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "216137", "n_followings" : "428", "n_medias" : "1215", "social_media" : "Instagram", "date" : datetime.strptime("01-11-2020",'%d-%m-%Y'), "username" : "audispain" },
                  {"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=IuH2NUq_6kwAX9-xnN0&oh=254e28ac6fa2e446c788f18231089c8a&oe=5FCA8D0A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "216897", "n_followings" : "428", "n_medias" : "1215", "social_media" : "Instagram", "date" : datetime.strptime("02-11-2020",'%d-%m-%Y'), "username" : "audispain" },
                  {"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=IuH2NUq_6kwAX81U4wb&oh=c428ab85e33752abb9faf11f12c4abfa&oe=5FCA8D0A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "217163", "n_followings" : "428", "n_medias" : "1215", "social_media" : "Instagram", "date" : datetime.strptime("03-11-2020",'%d-%m-%Y'), "username" : "audispain" },
                  {"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=nS90OZW4faUAX81clHv&oh=d2ced660151ec9615f0d77c593e967a8&oe=5FCA8D0A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "217069", "n_followings" : "430", "n_medias" : "1217", "social_media" : "Instagram", "date" : datetime.strptime("04-11-2020",'%d-%m-%Y'), "username" : "audispain" },
                  {"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=nS90OZW4faUAX81clHv&oh=88423019cc1028caa505d68c2de6f9ea&oe=5FCE818A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "217094", "n_followings" : "430", "n_medias" : "1217", "social_media" : "Instagram", "date" : datetime.strptime("05-11-2020",'%d-%m-%Y'), "username" : "audispain" },
                  {"userid" : "1121839441", "username" : "audispain", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=nS90OZW4faUAX9bEQzi&oh=fc5ceaaa72a7cc21a0185719616ea3b0&oe=5FCE818A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "217178", "n_followings" : "431", "n_medias" : "1219", "social_media" : "Instagram", "date" : datetime.strptime("06-11-2020",'%d-%m-%Y')},
                  {"userid" : "1121839441", "username" : "audispain", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-1.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-1.fna.fbcdn.net&_nc_ohc=MMdtX1oSzBUAX-zXF_W&oh=fd89d26d138d5bc12bdf2dffe57bffba&oe=5FD2760A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "217299", "n_followings" : "431", "n_medias" : "1220", "social_media" : "Instagram", "date" : datetime.strptime("07-11-2020",'%d-%m-%Y')}
        ]
    for item in user_data:
        main_ops_object.common_data_object.insert_user_data(item, "test")
    # Delete all the records of the Postgres table in order to insert the data
    main_ops_object.postgresdb_object.empty_table("testprofiles")
    main_ops_object.postgresdb_object.empty_table("testprofilesevolution")
    main_ops_object.postgresdb_object.empty_table("testprofiles_testprofilesevolution")
    result = main_ops_object.perform_analysis("audispain", "test_profile_evolution",
              "Instagram", "31-10-2020", "07-11-2020")
    assert type(result) == dict and result["state"] == True 

def test11_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the analysis to perform is Profile Activity on a set of 
    three-days user data.
    """
    # Delete all the records of the Postgres table in order to insert the data
    main_ops_object.postgresdb_object.empty_table("testprofiles")
    result = main_ops_object.perform_analysis("audispain", "test_profile_activity",
              "Instagram", "05-11-2020", "07-11-2020")
    assert type(result) == dict and result["state"] == True 
    
def test12_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the analysis to perform is the Profile Activity on a set of more
    than 7 days user data.
    """
    user_data = [{"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-1.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-1.fna.fbcdn.net&_nc_ohc=7VcHYzwWrZYAX-ACgjV&oh=d6e3cf37b9107352388a633c20cd1124&oe=5FC6988A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "215994", "n_followings" : "427", "n_medias" : "1213", "social_media" : "Instagram", "date" : datetime.strptime("31-10-2020",'%d-%m-%Y'), "username" : "audispain" },
                  {"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=IuH2NUq_6kwAX9bbldK&oh=ef15ba238a712f447fa8ce1ad68e7ae1&oe=5FC6988A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "216137", "n_followings" : "428", "n_medias" : "1215", "social_media" : "Instagram", "date" : datetime.strptime("01-11-2020",'%d-%m-%Y'), "username" : "audispain" },
                  {"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=IuH2NUq_6kwAX9-xnN0&oh=254e28ac6fa2e446c788f18231089c8a&oe=5FCA8D0A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "216897", "n_followings" : "428", "n_medias" : "1215", "social_media" : "Instagram", "date" : datetime.strptime("02-11-2020",'%d-%m-%Y'), "username" : "audispain" },
                  {"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=IuH2NUq_6kwAX81U4wb&oh=c428ab85e33752abb9faf11f12c4abfa&oe=5FCA8D0A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "217163", "n_followings" : "428", "n_medias" : "1215", "social_media" : "Instagram", "date" : datetime.strptime("03-11-2020",'%d-%m-%Y'), "username" : "audispain" },
                  {"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=nS90OZW4faUAX81clHv&oh=d2ced660151ec9615f0d77c593e967a8&oe=5FCA8D0A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "217069", "n_followings" : "430", "n_medias" : "1217", "social_media" : "Instagram", "date" : datetime.strptime("04-11-2020",'%d-%m-%Y'), "username" : "audispain" },
                  {"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=nS90OZW4faUAX81clHv&oh=88423019cc1028caa505d68c2de6f9ea&oe=5FCE818A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "217094", "n_followings" : "430", "n_medias" : "1217", "social_media" : "Instagram", "date" : datetime.strptime("05-11-2020",'%d-%m-%Y'), "username" : "audispain" },
                  {"userid" : "1121839441", "username" : "audispain", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=nS90OZW4faUAX9bEQzi&oh=fc5ceaaa72a7cc21a0185719616ea3b0&oe=5FCE818A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "217178", "n_followings" : "431", "n_medias" : "1219", "social_media" : "Instagram", "date" : datetime.strptime("06-11-2020",'%d-%m-%Y')},
                  {"userid" : "1121839441", "username" : "audispain", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-1.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-1.fna.fbcdn.net&_nc_ohc=MMdtX1oSzBUAX-zXF_W&oh=fd89d26d138d5bc12bdf2dffe57bffba&oe=5FD2760A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "217299", "n_followings" : "431", "n_medias" : "1220", "social_media" : "Instagram", "date" : datetime.strptime("07-11-2020",'%d-%m-%Y')}
        ]
    for item in user_data:
        main_ops_object.common_data_object.insert_user_data(item, "test")
    # Delete all the records of the Postgres table in order to insert the data
    main_ops_object.postgresdb_object.empty_table("testprofiles")
    main_ops_object.postgresdb_object.empty_table("testprofilesactivity")
    main_ops_object.postgresdb_object.empty_table("testprofiles_testprofilesactivity")
    result = main_ops_object.perform_analysis("audispain", "test_profile_activity",
              "Instagram", "31-10-2020", "07-11-2020")
    assert type(result) == dict and result["state"] == True
    
def test13_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the analysis to perform is Media Evolution on a set of three-days
    user data. In order to do that, the user data will be inserted into the 'Test'
    collection of Mongo database.
    """
    # Insert five records to test the analysis
    user_data = [
        {"medias" : [
    		{
     			"id_media" : "2429379247628862182_1121839441",
     			"title" : "Existen vehículos concebidos para mejorar nuestra movilidad… y otros que, además, definen quiénes somos y cuáles son nuestras aspiraciones. \n\nDescubre el Audi A6 Avant con MMI Touch y sistema de sonido Bang & Olufsen a través del enlace de nuestra BIO.\n\n#AudiA6Avant #A6Avant #MásQueUnAutomóvil",
     			"taken_at" : "27/10/2020",
     			"like_count" : "1035",
     			"comment_count" : "4",
    		},
    		{
     			"id_media" : "2429083272555842514_1121839441",
     			"title" : "Tú también puedes vivir una experiencia única como esta. Libera adrenalina en los cursos de Audi driving experience conduciendo uno de nuestros súper deportivos. ¡Reserva ya tu plaza a través del link de nuestra BIO!🏁\n\n#AudiDrivingExperience",
     			"taken_at" : "27/10/2020",
     			"like_count" : "663",
     			"comment_count" : "27",
    		},],
     	"social_media" : "Instagram",
     	"date" : datetime.strptime("31-10-2020",'%d-%m-%Y'),
     	"username" : "audispain"
        },
        {"medias" : [
    		{
     			"id_media" : "2429379247628862182_1121839441",
     			"title" : "Existen vehículos concebidos para mejorar nuestra movilidad… y otros que, además, definen quiénes somos y cuáles son nuestras aspiraciones. \n\nDescubre el Audi A6 Avant con MMI Touch y sistema de sonido Bang & Olufsen a través del enlace de nuestra BIO.\n\n#AudiA6Avant #A6Avant #MásQueUnAutomóvil",
     			"taken_at" : "28/10/2020",
     			"like_count" : "2040",
     			"comment_count" : "47",
    		},
    		{
     			"id_media" : "2429083272555842514_1121839441",
     			"title" : "Tú también puedes vivir una experiencia única como esta. Libera adrenalina en los cursos de Audi driving experience conduciendo uno de nuestros súper deportivos. ¡Reserva ya tu plaza a través del link de nuestra BIO!🏁\n\n#AudiDrivingExperience",
     			"taken_at" : "28/10/2020",
     			"like_count" : "895",
     			"comment_count" : "45",
    		},],
     	"social_media" : "Instagram",
     	"date" : datetime.strptime("01-11-2020",'%d-%m-%Y'),
     	"username" : "audispain"
        },
        {"medias" : [
    		{
     			"id_media" : "2429379247628862182_1121839441",
     			"title" : "Existen vehículos concebidos para mejorar nuestra movilidad… y otros que, además, definen quiénes somos y cuáles son nuestras aspiraciones. \n\nDescubre el Audi A6 Avant con MMI Touch y sistema de sonido Bang & Olufsen a través del enlace de nuestra BIO.\n\n#AudiA6Avant #A6Avant #MásQueUnAutomóvil",
     			"taken_at" : "29/10/2020",
     			"like_count" : "3520",
     			"comment_count" : "128",
    		},
    		{
     			"id_media" : "2429083272555842514_1121839441",
     			"title" : "Tú también puedes vivir una experiencia única como esta. Libera adrenalina en los cursos de Audi driving experience conduciendo uno de nuestros súper deportivos. ¡Reserva ya tu plaza a través del link de nuestra BIO!🏁\n\n#AudiDrivingExperience",
     			"taken_at" : "29/10/2020",
     			"like_count" : "1485",
     			"comment_count" : "69",
    		},],
     	"social_media" : "Instagram",
     	"date" : datetime.strptime("02-11-2020",'%d-%m-%Y'),
     	"username" : "audispain"
        },
        {"medias" : [
    		{
     			"id_media" : "2429379247628862182_1121839441",
     			"title" : "Existen vehículos concebidos para mejorar nuestra movilidad… y otros que, además, definen quiénes somos y cuáles son nuestras aspiraciones. \n\nDescubre el Audi A6 Avant con MMI Touch y sistema de sonido Bang & Olufsen a través del enlace de nuestra BIO.\n\n#AudiA6Avant #A6Avant #MásQueUnAutomóvil",
     			"taken_at" : "29/10/2020",
     			"like_count" : "4250",
     			"comment_count" : "220",
    		},
    		{
     			"id_media" : "2429083272555842514_1121839441",
     			"title" : "Tú también puedes vivir una experiencia única como esta. Libera adrenalina en los cursos de Audi driving experience conduciendo uno de nuestros súper deportivos. ¡Reserva ya tu plaza a través del link de nuestra BIO!🏁\n\n#AudiDrivingExperience",
     			"taken_at" : "29/10/2020",
     			"like_count" : "1689",
     			"comment_count" : "120",
    		},],
     	"social_media" : "Instagram",
     	"date" : datetime.strptime("03-11-2020",'%d-%m-%Y'),
     	"username" : "audispain"
        },
        {"medias" : [
    		{
     			"id_media" : "2429379247628862182_1121839441",
     			"title" : "Existen vehículos concebidos para mejorar nuestra movilidad… y otros que, además, definen quiénes somos y cuáles son nuestras aspiraciones. \n\nDescubre el Audi A6 Avant con MMI Touch y sistema de sonido Bang & Olufsen a través del enlace de nuestra BIO.\n\n#AudiA6Avant #A6Avant #MásQueUnAutomóvil",
     			"taken_at" : "29/10/2020",
     			"like_count" : "4200",
     			"comment_count" : "235",
    		},
    		{
     			"id_media" : "2429083272555842514_1121839441",
     			"title" : "Tú también puedes vivir una experiencia única como esta. Libera adrenalina en los cursos de Audi driving experience conduciendo uno de nuestros súper deportivos. ¡Reserva ya tu plaza a través del link de nuestra BIO!🏁\n\n#AudiDrivingExperience",
     			"taken_at" : "29/10/2020",
     			"like_count" : "1789",
     			"comment_count" : "135",
    		},],
     	"social_media" : "Instagram",
     	"date" : datetime.strptime("04-11-2020",'%d-%m-%Y'),
     	"username" : "audispain"
        },
        {"medias" : [
    		{
     			"id_media" : "2429379247628862182_1121839441",
     			"title" : "Existen vehículos concebidos para mejorar nuestra movilidad… y otros que, además, definen quiénes somos y cuáles son nuestras aspiraciones. \n\nDescubre el Audi A6 Avant con MMI Touch y sistema de sonido Bang & Olufsen a través del enlace de nuestra BIO.\n\n#AudiA6Avant #A6Avant #MásQueUnAutomóvil",
     			"taken_at" : "29/10/2020",
     			"like_count" : "4520",
     			"comment_count" : "369",
    		},
    		{
     			"id_media" : "2429083272555842514_1121839441",
     			"title" : "Tú también puedes vivir una experiencia única como esta. Libera adrenalina en los cursos de Audi driving experience conduciendo uno de nuestros súper deportivos. ¡Reserva ya tu plaza a través del link de nuestra BIO!🏁\n\n#AudiDrivingExperience",
     			"taken_at" : "29/10/2020",
     			"like_count" : "1899",
     			"comment_count" : "145",
    		},],
     	"social_media" : "Instagram",
     	"date" : datetime.strptime("05-11-2020",'%d-%m-%Y'),
     	"username" : "audispain"
        },
        {"medias" : [
    		{
     			"id_media" : "2429379247628862182_1121839441",
     			"title" : "Existen vehículos concebidos para mejorar nuestra movilidad… y otros que, además, definen quiénes somos y cuáles son nuestras aspiraciones. \n\nDescubre el Audi A6 Avant con MMI Touch y sistema de sonido Bang & Olufsen a través del enlace de nuestra BIO.\n\n#AudiA6Avant #A6Avant #MásQueUnAutomóvil",
     			"taken_at" : "29/10/2020",
     			"like_count" : "4789",
     			"comment_count" : "128",
    		},
    		{
     			"id_media" : "2429083272555842514_1121839441",
     			"title" : "Tú también puedes vivir una experiencia única como esta. Libera adrenalina en los cursos de Audi driving experience conduciendo uno de nuestros súper deportivos. ¡Reserva ya tu plaza a través del link de nuestra BIO!🏁\n\n#AudiDrivingExperience",
     			"taken_at" : "29/10/2020",
     			"like_count" : "2050",
     			"comment_count" : "189",
    		},],
     	"social_media" : "Instagram",
     	"date" : datetime.strptime("06-11-2020",'%d-%m-%Y'),
     	"username" : "audispain"
        },
        {"medias" : [
    		{
     			"id_media" : "2429379247628862182_1121839441",
     			"title" : "Existen vehículos concebidos para mejorar nuestra movilidad… y otros que, además, definen quiénes somos y cuáles son nuestras aspiraciones. \n\nDescubre el Audi A6 Avant con MMI Touch y sistema de sonido Bang & Olufsen a través del enlace de nuestra BIO.\n\n#AudiA6Avant #A6Avant #MásQueUnAutomóvil",
     			"taken_at" : "29/10/2020",
     			"like_count" : "5895",
     			"comment_count" : "352",
    		},
    		{
     			"id_media" : "2429083272555842514_1121839441",
     			"title" : "Tú también puedes vivir una experiencia única como esta. Libera adrenalina en los cursos de Audi driving experience conduciendo uno de nuestros súper deportivos. ¡Reserva ya tu plaza a través del link de nuestra BIO!🏁\n\n#AudiDrivingExperience",
     			"taken_at" : "29/10/2020",
     			"like_count" : "3698",
     			"comment_count" : "369",
    		},],
     	"social_media" : "Instagram",
     	"date" : datetime.strptime("07-11-2020",'%d-%m-%Y'),
     	"username" : "audispain"
        },
    ]
    for item in user_data:
        main_ops_object.common_data_object.insert_user_data(item, "test_medias")
    # Delete all the records of the Postgres table in order to insert the data
    main_ops_object.postgresdb_object.empty_table("testmedias")
    main_ops_object.postgresdb_object.empty_table("testmediatitles")
    main_ops_object.postgresdb_object.empty_table("testmediacomments")
    result = main_ops_object.perform_analysis("audispain", "test_media_evolution",
              "Instagram", "31-10-2020", "02-11-2020")
    assert type(result) == dict and result["state"] == True 
    
def test14_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the analysis to perform is the Media Evolution on a set of more
    than 7 days user data.
    """
    main_ops_object.postgresdb_object.empty_table("testmediasevolution")
    main_ops_object.postgresdb_object.empty_table("testmedias_testmediasevolution")
    result = main_ops_object.perform_analysis("audispain", "test_media_evolution",
              "Instagram", "31-10-2020", "07-11-2020")
    assert type(result) == dict and result["state"] == True 

def test15_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the analysis to perform is the Media Popularity on a set of three
    days user data.
    """
    result = main_ops_object.perform_analysis("audispain", "test_media_popularity",
              "Instagram", "31-10-2020", "02-11-2020")
    assert type(result) == dict  
    
def test16_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the analysis to perform is the Media Popularity on a set of more
    than 7 days user data.
    """
    result = main_ops_object.perform_analysis("audispain", "test_media_popularity",
              "Instagram", "31-10-2020", "07-11-2020")
    assert type(result) == dict
    
def test17_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the analysis to perform is the Sentiment Analysis based on the
    comments from the posts during a specific period of time.
    """
    comments = [
        {
        "comments":[{ "id_media" : "2429379247628862182_1121839441", 
                     "texts" : [{ "user" : "azahara_carmona", "text" : "@rorry_carmona 😂😂😂😂😂" }, 
                                { "user" : "albarujano", "text" : "@apostolovakarina3 😂😂"} ]}],
        "social_media" : "Instagram", 
        "date" : datetime.strptime("31-10-2020",'%d-%m-%Y'),
        "username" : "audispain" 
        },
        {
        "comments":[{ "id_media" : "2429083272555842514_1121839441", 
                     "texts" : [{ "user" : "azahara_carmona", "text" : "@rorry_carmona 😂😂😂😂😂" }, 
                                { "user" : "albarujano", "text" : "@apostolovakarina3 😂😂"} ]}],
        "social_media" : "Instagram", 
        "date" : datetime.strptime("01-11-2020",'%d-%m-%Y'),
        "username" : "audispain" 
        },
        {
        "comments":[{ "id_media" : "2429379247628862182_1121839441", 
                     "texts" : [{ "user" : "azahara_carmona", "text" : "@rorry_carmona 😂😂😂😂😂" }, 
                                { "user" : "albarujano", "text" : "@apostolovakarina3 😂😂"} ]}],
        "social_media" : "Instagram", 
        "date" : datetime.strptime("02-11-2020",'%d-%m-%Y'),
        "username" : "audispain" 
        },
        ]
    
    # Delete the mongo collection
    main_ops_object.mongodb_object.set_collection("test_comments")
    main_ops_object.mongodb_object.delete_records("delete_all")
    for item in comments:
        main_ops_object.common_data_object.insert_user_data(item, "test_comments")
    
    main_ops_object.postgresdb_object.empty_table("testsentimentanalysis")
    result = main_ops_object.perform_analysis("audispain", "test_comment_sentiment_analysis",
              "Instagram", "31-10-2020", "02-11-2020")
    assert type(result) == dict and result["state"] == True 

def test18_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the analysis to perform is the Sentiment Analysis based on the
    titles of a set of posts during a specific period of time.
    """
    result = main_ops_object.perform_analysis("audispain", "test_title_sentiment_analysis",
              "Instagram", "31-10-2020", "02-11-2020")
    assert type(result) == dict and result["state"] == True 
    
def test19_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the analysis to perform is the Sentiment Analysis based on the
    titles of a set of posts during a specific period of time.
    """
    result = main_ops_object.perform_analysis("audispain", "test_users_behaviours",
              "Instagram", "31-10-2020", "02-11-2020")
    assert type(result) == dict and result["state"] == True 