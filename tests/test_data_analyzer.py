#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File in which there are many tests to check the behaviour of the methods contained
in the class DataAnalyzer. Each one performs a different type of data analysis.

@author: Lidia Sánchez Mérida
"""
from datetime import time
import sys
import pytest
sys.path.append("src")
sys.path.append("src/data")
import data_analyzer 
from exceptions import ValuesNotFound, KeysNotFound, ExpectedSameSize \
    , InvalidLinePlotData, UsernameNotFound, ProfilesNotFound, InvalidBarPlotData \
    , UserActivityNotFound, PostInteractionsNotFound, InvalidPiePlotData \
    , InvalidSocialMediaSource, PostPopularityNotFound, TextTupleNotFound
    
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

def test1_plot_lines_chart():
    """
    Test to check the method which draws a line plot from the provided data.
    In this test, the provided values to plot are not valid so an
    exception will be raised.
    """
    with pytest.raises(InvalidLinePlotData):
        assert da.plot_lines_chart([1,2,3,4], None, None, None)

def test2_plot_lines_chart():
    """
    Test to check the method which draws a line plot from the provided data.
    In this test, the X labels are not provided so an exception will be raised.
    """
    values = [[1,5,4], [3,6,9], [7,2,0]]
    with pytest.raises(InvalidLinePlotData):
        assert da.plot_lines_chart(values, None, None, None)
        
def test3_plot_lines_chart():
    """
    Test to check the method which draws a line plot from the provided data.
    In this test, the Y title, plot title and file path are not provided
    so an exception will be raised.
    """
    values = [[1,5,4], [3,6,9], [7,2,0]]
    legend_labels = ["line 1", "line 2", "line 3"]
    x_labels = ["26/07", "27/07", "29/07"]
    with pytest.raises(InvalidLinePlotData):
        assert da.plot_lines_chart(values, legend_labels, x_labels, 123)
    
def test4_plot_lines_chart():
    """
    Test to check the method which draws a line plot from the provided data.
    """
    values = [[1,5,4], [3,6,9], [7,2,0]]
    legend_labels = ["line 1", "line 2", "line 3"]
    x_labels = ["26/07", "27/07", "29/07"]
    result = da.plot_lines_chart(values, legend_labels, x_labels, da.plot_tests_path+"test_lines_plot")
    assert result == True
    
def test1_profile_evolution():
    """
    Test to check the method which draws a line plot after analysing the evolution
    of the profile from a specific user. In this test, the username is not provided
    so an exception will be raised.
    """
    with pytest.raises(UsernameNotFound):
        assert da.profile_evolution(None, None)

def test2_profile_evolution():
    """
    Test to check the method which draws a line plot after analysing the evolution
    of the profile from a specific user. In this test, the list of profiles is not
    provided so an exception will be raised.
    """
    with pytest.raises(ProfilesNotFound):
        assert da.profile_evolution("lidiasm", None)
        
def test3_profile_evolution():
    """
    Test to check the method which draws a line plot after analysing the evolution
    of the profile from a specific user. In this test, the provided list of profiles 
    is not valid so an exception will be raised.
    """
    invalid_profile_list = [("20/10/2020", "12", "54", "27"),
                    ("22/10/2020", "15", "35")]
    with pytest.raises(ProfilesNotFound):
        assert da.profile_evolution("lidiasm", invalid_profile_list)
        
def test4_profile_evolution():
    """
    Test to check the method which draws a line plot after analysing the evolution
    of the profile from a specific user. 
    """
    profile_list = [("20/10/2020", "12", "54", "27"),
                    ("22/10/2020", "15", "100", "35"),
                    ("24/10/2020", "25", "104", "68"),
                    ("28/10/2020", "26", "148", "124")]
    result = da.profile_evolution("lidiasm", profile_list)
    time(5)
    assert result == True
    
def test5_profile_evolution():
    """
    Test to check the method which draws a line plot after analysing the evolution
    of the profile from a specific user. 
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
    time(5)
    assert result == True
    
