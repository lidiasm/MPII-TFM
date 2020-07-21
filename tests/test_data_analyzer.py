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
    , ProfilesListNotFound, UsernameNotFound, InvalidPreferences, InvalidUsername \
    , InvalidRangeOfDates, PostsListNotFound, ContactsListsNotFound
    
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
    file_name = da.test_plots+"test_pie_plot"
    assert da.pie_plot(values, labels, title, file_name, colors) == True

def test5_pie_plot():
    """Test to draw a pie plot and save it to a PNG file."""
    values = [10, 5, 2]
    labels = ['positive', 'neutral', 'negative']
    title = "Test pie plot"
    file_name = da.test_plots+"test_pie_plot_2"
    assert da.pie_plot(values, labels, title, file_name) == True

def test1_bar_plot():
    """Test to check the method which draws bar plots without providing any data.
        It will raise an exception."""
    with pytest.raises(InvalidPlotData):
        assert da.bar_plot(None, None, None, None, None)

def test2_bar_plot():
    """Test to check the method which draws bar plots without providing the Y labels,
        plot title and file name. It will raise an exception."""
    values = [5, 2, 15, 8, 9]
    x_labels = ['user1', 'user3', 'user5', 'user2', 'user10']
    with pytest.raises(InvalidPlotData):
        assert da.bar_plot(values, x_labels, None, None, None)
        
def test3_bar_plot():
    """Test to check the method which draws a bar plot using the provided data,
        X and Y labels, the plot title as well as the file name and the path in which the image
        will be stored."""
    values = [5, 2, 15, 8, 9]
    x_labels = ['user1', 'user3', 'user5', 'user2', 'user10']
    result = da.bar_plot(values, x_labels, "Test values", "Test bar plot", da.test_plots+"test_bar_plot")
    assert result == True

def test1_lines_plot():
    """Test to check the method which draws line plot without providing valid data.
        It will raise an exception."""
    with pytest.raises(InvalidPlotData):
        assert da.lines_plot([1,2,3,4], None, None, None, None, None)

def test2_lines_plot():
    """Test to check the method which draws line plot without providing the legend 
        and the X labels. It will raise an exception."""
    values = [[1,5,4], [3,6,9], [7,2,0]]
    with pytest.raises(InvalidPlotData):
        assert da.lines_plot(values, None, None, None, None, None)
        
def test3_lines_plot():
    """Test to check the method which draws line plot without providing the Y label,
        the plot title and the file name. It will raise an exception."""
    values = [[1,5,4], [3,6,9], [7,2,0]]
    legend_labels = ["line 1", "line 2", "line 3"]
    x_labels = ["26/07", "27/07", "29/07"]
    with pytest.raises(InvalidPlotData):
        assert da.lines_plot(values, legend_labels, x_labels, None, 123, None)
    
def test4_lines_plot():
    """Test to check the method which draws a line plot using the provided data,
        X and Y labels, the plot title as well as the file name and the path in which the image
        will be stored."""
    values = [[1,5,4], [3,6,9], [7,2,0]]
    legend_labels = ["line 1", "line 2", "line 3"]
    x_labels = ["26/07", "27/07", "29/07"]
    result = da.lines_plot(values, legend_labels, x_labels, "Test values", "Test lines plot", da.test_plots+"test_lines_plot")
    assert result == True

def test1_table_plot():
    """Test to check the method which plots a table without providing valid data.
        It will raise an exception."""
    with pytest.raises(InvalidPlotData):
        assert da.table_plot(None, None, None, None)
        
def test2_table_plot():
    """Test to check the method which plots a table without providing valid columns.
        It will raise an exception."""
    values = [[1,2,3], [4,5,6]]
    with pytest.raises(InvalidPlotData):
        assert da.table_plot(values, None, None, None)
        
def test3_table_plot():
    """Test to check the method which plots a table without providing the same number
        of values and columns.
        It will raise an exception."""
    values = [[1,2,3], [4,5,6]]
    with pytest.raises(InvalidPlotData):
        assert da.table_plot(values, ['Col1', 'Col2', 'Col3'], None, None)
        
