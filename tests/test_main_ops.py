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
    , InvalidDates, CollectionNotFound, InvalidQuery
    
# MainOperations object to perform the tests
main_ops_object = main_ops.MainOperations()
# Username to get his user data from Instagram
username = "pablo_cuevas15"

def test1_set_user_to_study():
    """
    Test to check the method which sets the username of the user to collect data
    from the chosen social media sources. In this test, the username is not provided
    so an exception will be raised.
    """
    with pytest.raises(UsernameNotFound):
        assert main_ops_object.set_user_to_study(None)
        
def test2_set_user_to_study():
    """
    Test to check the method which sets the username of the user to collect data
    from the chosen social media sources. 
    """
    set_user = main_ops_object.set_user_to_study(username)
    assert set_user == username
        
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
    medias = [{'id_media': '1', "taken_at":"24/10/2020", "title":None, 'like_count': 29, 'comment_count': 14}, 
              {'id_media': '2', "taken_at":"24/10/2020", "title":None,'like_count': 18, 'comment_count': 0}]
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
    
def test1_get_data_from_postgresdb():
    """
    Test to check the method which recovers data from the Postgres database. In
    this test, the query to make is not provided so an exceptino will be raised.
    """
    with pytest.raises(InvalidQuery):
        assert main_ops_object.get_data_from_postgresdb(None, None)
        
def test2_get_data_from_postgresdb():
    """
    Test to check the method which recovers data from the Postgres database. In
    this test, the values to make the provided query are not provided so an exceptino will be raised.
    """
    with pytest.raises(UserDataNotFound):
        assert main_ops_object.get_data_from_postgresdb("check_test_profile", None)

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
    main_ops_object.postgresdb_object.empty_table("testprofilesevolution")
    result = main_ops_object.perform_analysis("audispain", "test_profile_evolution",
              "Instagram", "05-11-2020", "07-11-2020")
    assert type(result) == list and len(result) == 3
    
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
    result = main_ops_object.perform_analysis("audispain", "test_profile_evolution",
              "Instagram", "31-10-2020", "07-11-2020")
    assert type(result) == list and len(result) == 2

def test11_perform_analysis():
    """
    Test to check the method which performs a specific analysis on the selected
    user data getting the information from the Mongo database to Postgre database.
    In this test, the analysis to perform is Profiles Evolution and it's been done
    before so the method will recover the analysis results to plot them directly.
    """
    result = main_ops_object.perform_analysis("audispain", "test_profile_evolution",
              "Instagram", "31-10-2020", "07-11-2020")
    assert type(result) == dict

# def test12_perform_analysis():
#     """
#     Test to check the method which performs a specific analysis on the selected
#     user data getting the information from the Mongo database to Postgre database.
#     In this test, the analysis to perform is Profile Activity on a set of 
#     three-days user data.
#     """
#     # Delete all the records of the Postgres table in order to insert the data
#     main_ops_object.postgresdb_object.empty_table("testprofilesactivity")
#     result = main_ops_object.perform_analysis("audispain", "test_profile_activity",
#               "Instagram", "05-11-2020", "07-11-2020")
#     assert type(result) == list and len(result) == 3
    
