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
from exceptions import InvalidPlotData, CommentsListNotFound, CommentsDictNotFound \
    , SentimentAnalysisNotFound, BehaviourAnalysisNotFound, InvalidSentiment \
    , ProfilesListNotFound, ProfileDictNotFound, UsernameNotFound, InvalidPlotType
    
"""DataAnalyzer object to run the data analyzer methods"""
da = data_analyzer.DataAnalyzer()

def test1_pie_plot():
    """Test to check the method which draws pie plots without providing any data.
        It will raise an exception."""
    with pytest.raises(InvalidPlotData):
        assert da.pie_plot({}, {}, {}, {})

def test2_pie_plot():
    """Test to check the method which draws pie plots without providing values,
        labels and colors data without the same lenght. It will raise an exception."""
    values = [10, 5, 2, 2]
    labels = ['positive', 'neutral', 'negative']
    with pytest.raises(InvalidPlotData):
        assert da.pie_plot(values, labels, "", "")

def test3_pie_plot():
    """Test to check the method which draws pie plots without providing valid
        plot and file names. It will raise an exception."""
    values = [10, 5, 2]
    labels = ['positive', 'neutral', 'negative']
    with pytest.raises(InvalidPlotData):
        assert da.pie_plot(values, labels, "", "")

def test4_pie_plot():
    """Test to draw a pie plot and save it to a PNG file."""
    values = [10, 5, 2]
    labels = ['positive', 'neutral', 'negative']
    colors = ['yellowgreen', 'gold', 'lightcoral']
    title = "Test pie plot"
    file_name = "test_pie_plot"
    assert da.pie_plot(values, labels, title, file_name, colors) == True

def test5_pie_plot():
    """Test to draw a pie plot and save it to a PNG file."""
    values = [10, 5, 2]
    labels = ['positive', 'neutral', 'negative']
    title = "Test pie plot"
    file_name = "test_pie_plot_2"
    assert da.pie_plot(values, labels, title, file_name) == True

def test1_bar_and_line_plot():
    """Test to check the method which draws bar/line plots without a valid plot type.
        It will raise an exception."""
    with pytest.raises(InvalidPlotType):
        assert da.bar_and_line_plot("", {}, {}, {}, {}, {})

def test2_bar_and_line_plot():
    """Test to check the method which draws bar/line plots without a valid plot type.
        It will raise an exception."""
    with pytest.raises(InvalidPlotData):
        assert da.bar_and_line_plot("B", {}, {}, {}, {}, {})

def test3_bar_and_line_plot():
    """Test to check the method which draws bar plots without providing valid data.
        It will raise an exception. It will raise an exception."""
    values = [10, 5, 2, 15, 8, 9]
    x_labels = ['user1', 'user3', 'user5', 'user2', 'user10']
    with pytest.raises(InvalidPlotData):
        assert da.bar_and_line_plot("B",values, x_labels, {}, {}, {})
        
def test4_bar_and_line_plot():
    """Test to check the method which draws bar plots without providing valid data.
        It will raise an exception. It will raise an exception."""
    values = [10, 5, 2, 15, 8]
    x_labels = ['user1', 'user3', 'user5', 'user2', 'user10']
    with pytest.raises(InvalidPlotData):
        assert da.bar_and_line_plot("B",values, x_labels, {}, {}, {})
        
def test5_bar_and_line_plot():
    """Test to draw a bar plot about user data storing it into a file choosing the
        color of each bar randomly."""
    values = [10, 5, 2, 15, 8]
    x_labels = ['user1', 'user3', 'user5', 'user2', 'user10']
    result = da.bar_and_line_plot("B", values, x_labels, "Users", "Test bar plot", "test_bar_plot",)
    assert result == True

def test6_bar_and_line_plot():
    """Test to draw a line plot about user data storing it into a file choosing the
        color of the line and the marker randomly."""
    values = [10, 5, 2, 15, 8]
    x_labels = ['user1', 'user3', 'user5', 'user2', 'user10']
    result = da.bar_and_line_plot("L", values, x_labels, "Users", "Test line plot", "test_line_plot",)
    assert result == True