def test4_table_plot():
    """Test to check the method which plots a table without providing valid colours.
        It will raise an exception."""
    values = [[1,2,3], [4,5,6]]
    columns = ["Col1", "Col2"]
    with pytest.raises(InvalidPlotData):
        assert da.table_plot(values, columns, None, None)

def test5_table_plot():
    """Test to check the method which plots a table without providing the same number
        of values, columns and colours. An exception will be raised."""
    values = [[1,2,3], [4,5,6]]
    columns = ["Col1", "Col2"]
    colours = ["red", "yellow", "green"]
    with pytest.raises(InvalidPlotData):
        assert da.table_plot(values, columns, colours, None)
        
def test6_table_plot():
    """Test to check the method which plots a table without providing a valid file name.
        It will raise an exception."""
    values = [[1,2,3], [4,5,6]]
    columns = ["Col1", "Col2"]
    colours = ["red", "yellow"]
    with pytest.raises(InvalidPlotData):
        assert da.table_plot(values, columns, colours, None)
        
def test7_table_plot():
    """Test to plot a table using the provided data such as the values, the column
        names and the colours for each one of them as well as the file name and the
        path in which the image will be stored."""
    values = [['u1', 'u2', 'u3', 'u6', 'u7', 'u10', 'u55', 'u53', 'u9', 'u0', 'u22', 'u222', 'u4'], ['u4', 'u5']]
    columns = ["Col1", "Col2"]
    colours = ["red", "yellow"]
    assert da.table_plot(values, columns, colours, da.test_plots+"test_table_plot") == True
        
def test1_profile_evolution():
    """Test to check the method which gets the evolution of some fields from
        a user profile such us the number of followers, followings and medias.
        In this case there are not data provided so it will raise an exception."""
    with pytest.raises(ProfilesListNotFound):
        assert da.profile_evolution([])

def test2_profile_evolution():
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
    
def test3_profile_evolution():
    """Test to get the evolution of some fields from a user profile drawing them
        in bar plots."""
    profile1 = {"username" : "lidia.96.sm", "n_followings":120, "n_followers" : 122,
                "n_medias":30, "date" : "27-06-2020"}
    profile2 = {"username" : "isa", "n_followings":115, "n_followers" : 89,
                "n_medias":28, "date" : "26-06-2020"}
    with pytest.raises(InvalidUsername):
        da.profile_evolution([profile1, profile2])
        
def test1_sort_and_plot_posts():
    """Test to check the method which plots the favs/non-favs posts sorted by
        comments or likes without providing the username of the user who owns the
        posts. An exception will be raised."""
    with pytest.raises(UsernameNotFound):
          assert da.sort_and_plot_posts("", None, None, None)
         
def test2_sort_and_plot_posts():
    """Test to check the method which plots the favs/non-favs posts sorted by
        comments or likes without providing a valid field to sort the posts (likes/comments).
        An exception will be raised."""
    with pytest.raises(InvalidPreferences):
          assert da.sort_and_plot_posts("lidia.96.sm", None, None, None)
    
def test3_sort_and_plot_posts():
    """Test to check the method which plots the favs/non-favs posts sorted by
        comments or likes without providing a valid way to sort the posts 
        (favs=descending order/non-favs=ascending order). An exception will be raised."""
    with pytest.raises(InvalidPreferences):
        assert da.sort_and_plot_posts("lidia.96.sm", 'likes', 1234, None)

def test4_sort_and_plot_posts():
    """Test to get the favs posts sorted by likes of a specific user."""
    posts = [ { "id_post" : "1", "likes" : 29, "comments" : 14 }, 
              { "id_post" : "2", "likes" : 45, "comments" : 50 },
              { "id_post" : "3", "likes" : 120, "comments" : 250 },
              { "id_post" : "4", "likes" : 135, "comments" : 360 },
              { "id_post" : "5", "likes" : 115, "comments" : 69 },
              { "id_post" : "6", "likes" : 78, "comments" : 95 },
              { "id_post" : "7", "likes" : 112, "comments" : 34 },]
    result = da.sort_and_plot_posts("lidia.96.sm", 'likes', True, posts)
    assert result == True
    