# def test13_perform_analysis():
#     """
#     Test to check the method which performs a specific analysis on the selected
#     user data getting the information from the Mongo database to Postgre database.
#     In this test, the analysis to perform is the Profile Activity on a set of more
#     than 7 days user data.
#     """
#     user_data = [{"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-1.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-1.fna.fbcdn.net&_nc_ohc=7VcHYzwWrZYAX-ACgjV&oh=d6e3cf37b9107352388a633c20cd1124&oe=5FC6988A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "215994", "n_followings" : "427", "n_medias" : "1213", "social_media" : "Instagram", "date" : datetime.strptime("31-10-2020",'%d-%m-%Y'), "username" : "audispain" },
#                   {"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=IuH2NUq_6kwAX9bbldK&oh=ef15ba238a712f447fa8ce1ad68e7ae1&oe=5FC6988A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "216137", "n_followings" : "428", "n_medias" : "1215", "social_media" : "Instagram", "date" : datetime.strptime("01-11-2020",'%d-%m-%Y'), "username" : "audispain" },
#                   {"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=IuH2NUq_6kwAX9-xnN0&oh=254e28ac6fa2e446c788f18231089c8a&oe=5FCA8D0A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "216897", "n_followings" : "428", "n_medias" : "1215", "social_media" : "Instagram", "date" : datetime.strptime("02-11-2020",'%d-%m-%Y'), "username" : "audispain" },
#                   {"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=IuH2NUq_6kwAX81U4wb&oh=c428ab85e33752abb9faf11f12c4abfa&oe=5FCA8D0A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "217163", "n_followings" : "428", "n_medias" : "1215", "social_media" : "Instagram", "date" : datetime.strptime("03-11-2020",'%d-%m-%Y'), "username" : "audispain" },
#                   {"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=nS90OZW4faUAX81clHv&oh=d2ced660151ec9615f0d77c593e967a8&oe=5FCA8D0A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "217069", "n_followings" : "430", "n_medias" : "1217", "social_media" : "Instagram", "date" : datetime.strptime("04-11-2020",'%d-%m-%Y'), "username" : "audispain" },
#                   {"userid" : "1121839441", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=nS90OZW4faUAX81clHv&oh=88423019cc1028caa505d68c2de6f9ea&oe=5FCE818A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "217094", "n_followings" : "430", "n_medias" : "1217", "social_media" : "Instagram", "date" : datetime.strptime("05-11-2020",'%d-%m-%Y'), "username" : "audispain" },
#                   {"userid" : "1121839441", "username" : "audispain", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-2.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-2.fna.fbcdn.net&_nc_ohc=nS90OZW4faUAX9bEQzi&oh=fc5ceaaa72a7cc21a0185719616ea3b0&oe=5FCE818A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "217178", "n_followings" : "431", "n_medias" : "1219", "social_media" : "Instagram", "date" : datetime.strptime("06-11-2020",'%d-%m-%Y')},
#                   {"userid" : "1121839441", "username" : "audispain", "name" : "Audi España", "biography" : "Bienvenidos al canal oficial de Audi España. Nuestro equipo permanece a tu disposición en el número 800 500 102.", "gender" : "None", "profile_pic" : "https://instagram.fsvq2-1.fna.fbcdn.net/v/t51.2885-19/s150x150/13167289_1713494358922750_2066970229_a.jpg?_nc_ht=instagram.fsvq2-1.fna.fbcdn.net&_nc_ohc=MMdtX1oSzBUAX-zXF_W&oh=fd89d26d138d5bc12bdf2dffe57bffba&oe=5FD2760A", "location" : "None", "birthday" : "None", "date_joined" : "None", "n_followers" : "217299", "n_followings" : "431", "n_medias" : "1220", "social_media" : "Instagram", "date" : datetime.strptime("07-11-2020",'%d-%m-%Y')}
#         ]
#     for item in user_data:
#         main_ops_object.common_data_object.insert_user_data(item, "test")
#     # Delete all the records of the Postgres table in order to insert the data
#     result = main_ops_object.perform_analysis("audispain", "test_profile_activity",
#               "Instagram", "31-10-2020", "07-11-2020")
#     assert type(result) == list and len(result) == 2
    
# def test14_perform_analysis():
#     """
#     Test to check the method which performs a specific analysis on the selected
#     user data getting the information from the Mongo database to Postgre database.
#     In this test, the analysis to perform is the Profile Activity but it's been
#     done before so the method will recover the analysis results in order to plot them directly.
#     """
#     result = main_ops_object.perform_analysis("audispain", "test_profile_activity",
#               "Instagram", "31-10-2020", "07-11-2020")
#     assert type(result) == dict 
    
