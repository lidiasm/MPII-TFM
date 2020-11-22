#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains all methods used to analyze media social data from a specific user.
These methods are:
    - Analysis of some data related to the profile, such as the number of followers
    and followings as well as the number of uploaded posts in a specific period of time.
    The main goal is plotting the evolution of the contacts and the activity of the user.

@author: Lidia Sánchez Mérida
"""
import os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
# Style like R plots
plt.style.use('ggplot')
# Sentiment Analysis Library
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from exceptions import ValuesNotFound, KeysNotFound, ExpectedSameSize \
    , InvalidLinePlotData, ProfilesNotFound, UsernameNotFound, TextTupleNotFound \
    , InvalidBarPlotData, UserActivityNotFound, PostInteractionsNotFound \
    , PostPopularityNotFound, InvalidPiePlotData, TextDataDictNotFound, SentimentTupleNotFound

class DataAnalyzer:
    
    def __init__(self):
        """
        Creates a DataAnalyzer object whose attributes are:
            - The list of avalaible social media sources
            - The list of colours to draw the plots.
            - The default path to store the differents plots.
            - The list of avalaible analysis.

        Returns
        -------
        A DataAnalyzer object.
        """
        self.social_media_sources = ["instagram"]
        self.colors_line_plots = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        self.plot_tests_path = "./imgs/tests/"
        self.profile_evolution_path = "./imgs/profiles-evolution/"
        self.user_activity_path = "./imgs/user-activity/"
        self.post_evolution_path = "./imgs/posts-evolution/"
        self.text_sentiments_path = "./imgs/text-sentiments/"
        self.user_behaviours_path = "./imgs/user-behaviours/"
        # List of avalaible analysis
        self.avalaible_analysis = [
           "profile_evolution", "profile_activity",
           "media_evolution", "media_popularity", 
           "comment_sentiment_analysis", "title_sentiment_analysis", "users_behaviours",
           
           "test_profile_evolution", "test_profile_activity",
           "test_media_evolution", "test_media_popularity",
           "test_comment_sentiment_analysis", "test_title_sentiment_analysis", "test_users_behaviours"]
    
    def get_values_per_one_week(self, values, keys):
        """
        Gets the provided values and links them with their related category 
        depending on the position creating a list of values per one week. 
        That's why the length of each record must be the same than the number of keys.

        Parameters
        ----------
        values : list of tuples
            It's the list of data to link with their related class.
        keys : list of strings
            It's the list of keys which are related to each position in the records.

        Raises
        ------
        ValuesNotFound
            If the provided values are not a non-empty list of tuples.
        KeysNotFound
            If the provided keys are not a non-empty list of strings.
        ExpectedSameSize
            If the provided records of the list of values have not the same size
            than the number of keys.

        Returns
        -------
        A dict whose keys are the provided categories and whose values are the 
        list of the related values to each key.
        """
        # Check the provided list of values
        if (type(values) != list or len(values) == 0 or
            not (all(isinstance(item, tuple) for item in values))):
            raise ValuesNotFound("ERROR. The values should be a list of tuples.")
        # Check the provided list of keys
        if (type(keys) != list or len(keys) == 0 or
            not (all(isinstance(item, str) for item in keys))):
            raise KeysNotFound("ERROR. The keys should be a list of strings.")

        # Initialize the dict with the provided keys and an empty list as values
        result = {key:[] for key in keys}
        # Get from the records each data into their category
        for record in values:
            # Check there is the same number of values and key
            if (len(record) != len(keys)):
                raise ExpectedSameSize("ERROR. The number of values and keys should be the same.")
            for i in range(0, len(keys)):
                result[keys[i]].append(record[i])
        
        return result
    
    def get_values_per_many_weeks(self, values, keys):
        """Gets the provided values and links them with their related category 
        depending on the position creating a mean list per more than a week. 
        That's why the length of each record must be the same than the number 
        of keys.

        Parameters
        ----------
        values : list of tuples
            It's the list of data to link with their related class.
        keys : list of strings
            It's the list of keys which are related to each position in the records.

        Raises
        ------
        ValuesNotFound
            If the provided values are not a non-empty list of tuples.
        KeysNotFound
            If the provided keys are not a non-empty list of strings.
        ExpectedSameSize
            If the provided records of the list of values have not the same size
            than the number of keys.

        Returns
        -------
        A dict whose keys are the provided categories and whose values are the 
        list of the related values to each key.
        """
        # Check the provided list of values
        if (type(values) != list or len(values) == 0 or
            not (all(isinstance(item, tuple) for item in values))):
            raise ValuesNotFound("ERROR. The values should be a list of tuples.")
        # Check the provided list of keys
        if (type(keys) != list or len(keys) == 0 or
            not (all(isinstance(item, str) for item in keys))):
            raise KeysNotFound("ERROR. The keys should be a list of strings.")

        # Get the values per week
        value_list = self.get_values_per_one_week(values, keys)
        # Initialize the final dict to store the average per key
        result = {key:[] for key in keys}
        for i in range(1, len(list(value_list.keys()))):
            # Get the values for each key
            key_values = value_list[keys[i]]
            # Transform the values from string to int
            key_values = [int(i) for i in key_values]
            while (len(key_values) > 0):
                # Compute the average
                result[keys[i]].append(round(sum(key_values[:7])/len(key_values[:7])))
                # Delete the computed numbers
                key_values = key_values[7:]
        
        # Add the weeks depending on the number of averages
        weeks = [str(i+1) + " week(s)" for i in range(0, len(result[keys[1]]))]
        result['date'].extend(weeks)
        
        return result
        
    ########################## PROFILE ANALYSIS ##############################
    def profile_evolution(self, username, profile_list):
        """
        Draws a line plot about the evolution of the number of followers and 
        followings, as well as the number of uploaded posts of a specific
        user in a period of time. The plot will be saved as an image.

        Parameters
        ----------
        username : str
            It's the username who's been studied.
        profile_list : list of tuples
            It's the list of the required values to analyze the profile evolution.
            Each record will have 4 items: (date, n_medias, n_followers, n_followings)

        Raises
        ------
        UsernameNotFound
            If the provided username is not a non-empty string.
        ProfilesNotFound
            If the provided profiles are not a non-empty list of tuples.

        Returns
        -------
        A dict whose keys are:
            - 'state', which indicates if the analysis have been performed and saved
            as an image.
            - 'file', which has the path and the file name in which there is the
            analysis saved.
            - 'data', which returns the analysis results.
        """
        # Check the provided username
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")
        # Check the provided list of profiles
        if (type(profile_list) != list or len(profile_list) == 0):
            raise ProfilesNotFound("ERROR. The profiles to study should be in a non-empty list.")
        # Check that there are four types of values for: date, n_posts, n_followers and n_followings
        for profile in profile_list:
            if (type(profile) != tuple or len(profile) != 4):
                raise ProfilesNotFound("ERROR. The four fields to analyze the profile evolution should be tuples.")
        
        # Get the values per one week
        if (len(profile_list) <= 7):
            username += "_1week"
            result = self.get_values_per_one_week(profile_list, 
                          ['date', 'n_posts', 'n_followers', 'n_followings'])
        # Get the values per more than a week
        else:
            result = self.get_values_per_many_weeks(profile_list, 
                        ['date', 'n_posts', 'n_followers', 'n_followings'])
            username += "_"+str(len(result['date']))+"weeks"
        
        # Set the path and the title of the file
        file_name = self.profile_evolution_path + username
        # Draw the line plot
        plot_result = self.plot_lines_chart([result['n_followers'], result['n_followings'], result['n_posts']],
                 ['Followers', 'Followings', 'Posts'], result['date'], file_name)
        return {'state':plot_result[0], 'file':plot_result[1], 'data':result}
    
    def user_activity(self, username, activity_list):
        """
        Draws a bar plot about the user activity based on the numbers of uploaded
        posts per week or more time. Besides that, above the bars beginning with
        the first, the difference between days or weeks will be showed in order to
        know the number of uploaded posts per days or weeks. In the end, the plot
        will be saved as an image.

        Parameters
        ----------
        username : str
            It's the username of the studied user.
        activity_list : list of tuples
            It's the list of the user activity to plot.

        Raises
        ------
        UsernameNotFound
            If the provided username is not a non-empty string.
        UserActivityNotFound
            If the provided user activity is not a non-empty list of tuples.

        Returns
        -------
        A dict whose keys are:
            - 'state', which indicates if the analysis have been performed and saved
            as an image.
            - 'file', which has the path and the file name in which there is the
            analysis saved.
            - 'data', which returns the analysis results.
        """
        # Check the provided username
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")
        # Check the provided list of user activity
        if (type(activity_list) != list or len(activity_list) == 0):
            raise UserActivityNotFound("ERROR. The user activity should be a non-empty list.")
        # Check that there are four types of values for: date, n_posts, n_followers and n_followings
        for activity in activity_list:
            if (type(activity) != tuple or len(activity) != 2):
                raise UserActivityNotFound("ERROR. The two fields to analyze the user activity should be tuples.")
        
        # Get the values per one week
        if (len(activity_list) <= 7):
            username += "_1week"
            result = self.get_values_per_one_week(activity_list, 
                          ['date', 'n_posts'])
        # Get the values per more than a week
        else:
            result = self.get_values_per_many_weeks(activity_list, 
                        ['date', 'n_posts'])
            username += "_"+str(len(result['date']))+"weeks"
        
        # Compute the differences between the number of posts
        differences = []
        post_list = result['n_posts']
        # Transform the values to int in case they were the original strings
        post_list = [int(value) for value in post_list]
        for i in range(1, len(post_list)):
            differences.append(round(post_list[i] - post_list[i-1]))
            
        # Draw the bar plot
        file_name = self.user_activity_path + username
        plot_result = self.plot_bars_chart(post_list, result['date'], file_name, differences)
        return {'state':plot_result[0], 'file':plot_result[1], 'data':result}
    
    ############################ POSTS ANALYSIS ##############################
    def post_evolution(self, username, post_interactions):
        """
        Draws a line plot about the evolution of the interactions on the posts
        from a specific user. The plot will be saved as an image.

        Parameters
        ----------
        username : str
            It's the username of the studied user.
        post_interactions : list of tuples
            It's the list of post interactions.

        Raises
        ------
        UsernameNotFound
            If the provided username is not a non-empty string.
        PostInteractionsNotFound
            If the provided post interactions are not a non-empty list of tuples.

        Returns
        -------
        A dict whose keys are:
            - 'state', which indicates if the analysis have been performed and saved
            as an image.
            - 'file', which has the path and the file name in which there is the
            analysis saved.
            - 'data', which returns the analysis results.
        """
        # Check the provided username
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")
        # Check the provided list of posts
        if (type(post_interactions) != list or len(post_interactions) == 0):
            raise PostInteractionsNotFound("ERROR. The posts should be in a non-empty list.")
        # Check that there are four types of values for: date, n_posts, n_followers and n_followings
        for interaction in post_interactions:
            if (type(interaction) != tuple or len(interaction) != 3):
                raise PostInteractionsNotFound("ERROR. The four fields to analyze the profile evolution should be tuples.")
        
        # Compute the mean of likes and comments for each post
        mean_post_interactions = []
        # Get the dates without duplicates
        dates = list(set([item[0] for item in post_interactions]))
        dates.sort()
        for date in dates:
            likes = [int(item[1]) for item in post_interactions if item[0] == date]
            comments = [int(item[2]) for item in post_interactions if item[0] == date]
            mean_post_interactions.append((date, sum(likes)/len(likes), sum(comments)/len(comments)))
                
        # Get the values per one week
        if (len(mean_post_interactions) <= 7):
            username += "_1week"
            result = self.get_values_per_one_week(mean_post_interactions, 
                          ['date', 'like_count', 'comment_count'])
        # Get the values per more than a week
        else:
            result = self.get_values_per_many_weeks(mean_post_interactions, 
                        ['date', 'like_count', 'comment_count'])
            username += "_"+str(len(result['date']))+"weeks"
        
        # Set the path and the title of the file
        file_name = self.post_evolution_path + username
        # Draw the line plot
        plot_result = self.plot_lines_chart([result['like_count'], result['comment_count']],
                 ['Like count', 'Comment count'], result['date'], file_name)
        return {'state':plot_result[0], 'file':plot_result[1], 'data':result}
    
    def post_popularity(self, username, post_popularities):
        """
        Get the popularity data from each post from a specific user in order
        to plot them in a HTML table. Depending on the social media source,
        the data could be different.

        Parameters
        ----------
        username : str
            It's the username of the studied user.
        post_popularities : dict
            It's the dict which contains the media ids as well as the media
            interactions to analyze.

        Raises
        ------
        UsernameNotFound
            If the provided username is not a non-empty string.
        InvalidSocialMediaSource
            If the provided social media source is not a non-empty string or 
            it's not valid.
        PostPopularityNotFound
            If the provided posts are not in a non-empty dict.

        Returns
        -------
        A list of lists in which there are the analysis results for each post.
        """
        # Check the provided username
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")
        # Check the provided list of posts
        if (type(post_popularities) != dict or len(post_popularities) == 0):
            raise PostPopularityNotFound("ERROR. The posts should be in a non-empty dict.")
            
        # Computes the average of the number of likes and comments
        media_codes = [item[0] for item in post_popularities["data"]]
        unique_media_codes = list(dict.fromkeys(media_codes))
        results = []
        for code in unique_media_codes:
            likes = [int(item[1]) for item in post_popularities["data"] if item[0] == code]
            comments = [int(item[2]) for item in post_popularities["data"] if item[0] == code]
            indexes = [post_popularities["ids"][post_popularities["data"].index(item)] for item in post_popularities["data"] if item[0] == code]
            results.append((indexes, round(sum(likes)/len(likes)), round(sum(comments)/len(comments))))    
        
        return results
    
    ############################ TEXT ANALYSIS ##############################
    def sentiment_analysis_text(self, username, text_data):
        """
        Performs a sentiment analysis on a list of texts in order to show the
        number of positive, neutral and negative texts on a pie plot along with
        the polarity of each one of them, which shows how sure the classifier is
        when it labeled each text. The plot will be saved as an image.

        Parameters
        ----------
        username : str
            It's the username of the studied user.
        text_data : dict
            It's a dict whose first key is the list of text ids, and whose second
            key is a list of tuples which contains the preprocessed text to analyze.

        Raises
        ------
        UsernameNotFound
            If the provided username is not a non-empty string.
        TextTupleNotFound
            If the provided texts to analyse are not a non-empty list of strings.

        Returns
        -------
        True if the pie chart could be plotted and saved as an image, False if it couldn't.
        """
        # Check the provided username
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")
        # Check the provided list of post texts
        if (type(text_data) != dict or len(text_data) == 0 or 'ids' not in text_data or 'data' not in text_data):
            raise TextDataDictNotFound("ERROR. The preprocessed text should be a non-empty dict.")

        # Perform the sentiment analysis
        analysis_results = []
        analyzer = SentimentIntensityAnalyzer()
        total_sentiments = {'pos':0.0, 'neu':0.0, 'neg':0.0}
        total_degree = {'pos':0.0, 'neu':0.0, 'neg':0.0}
        analyzed_texts = 0
        
        for i in range(0, len(text_data["ids"])):
            # Check that there are two fields: id and text
            if (type(text_data["data"][i]) != tuple or len(text_data["data"][i]) != 1):
                raise TextTupleNotFound("ERROR. The preprocessed text to analyze should be in a one-size tuple.")
            
            # Get the sentiments
            analysis = analyzer.polarity_scores(text_data["data"][i][0])
            del analysis['compound']
            # Get the sentiment of the text
            sentiment = "none"
            if (analysis['pos'] != 0 or analysis['neu'] != 0 or analysis['neg'] != 0):
                analyzed_texts += 1
                sentiment = max(analysis, key=analysis.get)
                # Total count
                total_sentiments[sentiment] += 1
                total_degree[sentiment] += analysis[sentiment]
            
            # Get the degree of each sentiment
            analysis_results.append({"id_text":text_data["ids"][i], 
                                     "pos_degree":analysis['pos'], 
                                     "neu_degree":analysis['neu'],
                                      "neg_degree":analysis['neg'], 
                                      "sentiment":sentiment})
        # Plot the pie chart
        values = list(total_sentiments.values())
        labels = ["Positive\npolarity: "+str(round(total_degree['pos']/analyzed_texts,2))+" %",
                  "Neutral\npolarity: "+str(round(total_degree['neu']/analyzed_texts,2))+" %",
                  "Negative\npolarity: "+str(round(total_degree['neg']/analyzed_texts,2))+" %"]
        file_name = self.text_sentiments_path + username
        colours = ['lightgreen', 'gold', 'lightcoral']
        plot_result = self.plot_pie_chart(values, labels, file_name, colours)
        
        return {'state':plot_result[0], 'file':plot_result[1], 'data':analysis_results}

    def user_behaviours(self, username, user_list):
        """
        Draws the evolution of the number of haters and friends based on the
        sentiment analysis performed on their comments during a specific time.
        It could be a week or more than a week. The plot will be a line chart
        and it will be saved as an image.

        Parameters
        ----------
        username : str
            It's the username of the studied user.
        user_list : list of tuples
            It's the list of users which their identified sentiment for each date
            of downloaded data.

        Raises
        ------
        UsernameNotFound
            If the provided username is not a non-empty string.
        SentimentTupleNotFound
            If the provided list of sentiments is not a non-empty list of tuples.

        Returns
        -------
        True if the plot could be drawn and saved in a file, False if it couldn't.
        """
        # Check the provided username
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")
        # Check the provided list identified sentiments
        if (type(user_list) != list or len(user_list) == 0):
            raise SentimentTupleNotFound("ERROR. The list of sentiments should be in a non-empty list.")
        # Check that the list of sentiments contains tuples
        user_counts = {}
        for item in user_list:
            if (type(item) != tuple or len(item) != 3):
                raise SentimentTupleNotFound("ERROR. Each item should be a three-length tuple.")
            # First key: date of the downloaded data
            if (item[0] not in user_counts):
                user_counts[item[0]] = {}
            # Second key: the username
            if (item[1] not in user_counts[item[0]]):
                user_counts[item[0]][item[1]] = {'pos':0, 'neg':0}
            # Add the identified sentiment
            if (item[2] != "none" and item[2] != "neu"):
                user_counts[item[0]][item[1]][item[2]] += 1
        
        # Count the number of friends and haters per date
        haters_and_friends = []
        for date in user_counts:
            haters = 0
            friends = 0
            for user in user_counts[date]:
                if (user_counts[date][user]["pos"] != 0 or user_counts[date][user]["neg"]):
                    if (user_counts[date][user]["pos"] > user_counts[date][user]["neg"]):
                        friends += 1
                    else:
                        haters += 1
            # Add the total count
            haters_and_friends.append((date, friends, haters))
        
        # Get the data per week or per more than a week
        if (len(haters_and_friends) <= 7):
            username += "_1week"
            result = self.get_values_per_one_week(haters_and_friends, ['date', 'friends', 'haters'])
        else:
            result = self.get_values_per_many_weeks(haters_and_friends, ['date', 'friends', 'haters'])
            username += "_"+str(len(result['date']))+"weeks"
        
        # Set the path and the title of the file
        file_name = self.user_behaviours_path + username
        # Draw the line plot
        plot_result = self.plot_lines_chart([result['friends'], result['haters']],
                 ['Friends', 'Haters'], result['date'], file_name)
        return {'state':plot_result[0], 'file':plot_result[1], 'data':result}

    ###########################################################################
    ############################## PLOT METHODS  ##############################
    def plot_lines_chart(self, list_values, legend_labels, x_labels, file):
        """
        Draws the provided data in a line plot and set the legend as well as the
        labels for the X axis. The colours will be chosen randomly.
        In the end, the plot will be saved as an image in the provided path and file name.

        Parameters
        ----------
        list_values : list of numbers
            They are the values to plot in the Y axis.
        x_labels : list of strings
            They are the labels for each different value.
        legend_labels : list of strings
            They are the labels for each different data.
        file : str
            It's the path and file name to save the plot as an image.

        Raises
        ------
        InvalidLinePlotData
            If some of the previous parameters are wrong.

        Returns
        -------
        The path and file name in which the plot has been saved as well as the 
        state of the analysis. True if it could be done, False if it couldn't.
        """
        # Check the provided values
        if (type(list_values) != list or len(list_values) == 0 or 
            not all(isinstance(record, list) for record in list_values)):
            raise InvalidLinePlotData("ERROR. Values should be a non-empty list of lists.")
        # Check the provided legend labels
        if (type(legend_labels) != list or len(legend_labels) == 0 or
            type(x_labels) != list or len(x_labels) == 0):
            raise InvalidLinePlotData("ERROR. The labels of the legend and the X axis labels should be a non-empty lists.")
        # Check the rest of the provided data
        if (type(file) != str or file == ""):
            raise InvalidLinePlotData("ERROR. The file title should be a non-empty string.")
        
        # Draws each list of values in the same plot.
        plt.figure(figsize=(8, 8))
        for i in range(0, len(list_values)):
            positions = np.arange(len(list_values[i]))
            # Different colors for the line and the marker
            color = i%len(self.colors_line_plots)
            plt.plot(positions, list_values[i], color=self.colors_line_plots[color], 
                      mec=self.colors_line_plots[color] ,linestyle="--", 
                      marker="o", lw=3, mew=5, label=legend_labels[i])
        
        # General plot data
        plt.xticks(positions, x_labels, rotation='45')
        plt.legend()
        now = datetime.now()
        current_time = now.strftime("%d_%m_%Y_%H_%M_%S")
        file_title = file+"_"+current_time+".png"
        plt.savefig(file_title)
        
        return os.path.isfile(file_title), file_title

    def plot_bars_chart(self, values, x_labels, file, differences=None):
        """
        Draws the provided data in a bar plot and set the labels for the X axis
        The colours will be chosen randomly.
        In the end, the plot will be saved as an image in the provided path and file name.

        Parameters
        ----------
        values : list of numbers
            They are the values to plot in the Y axis.
        x_labels : list of strings
            They are the labels for each one of the values.
        file : str
            It's the path and file name to save the plot as an image.

        Raises
        ------
        InvalidBarPlotData
            If some of the previous parameters are wrong.

        Returns
        -------
        True if the plot could be saved as an image, False if it couldn't.
        """
        # Check the provided data
        if (type(values) != list or len(values) == 0 or len(x_labels) == 0 or type(x_labels) != list):
            raise InvalidBarPlotData("ERROR. Values and x_labels should be non-emtpy lists.")
        # Check strings like y_label, plot_title and file_title
        if (type(file) != str or file == ""):            
            raise InvalidBarPlotData("ERROR. The file name should be a non-empty string.")
        # Check if there are some provided values to set above the bars
        if (differences != None):
            if (type(differences) != list or len(differences) == 0):
                raise InvalidBarPlotData("ERROR. The values to set above the bars should be a non-empty list.")
        
        plt.figure(figsize=(8, 8))
        positions = np.arange(len(values))
        colors = np.random.rand(len(values),3)
        bar = plt.bar(positions, values, align='center', alpha=0.5, color=colors)
        # Add the provided values above the bars
        if (differences != None):
            index = 0
            for i in range(1, len(bar)):
                height = bar[i].get_height()
                sign = "+" if differences[index] > 0 else "-"
                plt.text(bar[i].get_x() + bar[i].get_width()/2.0, height, sign+str(differences[index]), ha='center', va='bottom')
                index += 1
                
        plt.xticks(positions, x_labels, rotation='45')
        now = datetime.now()
        current_time = now.strftime("%d_%m_%Y_%H_%M_%S")
        file_title = file+"_"+current_time+".png"
        plt.savefig(file_title)
        
        return os.path.isfile(file_title), file_title
    
    def plot_pie_chart(self, values, labels, file, colours=None):
        """
        Draws the provided data in a pie chart and set the labels for each
        piece. The colours can be provided or they will be chosen randomly.
        In the end, the plot will be saved as an image in the provided path and file name.

        Parameters
        ----------
        values : list of numbers
            They're the values to plot in the pie chart.
        labels : list of strings
            They are the labels for each different value.
        colours: list of strings
            They are the colours to plot each piece of the pie chart.
        file : str
            It's the path and file name to save the plot as an image.

        Raises
        ------
        InvalidPiePlotData
            If some of the provided parameters are wrong.

        Returns
        -------
        True if the pie chart could be plotted and saved in a fil, False if it couldn't.
        """
        # Check the provided data
        if (type(values) != list or type(labels) != list or len(values) == 0  or len(labels) == 0):
            raise InvalidPiePlotData("ERROR. Values and labels should be non emtpy lists.")
        # Values and x_labels should have the same lenght to be plotted
        if (len(values) != len(labels)):
            raise InvalidPiePlotData("ERROR. Values and labels should have the same lenght.")
        # Check the provided path and file name
        if (type(file) != str or file == ""):
            raise InvalidPiePlotData("ERROR. The title should be a non-empty string.")
        # Check the provided colours
        if (type(colours) != str and type(colours) != list):
            colours = np.random.rand(len(values),3)
        
        # Plot the pie chart
        plt.figure()
        plt.pie(values, labels=labels, colors=colours, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        now = datetime.now()
        current_time = now.strftime("%d_%m_%Y_%H_%M_%S")
        file_title = file+"_"+current_time+".png"
        plt.savefig(file_title)
        
        return os.path.isfile(file_title), file_title
    