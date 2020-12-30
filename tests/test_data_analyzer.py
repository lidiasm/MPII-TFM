#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File in which there are many tests to check the behaviour of the methods contained
in the class DataAnalyzer. Each one performs a different type of data analysis.

@author: Lidia Sánchez Mérida
"""
import sys
import pytest
sys.path.append("src")
sys.path.append("src/data")
import data_analyzer 
from exceptions import ValuesNotFound, KeysNotFound, ExpectedSameSize \
    , UsernameNotFound, ProfilesNotFound \
    , UserActivityNotFound, PostInteractionsNotFound \
    , PostPopularityNotFound, TextNotFound, SentimentNotFound, TextDataNotFound
    
# DataAnalyzer object to run the data analyzer methods
da = data_analyzer.DataAnalyzer()

def test1_get_values_per_one_week():
    """
    Test to check the method which gets a list of values and links to their
    related keys per one week. In this test, the list of values is not 
    provided so an exception will be raised.
    """
    with pytest.raises(ValuesNotFound):
        assert da.get_values_per_one_week(None, None)

def test2_get_values_per_one_week():
    """
    Test to check the method which gets a list of values and links to their
    related keys peer one week. In this test, the list of keys is not provided
    so an exception will be raised.
    """
    values = [('12/10/2020', '14'), ('14/10/2020', '21'), ('16/10/2020', '54')]
    with pytest.raises(KeysNotFound):
        assert da.get_values_per_one_week(values, None)
        
def test3_get_values_per_one_week():
    """
    Test to check the method which gets a list of values and links to their
    related keys peer one week. In this test, the list of values for each 
    record has not the same size than the number of keys, so an exception will be raised.
    """
    values = [('12/10/2020', '14'), ('14/10/2020', '21'), ('16/10/2020', '54')]
    keys = ['date']
    with pytest.raises(ExpectedSameSize):
        assert da.get_values_per_one_week(values, keys)
        
def test4_get_values_per_one_week():
    """
    Test to check the method which gets a list of values and links to their
    related keys per one week. The returned dict contains the keys and their 
    related list of values.
    """
    values = [('12/10/2020', '14'), ('14/10/2020', '21'), ('16/10/2020', '54')]
    keys = ['date', 'field_one']
    result = da.get_values_per_one_week(values, keys)
    assert len(list(result.keys())) == len(keys)
    
def test1_get_values_per_many_weeks():
    """
    Test to check the method which gets a list of values and links to their
    related keys per more than a week. In this test, the list of values is 
    not provided so an exception will be raised.
    """
    with pytest.raises(ValuesNotFound):
        assert da.get_values_per_many_weeks(None, None)

def test2_get_values_per_many_weeks():
    """
    Test to check the method which gets a list of values and links to their
    related keys per more than a week. In this test, the list of keys is not 
    provided so an exception will be raised.
    """
    values = [('12/10/2020', '14'), ('14/10/2020', '21'), ('16/10/2020', '54')]
    with pytest.raises(KeysNotFound):
        assert da.get_values_per_many_weeks(values, None)
        
def test3_get_values_per_many_weeks():
    """
    Test to check the method which gets a list of values and links to their
    related keys per more than a week. In this test, the list of values for 
    each record has not the same size than the number of keys, so an exception
    will be raised.
    """
    values = [('12/10/2020', '14'), ('14/10/2020', '21'), ('16/10/2020', '54')]
    keys = ['date']
    with pytest.raises(ExpectedSameSize):
        assert da.get_values_per_many_weeks(values, keys)
        
def test4_get_values_per_many_weeks():
    """
    Test to check the method which gets a list of values and links to their
    related keys per more than a week. The returned dict contains the keys and 
    their related list of values.
    """
    values = [('12/10/2020', '14'), ('14/10/2020', '21'), ('16/10/2020', '54'),
          ('18/10/2020', '24'), ('19/10/2020', '26'), ('20/10/2020', '29'),
          ('26/10/2020', '34'), ('14/10/2020', '37'), ('16/10/2020', '42'),
          ('29/10/2020', '54'), ('14/10/2020', '51'), ('16/10/2020', '63')]
    keys = ['date', 'field_one']
    result = da.get_values_per_many_weeks(values, keys)
    assert len(list(result.keys())) == len(keys)
    
def test1_profile_evolution():
    """
    Test to check the method which computes the evolution of the number of followers,
    followings and posts during a specific period of time. In this test, the username
    of the account to study is not provided so an exception will be raised.
    """
    with pytest.raises(UsernameNotFound):
        assert da.profile_evolution(None, None)

def test2_profile_evolution():
    """
    Test to check the method which computes the evolution of the number of followers,
    followings and posts during a specific period of time. In this test, the profiles
    to analyze are not provided so an exception will be raised.
    """
    with pytest.raises(ProfilesNotFound):
        assert da.profile_evolution("lidiasm", None)
        
def test3_profile_evolution():
    """
    Test to check the method which computes the evolution of the number of followers,
    followings and posts during a specific period of time. In this test, the provided
    profiles to analyze are not valid so an exception will be raised.
    """
    invalid_profile_list = [("20/10/2020", "12", "54", "27"),
                    ("22/10/2020", "15", "35")]
    with pytest.raises(ProfilesNotFound):
        assert da.profile_evolution("lidiasm", invalid_profile_list)
        
def test4_profile_evolution():
    """
    Test to check the method which computes the evolution of the number of followers,
    followings and posts during a specific period of time. In this test, there is a set
    of four profiles to analyze so their data will be returned directly.
    """
    profile_list = [("20/10/2020", "12", "54", "27"),
                    ("22/10/2020", "15", "100", "35"),
                    ("24/10/2020", "25", "104", "68"),
                    ("28/10/2020", "26", "148", "124")]
    result = da.profile_evolution("lidiasm", profile_list)
    assert type(result) == dict and len(result["date"]) == len(profile_list)

def test5_profile_evolution():
    """
    Test to check the method which computes the evolution of the number of followers,
    followings and posts during a specific period of time. In this test, there is a set
    of eleven profiles to analyze so the method will compute the average of each
    field per week.
    """
    profile_list = [("20/10/2020", "12", "54", "27"),
                    ("21/10/2020", "15", "100", "35"),
                    ("22/10/2020", "25", "104", "68"),
                    ("23/10/2020", "26", "148", "124"),
                    ("24/10/2020", "28", "135", "124"),
                    ("25/10/2020", "27", "121", "124"),
                    ("26/10/2020", "29", "125", "124"),
                    ("27/10/2020", "29", "126", "124"),
                    ("28/10/2020", "31", "148", "128"),
                    ("29/10/2020", "35", "142", "132"),
                    ("30/10/2020", "34", "139", "132"),
                    ("31/10/2020", "40", "145", "140")]
    result = da.profile_evolution("lidiasm", profile_list)
    assert type(result) == dict and len(result["date"]) == 2
    
def test1_user_activity():
    """
    Test to check the method which computes the user activity based on the number
    of uploaded posts during a specific period of time. In this test, the username
    of the account to study is not provided so an exception will be raised.
    """
    with pytest.raises(UsernameNotFound):
        assert da.user_activity(None, None)
    
def test2_user_activity():
    """
    Test to check the method which computes the user activity based on the number
    of uploaded posts during a specific period of time. In this test, the list of 
    uploaded posts is not provided so an exception will be raised.
    """
    with pytest.raises(UserActivityNotFound):
        assert da.user_activity("lidiasm", None)
        
def test3_user_activity():
    """
    Test to check the method which computes the user activity based on the number
    of uploaded posts during a specific period of time. In this test, the provided
    list of uploaded posts is not valid so an exception will be raised.
    """
    invalid_user_activity = [("24/10/2020"), ("25/10/2020", "125")]
    with pytest.raises(UserActivityNotFound):
        assert da.user_activity("lidiasm", invalid_user_activity)

def test4_user_activity():
    """
    Test to check the method which computes the user activity based on the number
    of uploaded posts during a specific period of time. In this test, there are seven
    records to analyze so they will be returned directly.
    """
    user_activity = [("20/10/2020", "12"), 
                      ("21/10/2020", "15"),
                      ("22/10/2020", "20"),
                      ("23/10/2020", "25"),
                      ("25/10/2020", "31"),
                      ("27/10/2020", "33"),
                      ("28/10/2020", "38")
                      ]
    result = da.user_activity("lidiasm", user_activity)
    assert type(result) == dict and len(result["date"]) == len(user_activity)
        
def test5_user_activity():
    """
    Test to check the method which computes the user activity based on the number
    of uploaded posts during a specific period of time. In this test, there are more
    than seven records to analyze so the method will compute the required averages per week.
    """
    user_activity = [("20/10/2020", "12"), 
                      ("21/10/2020", "15"),
                      ("22/10/2020", "20"),
                      ("23/10/2020", "25"),
                      ("25/10/2020", "31"),
                      ("27/10/2020", "33"),
                      ("28/10/2020", "38"),
                      
                      ("29/10/2020", "39"),
                      ("29/10/2020", "37"),
                      ("30/10/2020", "38"),
                      ("31/10/2020", "40"),
                      ]
    result = da.user_activity("lidiasm", user_activity)
    assert type(result) == dict and len(result["date"]) == 2

def test1_post_evolution():
    """
    Test to check the method which gets how interesting the posts are based on
    the interactions from the members of the social media. In this test, the username
    of the account to study is not provided so an exception will be raised.
    """
    with pytest.raises(UsernameNotFound):
        assert da.post_evolution(None, None)

def test2_post_evolution():
    """
    Test to check the method which gets how interesting the posts are based on
    the interactions from the members of the social media. In this test, the list
    of posts is not provided so an exception will be raised.
    """
    with pytest.raises(PostInteractionsNotFound):
        assert da.post_evolution("lidiasm", None)
        
def test3_post_evolution():
    """
    Test to check the method which gets how interesting the posts are based on
    the interactions from the members of the social media. In this test, the provided
    list of posts is not valid so an exception will be raised.
    """
    invalid_interactions = [("20/10/2020", "12", "54"), ("22/10/2020", "15")]
    with pytest.raises(PostInteractionsNotFound):
        assert da.post_evolution("lidiasm", invalid_interactions)
        
def test4_post_evolution():
    """
    Test to check the method which gets how interesting the posts are based on
    the interactions from the members of the social media. In this test, there are seven
    records to analyze so they will be returned directly.
    """
    post_interactions = [("20/10/2020", "128", "35"),
                        ("22/10/2020", "135", "48"),
                        ("24/10/2020", "147", "77"),
                        ("28/10/2020", "159", "89")]
    result = da.post_evolution("lidiasm", post_interactions)
    assert type(result) == dict and len(result["date"]) == len(post_interactions)
    
def test5_post_evolution():
    """
    Test to check the method which gets how interesting the posts are based on
    the interactions from the members of the social media. In this test, there are more
    than seven records to analyze so the method will compute the required averages per week.
    """
    post_interactions = [("20/10/2020", "12", "54"),
                    ("21/10/2020", "125", "95"),
                    ("22/10/2020", "135", "124"),
                    ("23/10/2020", "146", "138"),
                    ("24/10/2020", "149", "149"),
                    ("25/10/2020", "178", "151"),
                    ("26/10/2020", "180", "168"),
                    ("27/10/2020", "225", "172"),
                    ("28/10/2020", "235", "205"),
                    ("29/10/2020", "249", "215"),
                    ("30/10/2020", "245", "245"),
                    ("31/10/2020", "278", "289")]
    result = da.post_evolution("lidiasm", post_interactions)
    assert type(result) == dict and len(result["date"]) == 2
    
def test1_post_popularity():
    """
    Test to check the method which gets the best/worst posts from an user during
    a specific period of time. In this test, the username of the account to 
    study is not provided so an exception will be raised.
    """
    with pytest.raises(UsernameNotFound):
        assert da.post_popularity(None, None)
        
def test2_post_popularity():
    """
    Test to check the method which gets the best/worst posts from an user during
    a specific period of time. In this test, the posts to analyze are
    not provided so an exception will be raised.
    """
    with pytest.raises(PostPopularityNotFound):
        assert da.post_popularity("lidia.96.sm", None)
        
def test3_post_popularity():
    """
    Test to check the method which gets the best/worst posts from an user during
    a specific period of time. In this test, the provided posts to analyze are
    not valid so an exception will be raised.
    """
    with pytest.raises(PostInteractionsNotFound):
        assert da.post_popularity("lidia.96.sm", [[1,2,3,4]])
        
def test4_post_popularity():
    """
    Test to check the method which gets the best/worst posts from an user during
    a specific period of time. In this test, the posts will be sorted
    by the average number of likes and comments in descending order.
    """
    posts = [('123', '145', '174'), ('456', '45', '78'), ('789', '485', '25'), ('012', '489', '584')]
    result = da.post_popularity("lidia.96.sm", posts)
    assert type(result) == list
    
def test1_sentiment_analysis_text():
    """
    Test to check the method which performs a sentiment analysis based on a list
    of texts. In this test, the username of the account to study is not provided so
    an exception will be raised.
    """
    with pytest.raises(UsernameNotFound):
        da.sentiment_analysis_text(None, None)
        
def test2_sentiment_analysis_text():
    """
    Test to check the method which performs a sentiment analysis based on a list
    of texts. In this test, the texts to analyze are not provided so
    an exception will be raised.
    """
    with pytest.raises(TextDataNotFound):
        da.sentiment_analysis_text("lidia.96.sm", [])
        
def test3_sentiment_analysis_text():
    """
    Test to check the method which performs a sentiment analysis based on a list
    of texts. The provided texts to analyze are not valid so an exception will be
    raised.
    """
    with pytest.raises(TextNotFound):
        da.sentiment_analysis_text("lidia.96.sm", [1,2,3])
        
def test4_sentiment_analysis_text():
    """
    Test to check the method which performs a sentiment analysis based on a list
    of texts. The method will return a list of tuples with the analyzed text without
    preprocessing, the identified sentiment as well as its polarity degree.
    """
    text_list = [('1', '🔥','🔥'), ('2', '@audispain Azul eléctrico','@audispain Electric blue'), 
                  ('3', '@audispain verdad que blanco AUDI SIEMPREE !!!! 😎', '@audispain true to the white AUDI ALWAYSEE !!!! 😎'), 
                  ('4', '@audispain Me encanta en blanco y gris oscuro. Gracias por llenar Instagram con la perfección. ❤️','@audispain I love it in white and dark gray. Thanks for filling Instagram with perfection. ❤️'), 
                  ('5', '@audispain podríais donarme uno 🙌, aunque sea un modelo viejo, me encantaría poder pasear a mi hija', '@audispain could donate me one 🙌, even if it is an old model, I would be happy to be able to walk my daughter'), 
                  ('5', 'Yo negro ..... uauuuuu precio negro👏👏👏🏼👏🏻👏👏👏', 'I black ..... uauuuuu awesome black👏👏👏🏼👏🏻👏👏👏'), 
                  ('6', 'Personamelmente el típico color azul metálico del rs 😍', 'Personally the typical metallic blue color of the rs 😍'), 
                  ('7', '@audispain si mi Q2 es negro y me encanta ..... 💋💋', '@audispain if my Q2 is black and I love it ..... 💋💋'), 
                  ('8', '😍', '😍'), ('9', 'Una pura máquina de carretera 👏👏❤️', 'A pure road machine 👏👏❤️')]
    result = da.sentiment_analysis_text("lidia.96.sm", text_list)
    assert type(result) == list and len(result) == len(text_list)

def test1_user_behaviours():
    """
    Test to check the method which gets the evolution of the number of haters
    and friends based on a performed sentiment analysis during a specific period 
    of time. In this test, the username of the account to study is not provided so 
    an exception will be raised.
    """
    with pytest.raises(UsernameNotFound):
        da.user_behaviours(None, None)
        
def test2_user_behaviours():
    """
    Test to check the method which gets the evolution of the number of haters
    and friends based on a performed sentiment analysis during a specific period 
    of time. In this test, the list of identified sentiments is not provided 
    so an exception will be raised.
    """
    with pytest.raises(SentimentNotFound):
        da.user_behaviours("lidia.96.sm", None)
        
def test3_user_behaviours():
    """
    Test to check the method which gets the evolution of the number of haters
    and friends based on a performed sentiment analysis during a specific period 
    of time. In this test, the provided list of sentiments is not valid so an
    exception will be raised.
    """
    user_list = [{"author":"user1", "sentiment":"pos"},
                  {"date":"24/10/2020", "author":"user2", "sentiment":"neg"}]
    with pytest.raises(SentimentNotFound):
        da.user_behaviours("lidia.96.sm", user_list)
        
def test4_user_behaviours():
    """
    Test to check the method which gets the evolution of the number of haters
    and friends based on a performed sentiment analysis during a specific period 
    of time. In this test, the list of posts is less than seven days so the analysis
    results will be per day.
    """
    user_list = [{"date":"24/10/2020", "author":"user1", "sentiment":"pos"},
                  {"date":"24/10/2020", "author":"user2", "sentiment":"neg"},
                  {"date":"24/10/2020", "author":"user1", "sentiment":"neu"},
                  {"date":"24/10/2020", "author":"user1", "sentiment":"pos"},
                  {"date":"25/10/2020", "author":"user3", "sentiment":"none"},
                  {"date":"25/10/2020", "author":"user3", "sentiment":"pos"},
                  {"date":"26/10/2020", "author":"user1", "sentiment":"neg"},
                  {"date":"26/10/2020", "author":"user2", "sentiment":"none"},
                  {"date":"26/10/2020", "author":"user4", "sentiment":"pos"},
                  {"date":"27/10/2020", "author":"user1", "sentiment":"neu"},
                  {"date":"28/10/2020", "author":"user1", "sentiment":"pos"}]
    result = da.user_behaviours("lidia.96.sm", user_list)
    assert type(result) == dict
    
def test6_user_behaviours():
    """
    Test to check the method which gets the evolution of the number of haters
    and friends based on a performed sentiment analysis during a specific period 
    of time. In this test, the list of posts is more than seven days so the analysis
    results will be per week.
    """
    user_list = [{"date":"24/10/2020", "author":"user1", "sentiment":"pos"}, 
                  {"date":"24/10/2020", "author":"user2", "sentiment":"neg"},
                  {"date":"25/10/2020", "author":"user1", "sentiment":"neu"}, {"date":"25/10/2020", "author":"user1", "sentiment":"pos"},
                  {"date":"26/10/2020", "author":"user3", "sentiment":"none"}, {"date":"26/10/2020", "author":"user3", "sentiment":"pos"},
                  {"date":"27/10/2020", "author":"user1", "sentiment":"neg"}, {"date":"27/10/2020", "author":"user2", "sentiment":"none"},
                  {"date":"28/10/2020", "author":"user4", "sentiment":"pos"}, {"date":"28/10/2020", "author":"user1", "sentiment":"neg"},
                  {"date":"29/10/2020", "author":"user1", "sentiment":"neg"}, {"date":"29/10/2020", "author":"user1", "sentiment":"neg"},
                  {"date":"30/10/2020", "author":"user1", "sentiment":"neg"}, {"date":"30/10/2020", "author":"user1", "sentiment":"neg"},
                  {"date":"31/10/2020", "author":"user1", "sentiment":"neg"}, {"date":"31/10/2020", "author":"user1", "sentiment":"neg"},
                  {"date":"32/10/2020", "author":"user1", "sentiment":"pos"}, {"date":"32/10/2020", "author":"user1", "sentiment":"neg"}]
    result = da.user_behaviours("lidia.96.sm", user_list)
    assert type(result) == dict