# def test15_perform_analysis():
#     """
#     Test to check the method which performs a specific analysis on the selected
#     user data getting the information from the Mongo database to Postgre database.
#     In this test, the analysis to perform is Media Evolution on a set of three-days
#     user data. In order to do that, the user data will be inserted into the 'Test'
#     collection of Mongo database.
#     """
#     # Delete the previous records from the collections
#     main_ops_object.mongodb_object.set_collection("test_medias")
#     main_ops_object.mongodb_object.delete_records("delete_all")
#     main_ops_object.mongodb_object.set_collection("test_comments")
#     main_ops_object.mongodb_object.delete_records("delete_all")
#     # Insert five records to test the analysis
#     user_data = [
#         {"medias" : [
#     		{
#      			"id_media" : "2429379247628862182_1121839441",
#      			"title" : "Existen vehículos concebidos para mejorar nuestra movilidad… y otros que, además, definen quiénes somos y cuáles son nuestras aspiraciones. \n\nDescubre el Audi A6 Avant con MMI Touch y sistema de sonido Bang & Olufsen a través del enlace de nuestra BIO.\n\n#AudiA6Avant #A6Avant #MásQueUnAutomóvil",
#      			"taken_at" : "27/10/2020",
#      			"like_count" : "1035",
#      			"comment_count" : "4",
#     		},
#     		{
#      			"id_media" : "2429083272555842514_1121839441",
#      			"title" : "Tú también puedes vivir una experiencia única como esta. Libera adrenalina en los cursos de Audi driving experience conduciendo uno de nuestros súper deportivos. ¡Reserva ya tu plaza a través del link de nuestra BIO!🏁\n\n#AudiDrivingExperience",
#      			"taken_at" : "27/10/2020",
#      			"like_count" : "663",
#      			"comment_count" : "27",
#     		},],
#      	"social_media" : "Instagram",
#      	"date" : datetime.strptime("31-10-2020",'%d-%m-%Y'),
#      	"username" : "audispain"
#         },
#         {"medias" : [
#     		{
#      			"id_media" : "2429379247628862182_1121839441",
#      			"title" : "Existen vehículos concebidos para mejorar nuestra movilidad… y otros que, además, definen quiénes somos y cuáles son nuestras aspiraciones. \n\nDescubre el Audi A6 Avant con MMI Touch y sistema de sonido Bang & Olufsen a través del enlace de nuestra BIO.\n\n#AudiA6Avant #A6Avant #MásQueUnAutomóvil",
#      			"taken_at" : "28/10/2020",
#      			"like_count" : "2040",
#      			"comment_count" : "47",
#     		},
#     		{
#      			"id_media" : "2429083272555842514_1121839441",
#      			"title" : "Tú también puedes vivir una experiencia única como esta. Libera adrenalina en los cursos de Audi driving experience conduciendo uno de nuestros súper deportivos. ¡Reserva ya tu plaza a través del link de nuestra BIO!🏁\n\n#AudiDrivingExperience",
#      			"taken_at" : "28/10/2020",
#      			"like_count" : "895",
#      			"comment_count" : "45",
#     		},],
#      	"social_media" : "Instagram",
#      	"date" : datetime.strptime("01-11-2020",'%d-%m-%Y'),
#      	"username" : "audispain"
#         },
#         {"medias" : [
#     		{
#      			"id_media" : "2429379247628862182_1121839441",
#      			"title" : "Existen vehículos concebidos para mejorar nuestra movilidad… y otros que, además, definen quiénes somos y cuáles son nuestras aspiraciones. \n\nDescubre el Audi A6 Avant con MMI Touch y sistema de sonido Bang & Olufsen a través del enlace de nuestra BIO.\n\n#AudiA6Avant #A6Avant #MásQueUnAutomóvil",
#      			"taken_at" : "29/10/2020",
#      			"like_count" : "3520",
#      			"comment_count" : "128",
#     		},
#     		{
#      			"id_media" : "2429083272555842514_1121839441",
#      			"title" : "Tú también puedes vivir una experiencia única como esta. Libera adrenalina en los cursos de Audi driving experience conduciendo uno de nuestros súper deportivos. ¡Reserva ya tu plaza a través del link de nuestra BIO!🏁\n\n#AudiDrivingExperience",
#      			"taken_at" : "29/10/2020",
#      			"like_count" : "1485",
#      			"comment_count" : "69",
#     		},],
#      	"social_media" : "Instagram",
#      	"date" : datetime.strptime("02-11-2020",'%d-%m-%Y'),
#      	"username" : "audispain"
#         },
#         {"medias" : [
#     		{
#      			"id_media" : "2429379247628862182_1121839441",
#      			"title" : "Existen vehículos concebidos para mejorar nuestra movilidad… y otros que, además, definen quiénes somos y cuáles son nuestras aspiraciones. \n\nDescubre el Audi A6 Avant con MMI Touch y sistema de sonido Bang & Olufsen a través del enlace de nuestra BIO.\n\n#AudiA6Avant #A6Avant #MásQueUnAutomóvil",
#      			"taken_at" : "29/10/2020",
#      			"like_count" : "4250",
#      			"comment_count" : "220",
#     		},
#     		{
#      			"id_media" : "2429083272555842514_1121839441",
#      			"title" : "Tú también puedes vivir una experiencia única como esta. Libera adrenalina en los cursos de Audi driving experience conduciendo uno de nuestros súper deportivos. ¡Reserva ya tu plaza a través del link de nuestra BIO!🏁\n\n#AudiDrivingExperience",
#      			"taken_at" : "29/10/2020",
#      			"like_count" : "1689",
#      			"comment_count" : "120",
#     		},],
#      	"social_media" : "Instagram",
#      	"date" : datetime.strptime("03-11-2020",'%d-%m-%Y'),
#      	"username" : "audispain"
#         },
#         {"medias" : [
#     		{
#      			"id_media" : "2429379247628862182_1121839441",
#      			"title" : "Existen vehículos concebidos para mejorar nuestra movilidad… y otros que, además, definen quiénes somos y cuáles son nuestras aspiraciones. \n\nDescubre el Audi A6 Avant con MMI Touch y sistema de sonido Bang & Olufsen a través del enlace de nuestra BIO.\n\n#AudiA6Avant #A6Avant #MásQueUnAutomóvil",
#      			"taken_at" : "29/10/2020",
#      			"like_count" : "4200",
#      			"comment_count" : "235",
#     		},
#     		{
#      			"id_media" : "2429083272555842514_1121839441",
#      			"title" : "Tú también puedes vivir una experiencia única como esta. Libera adrenalina en los cursos de Audi driving experience conduciendo uno de nuestros súper deportivos. ¡Reserva ya tu plaza a través del link de nuestra BIO!🏁\n\n#AudiDrivingExperience",
#      			"taken_at" : "29/10/2020",
#      			"like_count" : "1789",
#      			"comment_count" : "135",
#     		},],
#      	"social_media" : "Instagram",
#      	"date" : datetime.strptime("04-11-2020",'%d-%m-%Y'),
#      	"username" : "audispain"
#         },
#         {"medias" : [
#     		{
#      			"id_media" : "2429379247628862182_1121839441",
#      			"title" : "Existen vehículos concebidos para mejorar nuestra movilidad… y otros que, además, definen quiénes somos y cuáles son nuestras aspiraciones. \n\nDescubre el Audi A6 Avant con MMI Touch y sistema de sonido Bang & Olufsen a través del enlace de nuestra BIO.\n\n#AudiA6Avant #A6Avant #MásQueUnAutomóvil",
#      			"taken_at" : "29/10/2020",
#      			"like_count" : "4520",
#      			"comment_count" : "369",
#     		},
#     		{
#      			"id_media" : "2429083272555842514_1121839441",
#      			"title" : "Tú también puedes vivir una experiencia única como esta. Libera adrenalina en los cursos de Audi driving experience conduciendo uno de nuestros súper deportivos. ¡Reserva ya tu plaza a través del link de nuestra BIO!🏁\n\n#AudiDrivingExperience",
#      			"taken_at" : "29/10/2020",
#      			"like_count" : "1899",
#      			"comment_count" : "145",
#     		},],
#      	"social_media" : "Instagram",
#      	"date" : datetime.strptime("05-11-2020",'%d-%m-%Y'),
#      	"username" : "audispain"
#         },
#         {"medias" : [
#     		{
#      			"id_media" : "2429379247628862182_1121839441",
#      			"title" : "Existen vehículos concebidos para mejorar nuestra movilidad… y otros que, además, definen quiénes somos y cuáles son nuestras aspiraciones. \n\nDescubre el Audi A6 Avant con MMI Touch y sistema de sonido Bang & Olufsen a través del enlace de nuestra BIO.\n\n#AudiA6Avant #A6Avant #MásQueUnAutomóvil",
#      			"taken_at" : "29/10/2020",
#      			"like_count" : "4789",
#      			"comment_count" : "128",
#     		},
#     		{
#      			"id_media" : "2429083272555842514_1121839441",
#      			"title" : "Tú también puedes vivir una experiencia única como esta. Libera adrenalina en los cursos de Audi driving experience conduciendo uno de nuestros súper deportivos. ¡Reserva ya tu plaza a través del link de nuestra BIO!🏁\n\n#AudiDrivingExperience",
#      			"taken_at" : "29/10/2020",
#      			"like_count" : "2050",
#      			"comment_count" : "189",
#     		},],
#      	"social_media" : "Instagram",
#      	"date" : datetime.strptime("06-11-2020",'%d-%m-%Y'),
#      	"username" : "audispain"
#         },
#         {"medias" : [
#     		{
#      			"id_media" : "2429379247628862182_1121839441",
#      			"title" : "Existen vehículos concebidos para mejorar nuestra movilidad… y otros que, además, definen quiénes somos y cuáles son nuestras aspiraciones. \n\nDescubre el Audi A6 Avant con MMI Touch y sistema de sonido Bang & Olufsen a través del enlace de nuestra BIO.\n\n#AudiA6Avant #A6Avant #MásQueUnAutomóvil",
#      			"taken_at" : "29/10/2020",
#      			"like_count" : "5895",
#      			"comment_count" : "352",
#     		},
#     		{
#      			"id_media" : "2429083272555842514_1121839441",
#      			"title" : "Tú también puedes vivir una experiencia única como esta. Libera adrenalina en los cursos de Audi driving experience conduciendo uno de nuestros súper deportivos. ¡Reserva ya tu plaza a través del link de nuestra BIO!🏁\n\n#AudiDrivingExperience",
#      			"taken_at" : "29/10/2020",
#      			"like_count" : "3698",
#      			"comment_count" : "369",
#     		},],
#      	"social_media" : "Instagram",
#      	"date" : datetime.strptime("07-11-2020",'%d-%m-%Y'),
#      	"username" : "audispain"
#         },
#     ]
#     for item in user_data:
#         main_ops_object.common_data_object.insert_user_data(item, "test_medias")
#     # Insert their comments
#     comments = [
#         {"comments" : [
#     		{
#      			"id_media" : "2429379247628862182_1121839441",
#                   "texts":[
#                       { "user" : "vicenteterol_", "text" : "Es una locura, otro rollo...🔥" },
#                       { "user" : "rubenj_xd", "text" : "@audispain nada el frontal está genial ⚡️" }
#                   ]
#     		},
#             {
#      			"id_media" : "2429083272555842514_1121839441",
#                   "texts":[
#                       { "user" : "hugoortegamtz", "text" : "@mendez.alan97 concuerdo contigo mi buen. En lo personal yo creo que esos difusores de aire al frente le dan un toque mágico" },
#                       { "user" : "mendez.alan97", "text" : "@audispain todo, esta simplemente espectacular, siempre Audi nos sorprende 🙌" },
#                   ]
#     		}
#         ],
#      	"social_media" : "Instagram",
#      	"date" : datetime.strptime("31-10-2020",'%d-%m-%Y'),
#      	"username" : "audispain"
#         },
#         {"comments" : [
#     		{
#      			"id_media" : "2429379247628862182_1121839441",
#                   "texts":[
#                       { "user" : "beatriche_rs", "text" : "@alonsorocha estas tú que vas a conducir ese coche, sigue soñando 🤣🤣🤣🤣" },
#                       { "user" : "guilleecg__", "text" : "@nbx_07 @raul.__16" }
#                   ]
#     		},
#             {
#      			"id_media" : "2429083272555842514_1121839441",
#                   "texts":[
#                       { "user" : "david.michelena.3", "text" : "@cristinafger y tanto!" },
#                       { "user" : "cristinafger", "text" : "@david.michelena.3 . Seguro q te gusta!" }
#                     ]
#     		}
#         ],
#      	"social_media" : "Instagram",
#      	"date" : datetime.strptime("01-11-2020",'%d-%m-%Y'),
#      	"username" : "audispain"
#         },
#         {"comments" : [
#     		{
#      			"id_media" : "2429379247628862182_1121839441",
#                   "texts":[
#                       { "user" : "abl_95flames", "text" : "@audispain en eso tenéis razon🤣👏👏" },
#                       { "user" : "vladimir.vasquezm", "text" : "@audispain 🤣" }
#                 ]
#     		},
#             {
#      			"id_media" : "2429083272555842514_1121839441",
#                   "texts":[
#                       { "user" : "trancaso", "text" : "M gustaría ver y que nunca me alcancé, al que debe cobrarme el auto jeje. Hablando en serio, escuche un informe donde, comunican todos los cambios en la línea audi, como siempre en la vanguardia, q7 y q8 lo más, q3 con muchas novedades." },
#                       { "user" : "esiris_model", "text" : "@audispain a vosotros por estas maravillas😍" }
#                     ]
#     		}
#         ],
#      	"social_media" : "Instagram",
#      	"date" : datetime.strptime("02-11-2020",'%d-%m-%Y'),
#      	"username" : "audispain"
#         },
#         {"comments" : [
#     		{
#      			"id_media" : "2429379247628862182_1121839441",
#                   "texts":[
#                       { "user" : "alfonsofloress__", "text" : "Con este coche me voy Murcia hasta italia de una arrancada" }, 
#                       { "user" : "martiiineez_34", "text" : "Ufffff🔥🤤🤤" }
#                 ]
#     		},
#             {
#      			"id_media" : "2429083272555842514_1121839441",
#                   "texts":[
#                       { "user" : "emf_fotografia", "text" : "Uff !!!! Ese si es un coche que me apetece fotografiar !!!" }, 
#                       { "user" : "enri_pomme", "text" : "Que tengo que hacer para hacerle fotos a esa maldita bestia" }
#                 ]
#     		}
#         ],
#      	"social_media" : "Instagram",
#      	"date" : datetime.strptime("03-11-2020",'%d-%m-%Y'),
#      	"username" : "audispain"
#         },
#         {"comments" : [
#     		{
#      			"id_media" : "2429379247628862182_1121839441",
#                   "texts":[
#                       { "user" : "vicariapuentedura", "text" : "@audispain el RS7 de serie ya es la leche. Como el RS5 en verde." }, 
#                       { "user" : "maribel240114", "text" : "@mchkpro" }
#                 ]
#     		},
#             {
#      			"id_media" : "2429083272555842514_1121839441",
#                   "texts":[
#                       { "user" : "antonio_realtor", "text" : "la parrilla" }, 
#                       { "user" : "craemone", "text" : "las ópticas y la parilla frontal son impresionantes!! lástima que no me toque la lotería que no juego xD" }
#                 ]
#     		}
#         ],
#      	"social_media" : "Instagram",
#      	"date" : datetime.strptime("04-11-2020",'%d-%m-%Y'),
#      	"username" : "audispain"
#         },
#         {"comments" : [
#     		{
#      			"id_media" : "2429379247628862182_1121839441",
#                   "texts":[
#                       { "user" : "saaray11", "text" : "@norbergmr87" }, 
#                       { "user" : "mr.sashu", "text" : "@audispain No importa, yo seguiría llevando el coche con la misma clase👌🏻" }
#                 ]
#     		},
#             {
#      			"id_media" : "2429083272555842514_1121839441",
#                   "texts":[{ "user" : "amorsubito", "text" : "@audispain a mi de entrada cualquier Audi me hipnotiza....me deja turoleta no puedo evitarlo, yo estoy enamorada del mío.....i 💙 Q2" }, 
#                           { "user" : "antonio_realtor", "text" : "la parrilla" },
#                   ]
#     		}
#         ],
#      	"social_media" : "Instagram",
#      	"date" : datetime.strptime("05-11-2020",'%d-%m-%Y'),
#      	"username" : "audispain"
#         },
#         {"comments" : [
#     		{
#      			"id_media" : "2429379247628862182_1121839441",
#                   "texts":[{ "user" : "gerialbors", "text" : "@jangzanni q cojones vaya locura" }, 
#                           { "user" : "jangzanni", "text" : "@audispain tenéis razón... @bmwespana modernizaros anda" }
#                   ]
#     		},
#             {
#      			"id_media" : "2429083272555842514_1121839441",
#                   "texts":[
#                       { "user" : "goloson5", "text" : "@audispain ❤️❤️😍😍" }, 
#                       { "user" : "guillermo_aleman27", "text" : "@audispain de Audi" }, { "user" : "amorsubito", "text" : "Me da igual estando dentro de él....❤️💋😍😘" }
#                   ]
#     		}
#         ],
#      	"social_media" : "Instagram",
#      	"date" : datetime.strptime("06-11-2020",'%d-%m-%Y'),
#      	"username" : "audispain"
#         },
#         {"comments" : [
#     		{
#      			"id_media" : "2429379247628862182_1121839441",
#                   "texts":[{ "user" : "joaquinrdmz", "text" : "@audispain pues desde los 90 ha hecho 97k, está cuidado con mimo 😁" }, 
#                           {"user" : "joseluismmxviii", "text" : "@audispain es imposible que el RS5 sea confortable. Lo qye ganas en caballos lo pierdes en comodidad" }
#                 ]
#     		},
#             {
#      			"id_media" : "2429083272555842514_1121839441",
#                   "texts":[
#                       { "user" : "david.l.m_13", "text" : "@audispain todo" }, 
#                       { "user" : "barrio.25_30", "text" : "@audispain El interior del audi A3 sportback es espectacular" },
#                 ]
#     		}
#         ],
#      	"social_media" : "Instagram",
#      	"date" : datetime.strptime("07-11-2020",'%d-%m-%Y'),
#      	"username" : "audispain"
#         },
#     ]
#     for item in comments:
#         main_ops_object.common_data_object.insert_user_data(item, "test_comments")
        
