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

import pandas as pd
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

from exceptions import InvalidLinePlotData, ProfilesNotFound, UsernameNotFound \
    , InvalidBarPlotData, UserActivityNotFound

class DataAnalyzer:
    
    def __init__(self):
        """
        Creates a DataAnalyzer object whose attributes are:
            - The list of colours to draw the plots.
            - The default path to store the differents plots.

        Returns
        -------
        A DataAnalyzer object.
        """
        self.colors_line_plots = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        self.plot_tests_path = "./imgs/tests/"
        self.profile_evolution_path = "./imgs/profiles-evolution/"
        self.user_activity_path = "./imgs/user-activity/"
        
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

        Raises
        ------
        UsernameNotFound
            If the provided username is not a non-empty string.
        ProfilesNotFound
            If the provided profiles are not a non-empty list of tuples.

        Returns
        -------
        True if the plot could be drawn and saved in a image, False if it's not.
        """
        # Check the provided username
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")
        # Check the provided list of profiles
        if (type(profile_list) != list or len(profile_list) == 0):
            raise ProfilesNotFound("ERROR. The profiles to study should be in a non-empty list.")
        
        # Check the content of each profile
        post_list = []
        followers_list = []
        followings_list = []
        date_list = []
        for profile in profile_list:
            if (type(profile) != tuple or len(profile) != 4):
                raise ProfilesNotFound("ERROR. The three fields to analyze the profile evolution should be tuples.")
            # Get each data separately
            date_list.append(profile[0])
            post_list.append(int(profile[1]))
            followers_list.append(int(profile[2]))
            followings_list.append(int(profile[3]))
        
        # Draw the line plot
        file_name = self.profile_evolution_path + username
        return self.plot_lines([followers_list, followings_list, post_list],
                 ['Followers', 'Followings', 'Posts'], date_list, file_name)
    
    def user_activity(self, username, activity_list):
        """
        Draws a bar plot about the user activity based on the numbers of uploaded
        posts per week or month. The plot will be saved as an image.

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
        True if the plot could be drawn and saved in a image, False if it's not.
        """
        # Check the provided username
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")
        # Check the provided list of user activity
        if (type(activity_list) != list or len(activity_list) == 0):
            raise UserActivityNotFound("ERROR. The user activity should be a non-empty list.")

        date_list = []
        post_list = []
        # PLOTTING EACH DAY IN DIFFERENT BARS (MAX 7 BARS)
        if (len(activity_list) <= 7):
            username += "_week"
            for activity in activity_list:
                print(type(activity) != tuple or len(activity) != 2)
                if (type(activity) != tuple or len(activity) != 2):
                    raise UserActivityNotFound("ERROR. The two fields to analyze the user activity should be tuples.")
                # Get each field separetely
                date_list.append(activity[0])
                post_list.append(int(activity[1]))
        # PLOTTING PER WEAK WITH WEAK MEANS
        else:
            add = []
            week_number = 1
            for activity in activity_list:
                if (type(activity) != tuple or len(activity) != 2):
                    raise UserActivityNotFound("ERROR. The two fields to analyze the user activity should be tuples.")
                # Get each field separetely
                if (len(add) < 7):
                    add.append(int(activity[1]))
                else:
                    date_list.append("Week "+str(week_number))
                    post_list.append(sum(add)/7)
                    add = []
                    week_number += 1
            
            # If there are some activies left
            if (len(add) > 0):
                date_list.append("Week "+str(week_number))
                post_list.append(sum(add)/len(add))
            
            username += "_"+str(week_number)+"_more"
        
        # Compute the differences between the number of posts
        differences = []
        for i in range(1, len(post_list)):
            differences.append(round(post_list[i] - post_list[i-1]))
        # Draw the bar plot
        file_name = self.user_activity_path + username
        return self.plot_bars(post_list, date_list, file_name, differences)
            
    ###########################################################################
    ############################## PLOT METHODS  ##############################
    def plot_lines(self, list_values, legend_labels, x_labels, file):
        """
        Draws the provided data in a line plot and set the legend as well as the
        labels for the X axis. The colours will be chosen randomly.
        In the end, the plot will be saved as an image in the provided path and file name.

        Parameters
        ----------
        list_values : list
            They are the values to plot in the Y axis.
        legend_labels : list
            They are the values to plot in the X axis.
        x_labels : str
            It's the title for the X axis.
        file : str
            It's the path and file name to save the plot as an image.

        Raises
        ------
        InvalidLinePlotData
            If some of the previous parameters are wrong.

        Returns
        -------
        True if the plot could be saved as an image, False if it couldn't.
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
        
        return os.path.isfile(file_title)

    def plot_bars(self, values, x_labels, file, differences=None):
        """
        Draws the provided data in a bar plot and set the labels for the X axis
        The colours will be chosen randomly.
        In the end, the plot will be saved as an image in the provided path and file name.

        Parameters
        ----------
        list_values : list
            They are the values to plot in the Y axis.
        x_labels : str
            It's the title for the X axis.
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
        if (type(values) != list or type(x_labels) != list):
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
        
        return os.path.isfile(file_title)