def test5_sort_and_plot_posts():
    """Test to get the non-favs posts sorted by comments of a specific user."""
    posts = [ { "id_post" : "1", "likes" : 29, "comments" : 14 }, 
              { "id_post" : "2", "likes" : 45, "comments" : 50 },
              { "id_post" : "3", "likes" : 120, "comments" : 250 },
              { "id_post" : "4", "likes" : 135, "comments" : 360 },
              { "id_post" : "5", "likes" : 115, "comments" : 69 },
              { "id_post" : "6", "likes" : 78, "comments" : 95 },
              { "id_post" : "7", "likes" : 112, "comments" : 34 },]
    result = da.sort_and_plot_posts("lidia.96.sm", 'comments', False, posts)
    assert result == True

def test1_followers_activity():
    with pytest.raises(UsernameNotFound):
          assert da.followers_activity("", None, None, None, None, None, None)
          
def test2_followers_activity():
    likers = [('user1', 20), ('user2', 17), ('user3', 30), ('user4', 9), ('user5', 13)]
    comments = [ { "id_post" : "1", "comments" : [ 
                    { "user" : "user1", "comment" : "aa" },
                    { "user" : "user2", "comment" : "ee" } ] }, 
                { "id_post" : "2", "comments" : [ 
                    { "user" : "user3", "comment" : "ii" },
                    { "user" : "user2", "comment" : "oo" } ] } ]
    followers = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7']
    with pytest.raises(InvalidPreferences):
          assert da.followers_activity("lidia.96.sm", likers, comments, followers, None, None, None)

def test3_followers_activity():
    likers = [('user1', 20), ('user2', 17), ('user3', 30), ('user4', 9), ('user5', 13)]
    comments = [ { "id_post" : "1", "comments" : [ 
                    { "user" : "user1", "comment" : "aa" },
                    { "user" : "user2", "comment" : "ee" } ] }, 
                { "id_post" : "2", "comments" : [ 
                    { "user" : "user3", "comment" : "ii" },
                    { "user" : "user2", "comment" : "oo" } ] } ]
    followers = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7']
    with pytest.raises(InvalidPreferences):
          assert da.followers_activity("lidia.96.sm", likers, comments, followers, "likes", 1234, None)
        
def test4_followers_activity():
    likers = [('user1', 20), ('user2', 17), ('user3', 30), ('user4', 9), ('user5', 13)]
    comments = [ { "id_post" : "1", "comments" : [ 
                    { "user" : "user1", "comment" : "aa" },
                    { "user" : "user2", "comment" : "ee" } ] }, 
                { "id_post" : "2", "comments" : [ 
                    { "user" : "user3", "comment" : "ii" },
                    { "user" : "user2", "comment" : "oo" } ] } ]
    followers = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8', 'user9',
                 'user10', 'user11', 'user12', 'user13', 'user14', 'user15']
    result = da.followers_activity("lidia.96.sm", likers, comments, followers, "likes", True, False)
    assert result[0] == True and result[1] == False
        
def test5_followers_activity():
    likers = [('user1', 20), ('user2', 17), ('user3', 30), ('user4', 9), ('user5', 13),
              ('user100', 15), ('user99', 19), ('user98', 23), ('user97', 5), ('user96', 7)]
    comments = [ { "id_post" : "1", "comments" : [ 
                    { "user" : "user1", "comment" : "aa" },
                    { "user" : "user2", "comment" : "ee" } ] }, 
                { "id_post" : "2", "comments" : [ 
                    { "user" : "user3", "comment" : "ii" },
                    { "user" : "user2", "comment" : "oo" } ] } ]
    followers = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8', 'user9',
                 'user10', 'user11', 'user12', 'user13', 'user14', 'user15']
    result = da.followers_activity("lidia.96.sm", likers, comments, followers, "comments", False, True)
    assert all(item==True for item in result) == True
    