#     # Delete all the records of the Postgres table in order to insert the data
#     main_ops_object.postgresdb_object.empty_table("testmedias")
#     main_ops_object.postgresdb_object.empty_table("testmediatitles")
#     main_ops_object.postgresdb_object.empty_table("testmediacomments")
#     main_ops_object.postgresdb_object.empty_table("testmediasevolution")
#     result = main_ops_object.perform_analysis("audispain", "test_media_evolution",
#               "Instagram", "31-10-2020", "02-11-2020")
#     assert type(result) == list and len(result) == 3

# def test16_perform_analysis():
#     """
#     Test to check the method which performs a specific analysis on the selected
#     user data getting the information from the Mongo database to Postgre database.
#     In this test, the analysis to perform is the Media Evolution on a set of more
#     than 7 days user data.
#     """
#     result = main_ops_object.perform_analysis("audispain", "test_media_evolution",
#               "Instagram", "31-10-2020", "07-11-2020")
#     assert type(result) == list and len(result) == 2
    
# def test17_perform_analysis():
#     """
#     Test to check the method which performs a specific analysis on the selected
#     user data getting the information from the Mongo database to Postgre database.
#     In this test, the analysis to perform is the Media Evolution on a set of three
#     days but it's been already done so the analysis results will be recovered 
#     in order to plot them directly.
#     """
#     result = main_ops_object.perform_analysis("audispain", "test_media_evolution",
#               "Instagram", "31-10-2020", "02-11-2020")
#     assert type(result) == dict