def test1_profile_evolution():
    """Test to check the method which gets the evolution of some fields from
        a user profile such us the number of followers, followings and medias.
        In this case there are not data provided so it will raise an exception."""
    with pytest.raises(ProfilesListNotFound):
        assert da.profile_evolution([])

def test2_profile_evolution():
    """Test to check the method which gets the evolution of some fields from
        a user profile such us the number of followers, followings and medias.
        In this case the provided data is not valid so it will raise an exception."""
    with pytest.raises(ProfileDictNotFound):
        assert da.profile_evolution([1, 2])      
        
def test3_profile_evolution():
    """Test to check the method which gets the evolution of some fields from
        a user profile such us the number of followers, followings and medias.
        In this case the provided data is not valid so it will raise an exception."""
    with pytest.raises(ProfileDictNotFound):
        assert da.profile_evolution([{'user':'u1'}, {'user':'u2'}])
        
def test4_profile_evolution():
    """Test to check the method which gets the evolution of some fields from
        a user profile such us the number of followers, followings and medias.
        In this case the provided data are two profiles from different users
        so it will raise an exception."""
    profile1 = {"username" : "lidia.96.sm", "n_followings":124, "n_followers" : 61,
                "n_medias":24, "date" : "27-06-2020"}
    profile2 = {"username" : "leila.59", "n_followings":124, "n_followers" : 61,
                "n_medias":125, "date" : "26-06-2020"}
    with pytest.raises(UsernameNotFound):
        assert da.profile_evolution([profile1, profile2])

def test5_profile_evolution():
    """Test to get the evolution of some fields from a user profile drawing them
        in bar plots."""
    profile1 = {"username" : "lidia.96.sm", "n_followings":120, "n_followers" : 122,
                "n_medias":30, "date" : "27-06-2020"}
    profile2 = {"username" : "lidia.96.sm", "n_followings":115, "n_followers" : 89,
                "n_medias":28, "date" : "26-06-2020"}
    profile3 = {"username" : "lidia.96.sm", "n_followings":120, "n_followers" : 56,
                "n_medias":24, "date" : "25-06-2020"}
    profile4 = {"username" : "lidia.96.sm", "n_followings":120, "n_followers" : 35,
                "n_medias":22, "date" : "20-06-2020"}
    profile5 = {"username" : "lidia.96.sm", "n_followings":98, "n_followers" : 15,
                "n_medias":20, "date" : "15-06-2020"}
    profile6 = {"username" : "lidia.96.sm", "n_followings":85, "n_followers" : 10,
                "n_medias":15, "date" : "10-06-2020"}
    assert da.profile_evolution([profile1, profile2, profile3, profile4, profile5, profile6]) == True
    
def test1_comments_sentiment_analyzer():
    """Test to check the sentiment analyzer without providing the right type of
        data to analyze. So it will raise an exception."""
    with pytest.raises(CommentsListNotFound):
        assert da.comments_sentiment_analyzer({})
        
def test2_comments_sentiment_analyzer():
    """Test to check the sentiment analyzer without providing the right type of
        data to analyze. So it will raise an exception."""
    comments = [{'user':'u1', 'preproc_comment':'alcohollll alcohol love friend'},
                {'user':'u2', 'comment':'drooling_face drooling_face drooling_face'}]
    with pytest.raises(CommentsDictNotFound):
        assert da.comments_sentiment_analyzer(comments)
    