def test1_posts_evolution():
    """Test to check the method which performs a posts evolution without providing
        the username of the user who owns them. An exception will be raised."""
    with pytest.raises(UsernameNotFound):
        assert da.posts_evolution("", None, None)
        
def test2_posts_evolution():
    """Test to check the method which performs a posts evolution without providing
        the list of dates in which the posts were downloaded. An exception will be raised."""
    with pytest.raises(InvalidRangeOfDates):
        assert da.posts_evolution("lidia.96.sm", None, None)
        
def test3_posts_evolution():
    """Test to check the method which performs a posts evolution without providing
        the list of dates in which the posts were downloaded. An exception will be raised."""
    with pytest.raises(InvalidRangeOfDates):
        assert da.posts_evolution("lidia.96.sm", ["27/07/2020", 123456], None)
        
def test4_posts_evolution():
    """Test to check the method which performs a posts evolution without providing
        the list of posts. An exception will be raised."""
    with pytest.raises(PostsListNotFound):
        assert da.posts_evolution("lidia.96.sm", ["27/07/2020", "29/07/2020", "30/07/2020"], None)

def test5_posts_evolution():
    """Test to performs a posts evolution in order to draw the analysis in a
        bar plot drawing the evolution of likes and comments in a specific range 
        of dates."""
    posts1 = [ { "id_post" : "1", "likes" : 29, "comments" : 14 }, { "id_post" : "2", "likes" : 18, "comments" : 0 } ]
    posts2 = [ { "id_post" : "1", "likes" : 50, "comments" : 34 }, { "id_post" : "2", "likes" : 24, "comments" : 10 } ]
    posts3 = [ { "id_post" : "1", "likes" : 71, "comments" : 39 }, { "id_post" : "2", "likes" : 59, "comments" : 29 } ]
    posts_list = [posts1, posts2, posts3]
    result = da.posts_evolution("lidia.96.sm", ["27/07/2020", "29/07/2020", "30/07/2020"], posts_list)
    assert result == True
    
def test1_contacts_activity():
    """Test to check the method which gets the new followers, followings as well
        as the old-new followers and followings without providing any data. 
        An exception will be raised."""
    with pytest.raises(ContactsListsNotFound):
        assert da.contacts_activity(None, None, None)

def test2_contacts_activity():
    """Test to check the method which gets the new followers, followings as well
        as the old-new followers and followings only providing the list of followers.
        An exception will be raised."""
    followers_list = [["user1", "user2", "user3"], ["user1", "user2", "user4", "user5"]]
    with pytest.raises(ContactsListsNotFound):
        assert da.contacts_activity(followers_list, [1,2,3,4], None)
        
def test3_contacts_activity():
    """Test to check the method which gets the new followers, followings as well
        as the old-new followers and followings only providing the list of followers and followings.
        An exception will be raised."""
    followers_list = [["user1", "user2", "user3"], 
                      ["user1", "user2", "user4", "user5"]]
    followings_list = [["user1", "user2", "user3"], 
                        ["user1", "user2", "user3", "user4", "user5"]]
    with pytest.raises(UsernameNotFound):
        assert da.contacts_activity(followers_list, followings_list, None)

def test4_contacts_activity():
    followers_list = [["user1", "user2", "user3"], 
                      ["user1", "user2", "user4", "user5", "user8", "user9", "user25"],
                      ["user3", "user4", "user5", "user6", "user11", "user9", "user54", "user96"],
                      ["user3", "user4", "user5", "user6", "user8", "user9", "user10", "user21"]]
    followings_list = [["user1", "user2", "user3"], 
                        ["user1", "user2", "user4", "user5", "user54", "user8", "user9"],
                        ["user2", "user3", "user4", "user5", "user6", "user7", "user8"]]
    assert da.contacts_activity(followers_list, followings_list, "lidia.96.sm") == True
        
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