# def test18_perform_analysis():
#     """
#     Test to check the method which performs a specific analysis on the selected
#     user data getting the information from the Mongo database to Postgre database.
#     In this test, the analysis to perform is the Media Popularity on a set of three
#     days user data.
#     """
#     # Delete the previous records of the analysis table
#     main_ops_object.postgresdb_object.empty_table("testmediaspopularity")
#     result = main_ops_object.perform_analysis("audispain", "test_media_popularity",
#               "Instagram", "31-10-2020", "02-11-2020")
#     assert type(result) == list and len(result) == 2

# def test19_perform_analysis():
#     """
#     Test to check the method which performs a specific analysis on the selected
#     user data getting the information from the Mongo database to Postgre database.
#     In this test, the analysis to perform is the Media Popularity on a set of more
#     than 7 days user data.
#     """
#     result = main_ops_object.perform_analysis("audispain", "test_media_popularity",
#               "Instagram", "31-10-2020", "07-11-2020")
#     assert type(result) == list and len(result) == 2
    
# def test20_perform_analysis():
#     """
#     Test to check the method which performs a specific analysis on the selected
#     user data getting the information from the Mongo database to Postgre database.
#     In this test, the analysis to perform is the Media Popularity on a set of three
#     days user data. However, this analysis has been performed previously so the
#     analysis results will be recovered in order to plot them directly.
#     """
#     result = main_ops_object.perform_analysis("audispain", "test_media_popularity",
#               "Instagram", "31-10-2020", "02-11-2020")
#     assert type(result) == list

