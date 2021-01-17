#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains the different analysis which could be performed in the platform.
These analysis are:
    - A profile evolution, which will show the evolution of the number of followers,
    followings and posts over a specific period of time.
    - The user activity based on the number of posts they uploaded per date.
    - How interesting the posts of a specific user are based on the number of interactions
    from the other members of the social media.
    - The best/worst posts based on the different interactions such as the number of
    likes and comments.
    - The percentage of positive, neutral and negative comments and post titles
    during a specific period of time.
    - The user behaviours which could be identified from the previous sentiment analysis
    based on the comments they wrote on the posts of a specific user.

@author: Lidia Sánchez Mérida
"""
# Sentiment Analyzer based on pre-trained models
from flair.models import TextClassifier
from flair.data import Sentence
        
# Sentiment Analyzer based on lexicon
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from exceptions import ValuesNotFound, KeysNotFound, ExpectedSameSize \
    , ProfilesNotFound, UsernameNotFound, TextNotFound \
    , UserActivityNotFound, PostInteractionsNotFound \
    , PostPopularityNotFound, TextDataNotFound, SentimentNotFound

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
        # List of avalaible analysis
        self.avalaible_analysis = [
           "profile_evolution", "profile_activity",
           "media_evolution", "media_popularity", 
           "comment_sentiment_analysis", "title_sentiment_analysis", 
           "user_behaviours",
           
           "test_profile_evolution", "test_profile_activity",
           "test_media_evolution", "test_media_popularity",
           "test_comment_sentiment_analysis", "test_title_sentiment_analysis", 
           "test_user_behaviours"]
    
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
        weeks = ["Semana "+str(i+1) for i in range(0, len(result[keys[1]]))]
        result['date'].extend(weeks)
        
        return result
        
    ########################## PROFILE ANALYSIS ##############################
    def profile_evolution(self, username, profile_list):
        """
        Computes the evolution of the number of followers, followings as well
        as the uploaded posts over a specific period of time. If it's more than
        7 days, the method will calculate the average of each field per week.

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
        A dict which contains the ProfilesEvolution analysis results per date.
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
            return self.get_values_per_one_week(profile_list, 
                          ['date', 'n_posts', 'n_followers', 'n_followings'])
        # Get the values per more than a week
        else:
            return self.get_values_per_many_weeks(profile_list, 
                        ['date', 'n_posts', 'n_followers', 'n_followings'])
    
    def user_activity(self, username, activity_list):
        """
        Gets the activiy of a specific user based on the number of uploaded posts
        during a specific period of time. If it's more than 7 days, the method will
        calculate the user activity per weeks.

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
        A dict dict which contains the UserActivity analysis results per date.
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
            return self.get_values_per_one_week(activity_list, 
                          ['date', 'n_posts'])
        # Get the values per more than a week
        else:
            return self.get_values_per_many_weeks(activity_list, 
                        ['date', 'n_posts'])
    
    ############################ POSTS ANALYSIS ##############################
    def post_evolution(self, username, post_interactions):
        """
        Computes the interest of the posts from a specific user during a particular
        period of time based on the provided interactions, such as the number of 
        likes and comments. If it's more than 7 days, the method will calculate the
        average of each interaction per week.

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
        A dict with the PostsEvolution analysis results per date.
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
                raise PostInteractionsNotFound("ERROR. The three fields to analyze the medias evolution should be tuples.")
        
        # Compute the mean of likes and comments for each post
        mean_post_interactions = []
        # Get the dates without duplicates
        dates = list(set([item[0] for item in post_interactions]))
        dates.sort()
        # Compute an average of the number of comments and likes per day
        for date in dates:
            likes = [int(item[1]) for item in post_interactions if item[0] == date]
            comments = [int(item[2]) for item in post_interactions if item[0] == date]
            mean_post_interactions.append((date, round(sum(likes)/len(likes)), round(sum(comments)/len(comments))))
        
        # Get the values per one week
        if (len(mean_post_interactions) <= 7):
            return self.get_values_per_one_week(mean_post_interactions, 
                          ['date', 'like_count', 'comment_count'])
        # Get the values per more than a week
        else:
            return self.get_values_per_many_weeks(mean_post_interactions, 
                        ['date', 'like_count', 'comment_count'])
    
    def post_popularity(self, username, post_popularities, mode="best"):
        """
        Gets the most or worst popular posts of a specific user during the provided
        period of time based on a set of interactions, such as the number of likes
        and comments. 

        Parameters
        ----------
        username : str
            It's the username of the studied user.
        post_popularities : dict
            It's the dict which contains the media ids as well as the media
            interactions to analyze.
        mode : str
            It's the type of order to sort the medias. Options are:
                - best, it will plot the best popular posts.
                - worst, it will plot the posts with less interactions.

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
        A sorted list with the ten matched posts.
        """
        # Check the provided username
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")
        # Check the provided list of posts
        if (type(post_popularities) != list or len(post_popularities) == 0):
            raise PostPopularityNotFound("ERROR. The posts should be in a non-empty dict.")
        # Check that there are four types of values for: date, n_posts, n_followers and n_followings
        for interaction in post_popularities:
            if (type(interaction) != tuple or len(interaction) != 3):
                raise PostInteractionsNotFound("ERROR. The three fields to analyze the medias popularity should be tuples.")
        
        # Computes the average of the number of likes and comments
        media_codes = [item[0] for item in post_popularities]
        unique_media_codes = list(dict.fromkeys(media_codes))
        analysis_results = []
        for code in unique_media_codes:
            likes = [int(item[1]) for item in post_popularities if item[0] == code]
            comments = [int(item[2]) for item in post_popularities if item[0] == code]
            mean_likes = round(sum(likes)/len(likes))
            mean_comments = round(sum(comments)/len(comments))
            analysis_results.append((code, mean_likes, mean_comments)) 
        
        return analysis_results
    
    ############################ TEXT ANALYSIS ##############################
    def sentiment_analysis_text(self, username, text_data):
        """
        Performs a sentiment analysis on a list of texts in order to show the
        number of positive, neutral and negative texts on a chart along with
        the polarity of each one of them, which shows how sure the classifier is
        when it labeled each text. 

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
        A list of tuples which contains the analyzed text without preprocessing,
        the identified sentiment as well as the polarity degree.
        """
        # Check the provided username
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")
        # Check the provided list of post texts
        if (type(text_data) != list or len(text_data) == 0):
            raise TextDataNotFound("ERROR. The preprocessed texts to analyze should be a non-empty list of tuples.")

        # For pre-trained models 
        flair_analyzer = TextClassifier.load('sentiment')
        # For VADER lexicon
        vader_analyzer = SentimentIntensityAnalyzer()
        
        # Perform the sentiment analysis
        text_analysis_results = []
        for text in text_data:
            # Check that there are two fields: id and text
            if (type(text) != tuple or len(text) != 3):
                raise TextNotFound("ERROR. The text to analyze should be in a three-size tuple.")
            
            # 1. Apply a pre-trained model to identifiy the sentiment of the text
            sentence = Sentence(text[1])
            flair_analyzer.predict(sentence)
            total_sentiment = sentence.labels
            if (len(total_sentiment) > 0):
                sentiment = total_sentiment[0].value
                score = total_sentiment[0].score
                sentiment = "pos" if sentiment.lower() == "positive" else "neg"
                # Analysis results to insert
                text_analysis_results.append({"original_text":text[2], "sentiment":sentiment, "degree":score})
            # 2. Apply the VADER lexicon if the pre-trained model could not identify the sentiment of the text
            else: #pragma no cover
                # Get the sentiments
                analysis = vader_analyzer.polarity_scores(text[1])
                del analysis['compound']
                # Get the sentiment of the text
                sentiment = "none"
                if (analysis['pos'] != 0 or analysis['neu'] != 0 or analysis['neg'] != 0):
                    sentiment = max(analysis, key=analysis.get)
                # Analysis results to insert
                text_analysis_results.append({"original_text":text[2], "sentiment":sentiment, 
                                              "degree":analysis[sentiment] if sentiment != "none" else 0.0})
        
        return text_analysis_results

    def user_behaviours(self, username, user_list):
        """
        Computes the evolution of the number of haters and friends based on the
        sentiment analysis performed on their comments during a specific period of
        time. If it's more than 7 days, the method will calculate the average of 
        likers and haters per week.

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
        A dict with the UserBehaviours analysis results per date.
        """
        # Check the provided username
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")
        # Check the provided list identified sentiments
        if (type(user_list) != list or len(user_list) == 0 or 
            not all(isinstance(item, dict) for item in user_list)):
            raise SentimentNotFound("ERROR. The users to analyze should be in a non-empty list of dicts.")
        
        # Count the number of different sentiments for each date without duplicates
        user_patterns = {}
        for item in user_list:
            if ("date" not in item or "author" not in item or "sentiment" not in item):
                raise SentimentNotFound("ERROR. Each item should be the three keys: 'date', 'author' and 'sentiment'.")
            
            # Case 1. The date is not in the analysis results
            if (item["date"] not in user_patterns):
                user_patterns[item["date"]] = {}
            # Case 1.1. The user is not in the analysis results
            if (item["author"] not in user_patterns):
                user_patterns[item["date"]][item["author"]] = {"pos":0, "neu":0, "neg":0}
            # Add the identified sentiment
            if (item["sentiment"] != "none"):
                user_patterns[item["date"]][item["author"]][item["sentiment"]] += 1
        
        # Get the number of likers and haters per date without duplicates
        behaviour_summary = []
        for date in user_patterns:
            n_likers = 0
            n_haters = 0
            for user in user_patterns[date]:
                if (max(user_patterns[date][user], key=user_patterns[date][user].get) == "pos"): n_likers += 1
                elif (max(user_patterns[date][user], key=user_patterns[date][user].get) == "neg"): n_haters += 1
        
            # Add the results per date in order to plot them
            behaviour_summary.append((date, n_likers, n_haters))
                    
        # Get the data per week or per more than a week
        if (len(behaviour_summary) <= 7):
            return self.get_values_per_one_week(behaviour_summary, ['date', 'likers', 'haters'])
        else:
            return self.get_values_per_many_weeks(behaviour_summary, ['date', 'likers', 'haters'])