def test1_plot_bars_chart():
    """
    Test to check the method which draws a bar plot from the provided data.
    In this test, there are not provided data so an exception will be raised.
    """
    with pytest.raises(InvalidBarPlotData):
        assert da.plot_bars_chart(None, None, None)

def test2_plot_bars_chart():
    """
    Test to check the method which draws a bar plot from the provided data.
    In this test, the path and file name to save the plot as an image are not provided
    so an exception will be raised.
    """
    values = [5, 2, 15, 8, 9]
    x_labels = ['label1', 'label2', 'label3', 'label4', 'label5']
    with pytest.raises(InvalidBarPlotData):
        assert da.plot_bars_chart(values, x_labels, None)
        
def test3_plot_bars_chart():
    """
    Test to check the method which draws a bar plot from the provided data.
    In this test, the path and file name to save the plot as an image are not provided
    so an exception will be raised.
    """
    values = [5, 2, 15, 8, 9]
    x_labels = ['label1', 'label2', 'label3', 'label4', 'label5']
    with pytest.raises(InvalidBarPlotData):
        assert da.plot_bars_chart(values, x_labels, da.plot_tests_path+"test_bar_plot", "")
        
def test4_plot_bars_chart():
    """
    Test to check the method which draws a bar plot from the provided data.
    """
    values = [5, 2, 15, 8, 9]
    x_labels = ['label1', 'label2', 'label3', 'label4', 'label5']
    result = da.plot_bars_chart(values, x_labels, da.plot_tests_path+"test_bar_plot")
    assert result == True

def test5_plot_bars_chart():
    """
    Test to check the method which draws a bar plot from the provided data.
    """
    values = [5, 2, 15, 8, 9]
    x_labels = ['label1', 'label2', 'label3', 'label4', 'label5']
    result = da.plot_bars_chart(values, x_labels, da.plot_tests_path+"test_bar_plot",
                          [-3, 13, -7, -1])
    assert result == True
    
def test1_user_activity():
    """
    Test to check the method which analyzes the user activity per week or more.
    In this test, the username is not provided so an exception will be raised.
    """
    with pytest.raises(UsernameNotFound):
        assert da.user_activity(None, None)
    
def test2_user_activity():
    """
    Test to check the method which analyzes the user activity per week or more.
    In this test, the user activity is not provided so an exception will be raised.
    """
    with pytest.raises(UserActivityNotFound):
        assert da.user_activity("lidiasm", None)
        
def test3_user_activity():
    """
    Test to check the method which analyzes the user activity per week or more.
    In this test, the provided user activity is not valid so an exception will be raised.
    """
    invalid_user_activity = [("24/10/2020"), ("25/10/2020", "125")]
    with pytest.raises(UserActivityNotFound):
        assert da.user_activity("lidiasm", invalid_user_activity)
        
def test4_user_activity():
    """
    Test to check the method which analyzes the user activity per week or more.
    In this test, the provided user activity is not valid so an exception will be raised.
    """
    invalid_user_activity = [("24/10/2020"), ("25/10/2020", "125"),
                              ("24/10/2020"), ("25/10/2020", "125"),
                              ("24/10/2020"), ("25/10/2020", "125"),
                              ("24/10/2020"), ("25/10/2020", "125")]
    with pytest.raises(UserActivityNotFound):
        assert da.user_activity("lidiasm", invalid_user_activity)

def test5_user_activity():
    """
    Test to check the method which analyzes the user activity per week or more.
    In this test, the provided user activity is not valid so an exception will be raised.
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
    assert result == True
        
def test6_user_activity():
    """
    Test to check the method which analyzes the user activity per week or more.
    In this test, the plot will show the user activity per week.
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
    time(5)
    assert result == True

def test1_post_evolution():
    """
    Test to check the method which draws a line plot after analysing the evolution
    of the post interactions. In this test, the username is not provided
    so an exception will be raised.
    """
    with pytest.raises(UsernameNotFound):
        assert da.post_evolution(None, None)