# def test21_perform_analysis():
#     """
#     Test to check the method which performs a specific analysis on the selected
#     user data getting the information from the Mongo database to Postgre database.
#     In this test, the analysis to perform is the Comment Sentiments on a set of 
#     one-day data.
#     """
#     main_ops_object.postgresdb_object.empty_table("testtextsentiments")
#     main_ops_object.postgresdb_object.empty_table("testcommentsentiments")
#     result = main_ops_object.perform_analysis("audispain", "test_comment_sentiment_analysis",
#               "Instagram", "31-10-2020", "01-11-2020")
#     assert type(result) == list and len(result) == 1
    
# def test22_perform_analysis():
#     """
#     Test to check the method which performs a specific analysis on the selected
#     user data getting the information from the Mongo database to Postgre database.
#     In this test, the analysis to perform is the Comment Sentiments on a set of 
#     one-day data. But this analysis has been performed previously so the analysis
#     results will be recovered in order to plot them directly.
#     """
#     result = main_ops_object.perform_analysis("audispain", "test_comment_sentiment_analysis",
#               "Instagram", "31-10-2020", "01-11-2020")
#     assert type(result) == dict 

# def test23_perform_analysis():
#     """
#     Test to check the method which performs a specific analysis on the selected
#     user data getting the information from the Mongo database to Postgre database.
#     In this test, the analysis to perform is the Title Sentiments on a set of 
#     one-day data.
#     """
#     result = main_ops_object.perform_analysis("audispain", "test_title_sentiment_analysis",
#               "Instagram", "31-10-2020", "01-11-2020")
#     assert type(result) == list and len(result) == 1
    