def test3_comments_sentiment_analyzer():
    """Test to get the sentiments of the comments writen in the posts of a specific
        user in order to get different kinds of users, such as friends, haters, ...."""
    comments = [{'user':'u1', 'preproc_comment':'alcohollll alcohol love friend'},
                {'user':'u2', 'preproc_comment': 'drooling face drooling face drooling face'},
                {'user':'u2', 'preproc_comment':'would come back'},
                {'user':'u2', 'preproc_comment':'handsome'},
                {'user':'u5', 'preproc_comment':'smiling face heart eyes smiling face heart eyes smiling face heart eyes'}]
    result = da.comments_sentiment_analyzer(comments)
    assert type(result) == list

def test1_behaviour_patterns():
    """Test to check the method which tries to get behaviour patterns from the sentiment
        analysis without providing the sentiment analysis result. It will raise an exception."""
    with pytest.raises(SentimentAnalysisNotFound):
        assert da.behaviour_patterns([])

def test2_behaviour_patterns():
    """Test to check the method which tries to get behaviour patterns from the sentiment
        analysis without providing the correct sentiment analysis data. It will raise
        an exception."""
    comments = [{'user':'u1', 'preproc_comment':'alcohollll alcohol love friend'},
                {'user':'u2', 'comment':'drooling_face drooling_face drooling_face'}]
    with pytest.raises(CommentsDictNotFound):
        assert da.behaviour_patterns(comments)

def test3_behaviour_patterns():
    """Test to get the behaviour patterns from the sentiment analysis result in order
        to get the number of positive, neutral and negative comments of each user who
        wrote one or more comments to posts of a specific user."""
    sentiments = [
        {'user': 'u1', 'preproc_comment': 'alcohollll alcohol love friend', 'sentiment': 'neu', 'polarity': 0.66}, 
        {'user': 'u2', 'preproc_comment': 'drooling face drooling face drooling face', 'sentiment': 'pos', 'polarity': 0.58},
        {'user': 'u2', 'preproc_comment': 'would come back', 'sentiment': 'pos', 'polarity': 0.793}, 
        {'user': 'u2', 'preproc_comment': 'handsome', 'sentiment': 'pos', 'polarity': 0.886}, 
        {'user': 'u5', 'preproc_comment': 'smiling face with heart eyes smiling face with heart eyes smiling face with heart eyes', 'sentiment': 'pos', 'polarity': 0.948}
        ]
    behaviour_patterns_result = da.behaviour_patterns(sentiments)
    assert type(behaviour_patterns_result) == list

def test1_get_general_behaviour():
    """Test to get the general data about users behaviour from the comments of posts
        of a specific user without providing the comments data. It will raise an exception."""
    with pytest.raises(SentimentAnalysisNotFound):
        assert da.get_general_behaviour(None)
        
def test2_get_general_behaviour():
    """Test to check the method which gets the friends/haters of a specific user
        from the behaviour patterns found without providing the right data."""
    comments = [{'user':'u1', 'preproc_comment':'alcohollll alcohol love friend'},
                {'user':'u2', 'comment':'drooling_face drooling_face drooling_face'}]
    with pytest.raises(CommentsDictNotFound):
        assert da.get_general_behaviour(comments)
        
def test3_get_general_behaviour():
    """Test to get the users who wrote negative comments or haters to posts of 
        a specific user. It will plot maximum 10 haters on a bar graphic."""
    data = [
        {'user': 'u1', 'preproc_comment': 'alcohollll alcohol love friend', 'sentiment': 'neu', 'polarity': 0.66}, 
        {'user': 'u2', 'preproc_comment': 'drooling face drooling face drooling face', 'sentiment': 'pos', 'polarity': 0.58},
        {'user': 'u2', 'preproc_comment': 'would come back', 'sentiment': 'neu', 'polarity': 0.793}, 
        {'user': 'u2', 'preproc_comment': 'handsome', 'sentiment': 'pos', 'polarity': 0.886}, 
        {'user': 'u5', 'preproc_comment': 'smiling face heart eyes smiling face heart eyes smiling face heart eyes', 'sentiment': 'pos', 'polarity': 0.948},
        {'user': 'u6', 'preproc_comment': 'fool', 'sentiment': 'neg', 'polarity': 0.55},
        {'user': 'u6', 'preproc_comment': 'awesome', 'sentiment': 'neg', 'polarity': 0.15}
        ]
    plot_general = da.get_general_behaviour(data)
    assert plot_general == True
    