def test2_post_evolution():
    """
    Test to check the method which draws a line plot after analysing the evolution
    of the post interactions. In this test, the list of profiles is not
    provided so an exception will be raised.
    """
    with pytest.raises(PostInteractionsNotFound):
        assert da.post_evolution("lidiasm", None)
        
def test3_post_evolution():
    """
    Test to check the method which draws a line plot after analysing the evolution
    of the post interactions. In this test, the provided list of profiles 
    is not valid so an exception will be raised.
    """
    invalid_interactions = [("20/10/2020", "12", "54"), ("22/10/2020", "15")]
    with pytest.raises(PostInteractionsNotFound):
        assert da.post_evolution("lidiasm", invalid_interactions)
        
def test4_post_evolution():
    """
    Test to check the method which draws a line plot after analysing the evolution
    of the post interactions from a specific user. In this test, the analysis
    will be per a week.
    """
    post_interactions = [("20/10/2020", "128", "35"),
                    ("22/10/2020", "135", "48"),
                    ("24/10/2020", "147", "77"),
                    ("28/10/2020", "159", "89")]
    result = da.post_evolution("lidiasm", post_interactions)
    time(5)
    assert result == True
    
def test5_post_evolution():
    """
    Test to check the method which draws a line plot after analysing the evolution
    of the post interactions from a specific user. In this test, the analysis will
    be per more than a week.
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
    time(5)
    assert result == True
    
def test1_post_popularity():
    """
    Test to check the method which plots the best or worst posts from a user based
    on a selected set of interactions. In this test, the username is not provided
    so an exception will be raised.
    """
    with pytest.raises(UsernameNotFound):
        assert da.post_popularity(None, None, None)
        
def test2_post_popularity():
    """
    Test to check the method which plots the best or worst posts from a user based
    on a selected set of interactions. In this test, the social media source is
    not provided so an exception will be raised.
    """
    with pytest.raises(InvalidSocialMediaSource):
        assert da.post_popularity("lidia.96.sm", None, None)
        
def test3_post_popularity():
    """
    Test to check the method which plots the best or worst posts from a user based
    on a selected set of interactions. In this test, the provided social media
    source is not valid, so an exception will be raised.
    """
    with pytest.raises(InvalidSocialMediaSource):
        assert da.post_popularity("lidia.96.sm", "Invalid Social Media", None)
        
def test4_post_popularity():
    """
    Test to check the method which plots the best or worst posts from a user based
    on a selected set of interactions. In this test, the list of popular posts is
    not provided so an exception will be raised.
    """
    with pytest.raises(PostPopularityNotFound):
        assert da.post_popularity("lidia.96.sm", "Instagram", None)
        
def test5_post_popularity():
    """
    Test to check the method which plots the best or worst posts from a user based
    on a selected set of interactions. In this test, the provided list of popular
    posts is not valid so an exception will be raised.
    """
    popular_posts = [1,2,3,4]
    with pytest.raises(PostPopularityNotFound):
        assert da.post_popularity("lidia.96.sm", "Instagram", popular_posts)
        
def test6_post_popularity():
    """
    Test to check the method which plots the best or worst posts from a user based
    on a selected set of interactions. In this test, the provided list of popular
    posts is not valid so an exception will be raised.
    """
    popular_posts = [(1,2,3), (4,5,6), (7,8,9,10)]
    with pytest.raises(PostPopularityNotFound):
        assert da.post_popularity("lidia.96.sm", "Instagram", popular_posts)
        
def test7_post_popularity():
    """
    Test to check the method which plots the best or worst posts from a user based
    on a selected set of interactions. In this test, the data is similar to 
    Instagram data because the posts have titles. The metric to get the popularity
    is the average of likes.
    """
    popular_posts = [("Title of post 1", "URL", "24/10/2020", "Average likes: 1234"),
                     ("Title of post 2", "URL", "27/10/2020", "Average likes: 1122")]
    post_list = da.post_popularity("lidia.96.sm", "Instagram", popular_posts)
    check = [True for post in post_list if (len(post)) == 2]
    assert len(list(set(check))) == 1 and list(set(check))[0] == True

def test1_plot_pie_chart():
    """
    Test to check the method which draws a pie chart with the provided data and
    save it as an image. In this test, the values to show are not provided so
    an exception will be raised.
    """
    with pytest.raises(InvalidPiePlotData):
        assert da.plot_pie_chart(None, None, None, None)
        
def test2_plot_pie_chart():
    """
    Test to check the method which draws a pie chart with the provided data and
    save it as an image. In this test, the values to show have a different size
    from the number of labels so an exception will be raised.
    """
    with pytest.raises(InvalidPiePlotData):
        assert da.plot_pie_chart([120, 35, 107], ["Positive", "Negative"], None, None)
        
def test3_plot_pie_chart():
    """
    Test to check the method which draws a pie chart with the provided data and
    save it as an image. In this test, the file name is not provided so an exception
    will be raised.
    """
    with pytest.raises(InvalidPiePlotData):
        assert da.plot_pie_chart([120, 35, 107], ['Positive', 'Neutral', 'Negative'], 
                                 None, None)
        
def test4_plot_pie_chart():
    """
    Test to check the method which draws a pie chart with the provided data and
    save it as an image. In this test, the colours are not provided so they will
    be chosen randomly.
    """
    values = [120, 35, 107]
    labels = ['Positive', 'Neutral', 'Negative']
    file = da.plot_tests_path + "test_pie_plot"
    result = da.plot_pie_chart(values, labels, file, None)
    assert result == True
    
def test5_plot_pie_chart():
    """
    Test to check the method which draws a pie chart with the provided data and
    save it as an image. In this test, a list of colours are provided in order
    to plot each piece of pie of its related colour.
    """
    time(5)
    values = [140, 78, 92]
    labels = ['Positive', 'Neutral', 'Negative']
    file = da.plot_tests_path + "test_pie_plot"
    result = da.plot_pie_chart(values, labels, file, ["green", "yellow", "red"])
    assert result == True
    
def test1_sentiment_analysis_text():
    """
    Test to check the method which performs a sentiment analysis based on a list
    of texts. In this test, the username of the studied user is not provided so
    an exception will be raised.
    """
    with pytest.raises(UsernameNotFound):
        da.sentiment_analysis_text(None, None)
        
def test2_sentiment_analysis_text():
    """
    Test to check the method which performs a sentiment analysis based on a list
    of texts. In this test, the texts to analyse are not provided so
    an exception will be raised.
    """
    with pytest.raises(TextTupleNotFound):
        da.sentiment_analysis_text("lidia.96.sm", [])
        
def test3_sentiment_analysis_text():
    """
    Test to check the method which performs a sentiment analysis based on a list
    of texts. The provided texts to analyse are not valid so an exception will be
    raised.
    """
    with pytest.raises(TextTupleNotFound):
        da.sentiment_analysis_text("lidia.96.sm", [1,2,3,4])
        
def test4_sentiment_analysis_text():
    """
    Test to check the method which performs a sentiment analysis based on a list
    of texts. The results are plotted on a pie chart.
    """
    text_list = [('1', '🔥'), ('2', '@audispain Electric blue'), 
                 ('3', '@audispain true to the white AUDI ALWAYSEE !!!! 😎'), 
                 ('4', '@audispain I love it in white and dark gray. Thanks for filling Instagram with perfection. ❤️'), 
                 ('5', '@audispain could donate me one 🙌, even if it is an old model, I would be happy to be able to walk my daughter'), 
                 ('6', 'I black ..... uauuuuu awesome black👏👏👏🏼👏🏻👏👏👏'), 
                 ('7', 'Personally the typical metallic blue color of the rs 😍'), 
                 ('8', '@audispain if my Q2 is black and I love it ..... 💋💋'), 
                 ('9', '😍'), ('10', 'A pure road machine 👏👏❤️')]
    result = da.sentiment_analysis_text("lidia.96.sm", text_list)
    assert result == True