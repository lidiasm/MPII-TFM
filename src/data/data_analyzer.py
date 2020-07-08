#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains all methods used to analyze media social data from a specific user.
These methods are:
    - Feelings analyzer for post comments in order to get if they're positive, neutral
        or negative as wella as the confidence degree of the sentiment.

@author: Lidia Sánchez Mérida
"""
import os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
# Sentiment Analysis Library
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from exceptions import CommentsListNotFound, CommentsDictNotFound \
    , SentimentAnalysisNotFound, BehaviourAnalysisNotFound, InvalidSentiment \
    , ProfilesListNotFound, ProfileDictNotFound, UsernameNotFound, InvalidBarPlotData \
    , InvalidBarPlotColors

class DataAnalyzer:
    
    def __init__(self):
        """Constructor. Attributes:
            - The maximum number of users to plot in the method with gets the friends/heaters method.
            - The sentiments to analyze friends/haters users based in their comments.
            - The general path and the specific paths in which the plots will be saved."""
        self.max_n_users = 10
        self.sentiments = ["pos", "neg"]
        self.common_plots_path = "./images/"
        self.profev_path = "profiles evolutions/"
        self.behaviours_path = "behaviour patterns/"
    
    def bar_plot(self, values, x_labels, y_label, plot_title, file_title, colors):
        """Method which draws a bar plot providing the positions of the elements,
            their values, the labels of the X axis and the color(s) of each bar."""
        # Check the provided data
        if (type(values) != list or type(x_labels) != list
            or len(values) == 0 or len(x_labels) == 0):
            raise InvalidBarPlotData("ERROR. Values and x_labels should be non emtpy list.")
        # Values and x_labels should have the same lenght to be plotted
        if (len(values) != len(x_labels)):
            raise InvalidBarPlotData("ERROR. Values and x_labels should have the same lenght.")
        # Check strings like y_label, plot_title and file_title
        if (type(y_label) != str or type(plot_title) != str or type(file_title) != str or
            file_title == ""):
            raise InvalidBarPlotData("ERROR. The y_label, plot and file title should be non empty strings.")
        
        # Check colors type
        if (type(colors) != str and type(colors) != list):
            raise InvalidBarPlotColors("ERROR. One color should be a non empty strings. Many colors should be in a non emtpy list.")
        
        """New bar plot"""
        plt.figure(figsize=(8, 8))
        positions = np.arange(len(values))
        if (type(colors) == str and colors != ""):
            bars = plt.bar(positions, values, align='center', alpha=0.5, color=colors)
        
        if (type(colors) == list and len(colors) > 0):
            bars = plt.bar(positions, values, align='center', alpha=0.5)
            for i in range(0, len(colors)):
                bars[i].set_color(colors[i])
        
        plt.xticks(positions, x_labels, rotation='45')
        plt.ylabel(y_label)
        plt.title(plot_title)
        now = datetime.now()
        current_time = now.strftime("%d_%m_%Y_%H_%M_%S")
        file_title = self.common_plots_path+file_title+"_"+current_time+".png"
        plt.savefig(file_title)
        
        return os.path.isfile(file_title)
        
    def profile_evolution(self, profiles):
        """Method that analyzes the number of posts, followings and followers of
            the profile of a specific user during a certain period. 
            In order to do that, the provided data should be a list of many profiles of the same
            user from a social media but from different dates.
            
            Three plots will drawed in order to represent the evolutions of the 
                number of followings, followers and posts.
        """
        # Check the list of profiles
        if (type(profiles) != list or len(profiles) < 2):
            raise ProfilesListNotFound("ERROR. A non empty list of profiles should be provided.")
            
        # Check the profiles from the same user
        for prof in profiles:
            if (type(prof) != dict or len(prof) == 0):
                raise ProfileDictNotFound("ERROR. A user profile should be a non empty dict.")
            if ('username' not in prof or 'date' not in prof or 'n_followers'not in prof 
                or 'n_followings' not in prof or 'n_medias' not in prof):
                raise ProfileDictNotFound("ERROR. The profile should have a username, date, number of "+
                      "followers, followings and posts.")
        
        """Sort the profiles by the date."""
        sorted_profiles = sorted(profiles, key = lambda i: i['date'])
        dates = [prof['date'] for prof in sorted_profiles]
        n_followers = [prof['n_followers'] for prof in sorted_profiles]
        n_followings = [prof['n_followings'] for prof in sorted_profiles]
        n_medias = [prof['n_medias'] for prof in sorted_profiles]
        users = [prof['username'] for prof in sorted_profiles]
        
        if ( len(set(users)) > 1 ):
            raise UsernameNotFound("ERROR. All profiles should be from the same user.")
            
        """Plot three graphs for followers, followings and posts evolution."""
        plot_followers = self.bar_plot(n_followers, dates, "Number of followers", "Followers Evolution of user "+profiles[0]['username'],
              self.profev_path+"followers_ev_"+profiles[0]['username'], "blue")
        plot_followings = self.bar_plot(n_followings, dates, "Number of followings", "Followings Evolution of user "+profiles[0]['username'],
              self.profev_path+"followings_ev_"+profiles[0]['username'], "cyan")
        plot_medias = self.bar_plot(n_medias, dates, "Number of posts", "Posts Evolution of user "+profiles[0]['username'],
              self.profev_path+"posts_ev_"+profiles[0]['username'], "magenta")
        
        return plot_followers and plot_followings and plot_medias
    
    def comments_sentiment_analyzer(self, data):
        """Method that analyzes the feelings of the post comments of a specific user
            in order to get the sentiment and its confidence degree. Both fields will
            be added to the original data so each comment has its sentiment and confidence degree."""
        # Check the list of comments
        if (type(data) != list or len(data) == 0):
            raise CommentsListNotFound("ERROR. The comments to analyze should be a non empty list.")
        # Check each comment (user, preproc_comment)
        sent_analyzer = SentimentIntensityAnalyzer()
        for record in data:
            if ('user' not in record or 'preproc_comment' not in record):
                raise CommentsDictNotFound("ERROR. Each comment should be a dict like {'user':'username', 'preproc_comment:'text'}")
        
            """Sentiment Analysis for each comment using NLTK VADER library."""
            analysis = sent_analyzer.polarity_scores(record['preproc_comment'])
            # Delete the compound element
            del analysis['compound']
            sentiment = max(analysis, key=analysis.get)
            """Add the sentiment and the polarity score to the original data."""
            record['sentiment'] = sentiment
            record['polarity'] = analysis[sentiment]
        
        return data
    
    def behaviour_patterns(self, sentiment_analysis):
        """Method which counts the number of positive, neutral and negative comments
            of each user from the sentiment analysis of a user's posts.
            
            Returns a list of each user with the number of positive, negative and neutral comments
            as well as the mean confidence degree (1%).
        """
        # Check the list of comments
        if (type(sentiment_analysis) != list or len(sentiment_analysis) == 0):
            raise SentimentAnalysisNotFound("ERROR. The sentiment analysis should be a non empty list.")
        # Check each analyzed comment (user, preproc_comment, sentiment, confidence)
        list_users = []
        shown_users = []
        for record in sentiment_analysis:
            if ('user' not in record or 'preproc_comment' not in record or
                'sentiment' not in record or 'polarity' not in record):
                raise CommentsDictNotFound("ERROR. Each record should be a dict like "+
                   "{'user':'username', 'preproc_comment:'text', 'sentiment':'sentiment', 'polarity':polarity score'}")
            
            """Initialize the list of the users with the number of positive, neutral and
                 negative comments and the confidence degree to 0 without duplicates."""
            if (record['user'] not in shown_users):
                 shown_users.append(record['user'])
                 list_users.append({record['user']:{'pos':(0,0), 'neu':(0,0), 'neg':(0,0)}})
        
        for record_d in sentiment_analysis:
            user_d = record_d['user']
            """For each user, the number of positive, neutral and negative comments are counted
                along with their confidence degree."""
            for record_l in list_users:
                for user_l in record_l:
                    if (user_d == user_l):
                        sent = record_d['sentiment']
                        conf = record_d['polarity']
                        record_l[user_l][sent] = (record_l[user_l][sent][0]+1, record_l[user_l][sent][1]+conf)
            
        """Normalize the confidence degree dividing the value by the number of comments
            of each user for each sentiment if they're greater than 0."""
        for record in list_users:
            for user in record:
                if (record[user][sent][0] > 0 and record[user][sent][1] > 0):
                    record[user][sent] = (record[user][sent][0], round(record[user][sent][1]/record[user][sent][0]), 3)
            
        return list_users
    
    def get_general_behaviour(self, sentiment_analysis):
        """Method which plots the number of positive, neutral and negative comments
            of a specific set of comments with their means of the confidence degrees in
            order to represent how those sentiments are. That's why the provided data should
            be a sentiment analysis."""
        # Check the list of comments
        if (type(sentiment_analysis) != list or len(sentiment_analysis) == 0):
            raise SentimentAnalysisNotFound("ERROR. The sentiment analysis should be a non empty list.")
        
        general_analysis = {'pos':(0,0), 'neu':(0,0), 'neg':(0,0)}
        # Check each analyzed comment (user, preproc_comment, sentiment, confidence)
        for record in sentiment_analysis:
            if ('user' not in record or 'preproc_comment' not in record or
                'sentiment' not in record or 'polarity' not in record):
                raise CommentsDictNotFound("ERROR. Each record should be a dict like "+
                   "{'user':'username', 'preproc_comment:'text', 'sentiment':'sentiment', 'polarity':polarity score'}")
            
            """Compute the number of comments for each sentiment and their confidence degree."""
            general_analysis[record['sentiment']] = (general_analysis[record['sentiment']][0] + 1,
                                                     general_analysis[record['sentiment']][1] + record['polarity'])
        
        """Normalize the confidence degree (1%)"""
        if (general_analysis['pos'][1] > 0):
            general_analysis['pos'] = (general_analysis['pos'][0], round(general_analysis['pos'][1]/general_analysis['pos'][0], 3))
        if (general_analysis['neu'][1] > 0):
            general_analysis['neu'] = (general_analysis['neu'][0], round(general_analysis['neu'][1]/general_analysis['neu'][0], 3))
        if (general_analysis['neg'][1] > 0):
            general_analysis['neg'] = (general_analysis['neg'][0], round(general_analysis['neg'][1]/general_analysis['neg'][0], 3))
        
        """Order the results and plot them."""
        order_ga = dict(sorted(general_analysis.items(), key=lambda x: x[1], reverse=True))
        x_labels = ["positive\n"+str(round(order_ga['pos'][1]*100,3))+"%", "neutral\n"+str(round(order_ga['neu'][1]*100,3))+"%",
                    "negative\n"+str(round(order_ga['neg'][1]*100,3))+"%"]
        values = [order_ga['pos'][0], order_ga['neu'][0], order_ga['neg'][0]]
        
        return (self.bar_plot(values, x_labels, "Number of comments", "General Behaviour Patterns",
                      self.behaviours_path+"general_behaviour", ['green', 'yellow', 'red']))
        
    def get_haters_or_friends(self, behaviour_data, sentiment):
        """Method which plots the users who wrote positive/negative comments in the
            post of a specific user ordered by the mean of confidence degrees of each
            sentiment relative to a comment. 
            
            In order to do that, the provided data should be the data returned by the
            method 'behaviour_patterns'.
        """
        # Check the choosen sentiment
        if (type(sentiment) != str or sentiment == ""):
            raise InvalidSentiment("ERROR. The sentiment to plot should be a non empty string.")
        
        if (sentiment.lower() not in self.sentiments):
            raise InvalidSentiment("ERROR. The sentiment should be: positive or negative.")
            
        # Check the provided data
        if (type(behaviour_data) != list or len(behaviour_data) == 0):
            raise BehaviourAnalysisNotFound("ERROR. The behaviour patterns should be a non empty list.")
        
        user_analysis = []
        for record in behaviour_data:
            if (type(record) != dict or len(record) == 0):
                raise BehaviourAnalysisNotFound("ERROR. The behaviour patterns data should be a non-empty list of dicts.")
            for user in record:
                if (type(record[user]) != dict or len(record[user]) == 0):
                    raise BehaviourAnalysisNotFound("ERROR. The behaviour patterns data should be a non-empty list of dicts.")
                
                if ('pos' not in record[user] or 'neg' not in record[user]):
                    raise SentimentAnalysisNotFound("ERROR. Sentiments 'pos' and" 
                        + " 'neg' should be in each user record.")
                    
                if (type(record[user]['pos']) != tuple or type(record[user]['neg']) != tuple):
                    raise SentimentAnalysisNotFound("ERROR. Each sentiment should have the number"
                       + " of comments and the polarity score.")
                
                """Each user has the number of comments of the specific sentiment and the mean
                    of the confidence degrees."""
                user_analysis.append({'user':user, 'n_comments':record[user][sentiment][0], 'mean_pol':record[user][sentiment][1]})
                    
        """Order the users by their mean confidence degree of the choosen sentiment."""
        sorted_user_analysis = sorted(user_analysis, key = lambda i: (i['n_comments'],i['mean_pol']), reverse=True)
 
        """Plot the analysis results."""
        x_labels = []
        for record in sorted_user_analysis:
            x_labels.append(record['user'] + "\n" + str(round(record['mean_pol']*100,3)) + " %")
            
        values = [record['n_comments'] for record in sorted_user_analysis]
        color = "red"
        if (sentiment == 'pos'): color="green"
        
        return (self.bar_plot(values, x_labels, "Number of comments", "Plot "+sentiment+" comments",
                      self.behaviours_path+sentiment+"_comments", color))