# def test24_perform_analysis():
#     """
#     Test to check the method which performs a specific analysis on the selected
#     user data getting the information from the Mongo database to Postgre database.
#     In this test, the analysis to perform is the Title Sentiments on a set of 
#     one-day data. But this analysis has been performed previously so the analysis
#     results will be recovered in order to plot them directly.
#     """
#     result = main_ops_object.perform_analysis("audispain", "test_title_sentiment_analysis",
#               "Instagram", "31-10-2020", "01-11-2020")
#     assert type(result) == dict
    
# def test25_perform_analysis():
#     """
#     Test to check the method which performs a specific analysis on the selected
#     user data getting the information from the Mongo database to Postgres database.
#     In this test, the analysis to perform is the User Behaviours on a set of 
#     one-day data.
#     """
#     # Delete the previous records of the analysis table
#     main_ops_object.postgresdb_object.empty_table("testuserbehaviours")
#     result = main_ops_object.perform_analysis("audispain", "test_user_behaviours",
#                 "Instagram", "31-10-2020", "01-11-2020")
#     assert type(result) == list and len(result) == 2
    
# def test26_perform_analysis():
#     """
#     Test to check the method which performs a specific analysis on the selected
#     user data getting the information from the Mongo database to Postgre database.
#     In this test, the analysis has been performed before so the results will be
#     recovered directly to plot them.
#     """
#     result = main_ops_object.perform_analysis("audispain", "test_user_behaviours",
#                 "Instagram", "31-10-2020", "01-11-2020")
#     assert type(result) == dict and len(result["date"]) == 2