def test1_get_haters_or_friends():
    """Test to check the method which gets the friends/haters of a specific user
        from the behaviour patterns found without providing the sentiment to plot."""
    with pytest.raises(InvalidSentiment):
        assert da.get_haters_or_friends([], 2020)

def test2_get_haters_or_friends():
    """Test to check the method which gets the friends/haters of a specific user
        from the behaviour patterns found without providing a right sentiment 
        to plot (positive, neutral, negative)."""
    with pytest.raises(InvalidSentiment):
        assert da.get_haters_or_friends([], "Sentiment")

def test3_get_haters_or_friends():
    """Test to check the method which gets the friends/haters of a specific user
        from the behaviour patterns found without providing these data."""
    with pytest.raises(BehaviourAnalysisNotFound):
        assert da.get_haters_or_friends([], 'pos')

def test4_get_haters_or_friends():
    """Test to check the method which gets the friends/haters of a specific user
        from the behaviour patterns found without providing the right data."""
    behaviour_patterns_invalid_data = [1, 2, 3]
    with pytest.raises(BehaviourAnalysisNotFound):
        assert da.get_haters_or_friends(behaviour_patterns_invalid_data, 'pos')
    
def test5_get_haters_or_friends():
    """Test to check the method which gets the friends/haters of a specific user
        from the behaviour patterns found without providing the right data."""
    behaviour_patterns_invalid_data = [{'u1':2, 'u2':50}]
    with pytest.raises(BehaviourAnalysisNotFound):
        assert da.get_haters_or_friends(behaviour_patterns_invalid_data, 'pos')

def test6_get_haters_or_friends():
    """Test to check the method which gets the friends/haters of a specific user
        from the behaviour patterns found without providing the right data."""
    behaviour_patterns_invalid_data = [{'u1':{'pos':2, 'neu':"", 'neg':20}}]
    with pytest.raises(SentimentAnalysisNotFound):
        assert da.get_haters_or_friends(behaviour_patterns_invalid_data, "pos")

def test7_get_haters_or_friends():
    """Test to check the method which gets the friends/haters of a specific user
        from the behaviour patterns found without providing the right data."""
    behaviour_patterns_invalid_data = [{'u1':{'user':2}}]
    with pytest.raises(SentimentAnalysisNotFound):
        assert da.get_haters_or_friends(behaviour_patterns_invalid_data, 'pos')
        
def test8_get_haters_or_friends():
    """Test to get the users who wrote positive comments or friends to posts of 
        a specific user. It will plot maximum 10 haters on a bar graphic."""
    data = [{'u1': {'pos': (10, 0.85), 'neu': (3, 0.66), 'neg': (4, 0.25)}}, 
      {'u2': {'pos': (5, 0.753), 'neu': (4, 0.30), 'neg': (2, 0.55)}}, 
      {'u5': {'pos': (8, 0.948), 'neu': (5, 0.45), 'neg': (3, 0.69)}}]
    plot_friends = da.get_haters_or_friends(data, "pos")
    assert plot_friends == True

def test9_get_haters_or_friends():
    """Test to get the users who wrote negative comments or haters to posts of 
        a specific user. It will plot maximum 10 haters on a bar graphic."""
    data = [{'u1': {'pos': (10, 0.85), 'neu': (3, 0.66), 'neg': (4, 0.25)}}, 
      {'u2': {'pos': (5, 0.753), 'neu': (4, 0.30), 'neg': (2, 0.55)}}, 
      {'u5': {'pos': (8, 0.948), 'neu': (5, 0.45), 'neg': (3, 0.69)}}]
    plot_haters = da.get_haters_or_friends(data, "neg")
    assert plot_haters == True