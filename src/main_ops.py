#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains the main operations which can be done on the web platform.

@author: Lidia Sánchez Mérida
"""
from datetime import datetime
import sys
sys.path.append('src/data')
sys.path.append('data')

from api import Api
import commondata
import data_analyzer
from mongodb import MongoDB
from postgredb import PostgreDB
from exceptions import UsernameNotFound, MaxRequestsExceed, UserDataNotFound \
   , InvalidMongoDbObject, InvalidSocialMediaSource, InvalidMode, InvalidAnalysis \
    , InvalidDates, CollectionNotFound, InvalidQuery

class MainOperations:

    def __init__(self):
        """
        Creates a MainOperations object whose attributes are:
            - A MongoDB object to operate with the Mongo database.
            - A PostgresDB object to operate with the PostgreSQL database.
            - The MongoDB collections to store the preprocessed data depending
            on the context (test or real).
            - A CommonData object to preprocess the user data.
            - A DataAnalyzer object to perform the different analysis.
            - The list of avalaible analysis.
            
            
        Raises
        ------
        InvalidDatabaseCredentials
            If the credentials are not non-empty strings, are not saved in env
            variables or are wrong.

        Returns
        -------
        A MainOperations object.
        """
        # Mongo database credentials and collections
        self.mongodb_object = MongoDB('test')
        self.mongo_collections = {
            'test':{'profiles':'test', 'medias':'test_medias', 'comments':'test_comments'},
            'real':{'profiles':'profiles', 'medias':'medias', 'comments':'comments'}
            }
        # Relationship between the different analysis and the Mongo collections
        # in which there are the required data to perform them
        self.analysis_mongo_collections = {
            'test_profile_evolution':'test',
            'test_profile_activity':'test',
            'test_media_evolution':'test_medias',
            'test_media_popularity':'test_medias',
            'test_comment_sentiment_analysis':'test_comments',
            'test_title_sentiment_analysis':'test_comments',
            
            'profile_evolution':'profiles',
            'profile_activity':'profiles',
            'media_evolution':'medias',
            'media_popularity':'medias',
            'comment_sentiment_analysis':'comments',
            'title_sentiment_analysis':'medias',
        }
        
        # Postgre database connection
        self.postgresdb_object = PostgreDB()
        # Postgres insert queries for the data required for each analysis
        self.analysis_postgres_insert_queries = {
            "test_profile_evolution":"insert_test_profile",
            "test_profile_activity":"insert_test_profile",
            "test_media_evolution":"insert_test_medias",
            "test_media_popularity":"insert_test_medias",
            "test_comment_sentiment_analysis":"insert_test_media_comments",
            "test_title_sentiment_analysis":"insert_test_media_titles",
            
            "profile_evolution":"insert_profile",
            "profile_activity":"insert_profile",
            "media_evolution":"insert_medias",
            "media_popularity":"insert_medias",
            "comment_sentiment_analysis":"insert_media_comments",
            "title_sentiment_analysis":"insert_medias",
        }
        # Postgres select queries for each analysis
        self.analysis_postgres_select_queries = {
            "test_profile_evolution":"test_get_profiles",
            "test_profile_activity":"test_get_nmedias_profiles",
            "test_media_evolution":"test_get_medias",
            "test_media_popularity":"test_get_medias_with_id",
            "test_comment_sentiment_analysis":"test_get_media_comments",
            "test_title_sentiment_analysis":"test_get_media_titles",
            
            "profile_evolution":"get_profiles",
            "profile_activity":"get_nmedias_profiles",
            "media_evolution":"get_medias",
            "media_popularity":"get_medias_with_id",
            "comment_sentiment_analysis":"get_media_comments",
            "title_sentiment_analysis":"get_media_titles",
        }
        # Postgre insert queries to add the analysis results
        self.analysis_results_insert_queries = {
            "test_profile_evolution":"insert_test_profile_evolution",
            "test_profile_activity":"insert_test_profile_activity",
            "test_media_evolution":"insert_test_medias_evolution",
            "test_media_popularity":"insert_test_medias_popularity",
            "test_comment_sentiment_analysis":"insert_test_sentiment_analysis",
            "test_title_sentiment_analysis":"insert_test_sentiment_analysis",
            "test_user_behaviours":"insert_test_user_behaviour",
            
            "profile_evolution":"insert_profile_evolution",
            "profile_activity":"insert_profile_activity",
            "media_evolution":"insert_medias_evolution",
            "media_popularity":"insert_medias_popularity",
            "comment_sentiment_analysis":"insert_sentiment_analysis",
            "title_sentiment_analysis":"insert_sentiment_analysis",
            "user_behaviours":"insert_user_behaviour",
        }
        
        # CommonData object to preprocess the user data before inserting them
        self.common_data_object = commondata.CommonData(self.mongodb_object)
        # DataAnalyzer object to perform the chosen analysis
        self.data_analyzer_object = data_analyzer.DataAnalyzer()

    def get_user_instagram_common_data(self, search_user, mode):
        """
        Gets common Instagram data of a specific user using the LevPasha Instagram
        API. The downloaded user data is stored in the Mongo database.

        Parameters
        ----------
        search_user : str
            It's the username of the user to get their data.
        mode : str
            It's the mode in which the user data will be stored in the Mongo database.

        Raises
        ------
        UsernameNotFound
            If the provided username is not a non-empty string.
        InvalidMode
            If the provided mode is not 'test' or 'real'.
        MaxRequestsExceed
            If the maximum number of requests of the LevPasha Instagram API
            has been exceeded.

        Returns
        -------
        A dict with the downloaded user data.
        """
        # Check the provided user
        if (search_user == None or type(search_user) != str or search_user == ""):
            raise UsernameNotFound("ERROR. Invalid username.")
        # Check the provided mode
        if (mode != "test" and mode != "real"):
            raise InvalidMode("ERROR. The mode should be 'test' or 'real.")
        try:
            # Connect to the Levpasha Instagram API
            inst_api = Api()
            inst_api.connect_levpasha_instagram_api()
            # Download Instagram user data
            user_instagram_data = inst_api.get_levpasha_instagram_data(search_user)
            # Preprocess and store user data
            user_data = self.preprocess_and_store_common_data(user_instagram_data, "Instagram", mode)
            return user_data
        except MaxRequestsExceed:   # pragma: no cover
            # Try to connect again to the Instagram LevPasha API using the credentials
            # instead of the session file in order to avoid logout exceptions
            try:
                inst_api = Api()
                inst_api.connect_levpasha_instagram_api(use_session_file=False)
                user_instagram_data = inst_api.get_levpasha_instagram_data(search_user)
                user_data = self.preprocess_and_store_common_data(user_instagram_data, "Instagram", mode)
                return user_data
            except MaxRequestsExceed:   # pragma: no cover
                raise MaxRequestsExceed("Max requests exceed. Wait to send more.")

    def preprocess_and_store_common_data(self, user_data, social_media, mode):
        """
        Preprocesses the common data of a specific user from any API source and
        stores them in the Mongo database, if there aren't any items with the same
        id and date. In this case, the provided user data won't be inserted.

        Parameters
        ----------
        user_data : dict
            It's the user data to preprocess and store.
        social_media : str
            It's the social media which the user data came from.
        mode : str
            It's the mode in which the user data will be stored in the Mongo database.

        Raises
        ------
        UserDataNotFound
            If the provided user data is not a dict.
        InvalidSocialMediaSource
            If the provided social media source is not a non-empty string or it's
            not one of the avalaible social media sources.
        InvalidMode
            If the provided mode is not 'test' or 'real'.
        InvalidMongoDbObject
            If the MongoDB object has not been initialized and does not have the
            connection to the Mongo database.

        Returns
        -------
        A dict whose keys are the different user data and whose values indicate
        if each type of user data has been inserted in the Mongo database. Options are:
            - None, the item has not been inserted.
            - str, the id of the new inserted item.
        """
        if (type(user_data) != dict or len(user_data) == 0):
            raise UserDataNotFound("ERROR. User data should be a non empty dict.")
        # Check the provided social media source
        if (type(social_media) != str or social_media == ""):
            raise InvalidSocialMediaSource("ERROR. The social media source should be a non-empty string.")
        if (social_media.lower() not in self.common_data_object.social_media_sources):
            raise InvalidSocialMediaSource("ERROR. Avalaible social media sources: "
               +str(self.common_data_object.social_media_sources))
        # Check the provided mode
        if (mode != "test" and mode != "real"):
            raise InvalidMode("ERROR. The mode should be 'test' or 'real.")

        # Check the Mongo database object
        if (type(self.mongodb_object) != MongoDB):
            raise InvalidMongoDbObject("ERROR. The connection to the MongoDB database "+
                                       "should be a MongoDB object.")
        # Preprocess the user data
        preprocessed_data = self.common_data_object.preprocess_user_data(user_data, social_media)

        # Save the data if they don't already exist
        self.common_data_object.insert_user_data(
            preprocessed_data['profile'], self.mongo_collections[mode]['profiles'])
        self.common_data_object.insert_user_data(
            preprocessed_data['media_list'], self.mongo_collections[mode]['medias'])
        self.common_data_object.insert_user_data(
            preprocessed_data['media_comments'], self.mongo_collections[mode]['comments'])
        
        return {'profile':preprocessed_data["profile"], 'media':preprocessed_data["media_list"], 
                'comments':preprocessed_data["media_comments"]}
    
    def get_data_from_mongodb(self, username, social_media, collection, date_list):
        """
        Gets any kind of user data of a specific social media source and a related
        range of dates by recovering the information from a specific collection 
        in the Mongo database. The process will be run for each provided range 
        of date.

        Parameters
        ----------
        username : str
            It's the username of the studied user to get their data.
        social_media : str
            It's the social media source which the desired data came from.
        collection : str
            It's the collection in which the data will be looked for.
        date_list : list of tuples
            It's the range of dates to add to the query in order to get the data
            for each range.

        Raises
        ------
        UsernameNotFound
            If the provided username is not a non-empty string.
        InvalidSocialMediaSource
            If the provided social media source is not a non-empty string or does
            not exist.
        CollectionNotFound
            If the provided collection name is not a non-empty string or does not
            exist.
        InvalidDates
            If the provided range of dates is not a non-empty list of tuples, 
            does not have the valid format or is wrong.

        Returns
        -------
        A list of dicts in which each one of them is a matched data sample got
        from the collection in the Mongo database.
        """
        # Check the provided username
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")
        # Check the provided social media source
        if (type(social_media) != str or social_media == ""):
            raise InvalidSocialMediaSource("ERROR. The social media source should be a non-empty string.")
        if (social_media.lower() not in self.common_data_object.social_media_sources):
            raise InvalidSocialMediaSource("ERROR. The provided social media is wrong.")
        # Check the provided collection
        if (type(collection) != str or collection == ""):
            raise CollectionNotFound("ERROR. The Mongo collection should be a non-empty string.")
        
        # Check the provided list of dates
        if (type(date_list) != list or len(date_list) == 0):
            raise InvalidDates("ERROR. The dates should be a non-empty lists of tuples")
        # Check each range of date
        mongo_data = []
        for date_range in date_list:
            # Check if it's a tuple of length 2
            if (type(date_range) != tuple or len(date_range) != 2):
                raise InvalidDates("ERROR. Each range of dates should be a non-empty tuple of lenght 2.")
            # Check the provided range of dates
            if (type(date_range[0]) != str or date_range[0] == "" or len(date_range[0]) != 10
                or type(date_range[1]) != str or date_range[1] == "" or len(date_range[1]) != 10):
                raise InvalidDates("ERROR. The range of date should be two non-empty strings.")
            # Check if the range of dates is valid
            try:
                date_ini_datetime = datetime.strptime(date_range[0], "%d-%m-%Y")
                date_fin_datetime = datetime.strptime(date_range[1], "%d-%m-%Y")
            except:
                raise InvalidDates("ERROR. The range of date have a not valid format.")
            # Check that the initial date is lower than the final date
            if (date_ini_datetime > date_fin_datetime):
                raise InvalidDates("ERROR. Invalid range of dates. The initial is greater than the final.")
            
            # Complete the get query to make it to the Mongo database
            mongo_values = {"username":username, "social_media":social_media, "date_ini":date_range[0], "date_fin":date_range[1]}
            # Make the query
            mongo_data.extend(self.common_data_object.get_user_data(collection, "get_item", mongo_values))
        
        return mongo_data
    
    def get_data_from_postgresdb(self, query, select_values):
        """
        Gets the user data related to the provided query and values from a specific
        table of the Postgres database. The select query will be made as many times
        as the number of select values.
        
        The method will also separate the ids from the recovered data in order to know
        which data samples will participate in the user analysis.

        Parameters
        ----------
        query : str
            It's the select query to make in the Postgres database.
        select_values : list of dicts
            It's the number of select queries to make as well as the values to
            filter the data to recover.

        Raises
        ------
        InvalidQuery
            If the provided query is not a non-empty string or does not exist.
        UserDataNotFound
            If the provided values are not a non-empty list of dicts.

        Returns
        -------
        A dict whose first values are the ids from the recovered data and whose 
        second values are the recorevered data samples which matched with the
        select query.
        """
        # Check the provided query
        if (type(query) != str or query == ""):
            raise InvalidQuery("ERROR. The select query should be a non-empty string.")
        # Check the provided select values
        if (type(select_values) != list or len(select_values) == 0 or
            not (all(isinstance(item, dict) for item in select_values))):
            raise UserDataNotFound("ERROR. The select values should be a non-empty list of dicts.")
        
        # Get the id from the got data separately
        postgres_data = []
        id_data = []
        for item in select_values:
            required_data = self.postgresdb_object.get_data(query, item)
            for sample in required_data:
                id_data.append(sample[0])
                without_id = list(sample)
                without_id.pop(0)
                postgres_data.append(tuple(without_id))
        
        return {"ids":id_data, "data":postgres_data}
    
    def perform_profile_evolution(self, username, analysis, social_media, 
                                  date_ini, date_fin):
        """
        Performs the Profiles Evolution analysis since the beginning. The method
        will get the required user data from the Mongo database which belong to
        the provided range of dates. Then, the recovered data samples will be inserted
        in the Postgres database if they're not already. Finally, only the required
        fields will be recovered in order to perform this type of analysis and plot
        the results.

        Parameters
        ----------
        username : str
            It's the username of the user which is going to be studied.
        analysis : str
            It's the type of analysis to perform.
        social_media : str
            It's the social media source which the user data will be recovered.
        date_ini : str
            It's the initial date of the period of time to perform the analysis.
        date_fin : str
            It's the final date of the period of time to perform the analysis..

        Returns
        -------
        A dict whose keys are:
            - True if the analysis could be performed and saved in an image file.
            - The file name of the saved analysis results.
            - The ids of the inserted analysis results.
        """
        # 1. Get the required data from Mongo database
        collection = self.analysis_mongo_collections[analysis]
        mongo_data = self.get_data_from_mongodb(username, social_media, collection, [(date_ini, date_fin)])

        # 2. Insert the recovered data to Postgres database
        insert_query = self.analysis_postgres_insert_queries[analysis]
        check_query = self.postgresdb_object.check_queries[insert_query]
        check_keys = self.postgresdb_object.select_queries[check_query]['fields']
        for item in mongo_data:
            if (len(check_keys) > 0):
                check_dict = {key:item[key] for key in check_keys}
            # Insert the data and provide the check values, if there are any
            self.postgresdb_object.insert_data(insert_query, [dict(sorted(item.items()))], [check_dict])

        # 3. Get only the required fields to perform the analysis
        select_query = self.analysis_postgres_select_queries[analysis]
        select_values = {"username":username, "social_media":social_media,
                          "date_ini":date_ini, "date_fin":date_fin}
        required_data = self.postgresdb_object.get_data(select_query, select_values)
        
        # 4. Perform the analysis
        analysis_results = self.data_analyzer_object.profile_evolution(username, required_data)
        # Store the analysis results
        insert_query = self.analysis_results_insert_queries[analysis]
        analysis_ids = []
        for i in range(0, len(analysis_results["date"])):
            if("date" in str(type(analysis_results["date"][i]))):
                analysis_results["date"][i] = datetime.strftime(analysis_results["date"][i], "%d-%m-%Y")
                
            analysis_dict = {"date_fin":date_fin, "date_ini":date_ini, "id_user":username+"_"+social_media,
                             "mean_followers":analysis_results["n_followers"][i],
                             "mean_followings":analysis_results["n_followings"][i],
                             "mean_medias":analysis_results["n_posts"][i], 
                             "time":analysis_results["date"][i]}
            check_values = {"date_ini":date_ini, "date_fin":date_fin, 
                            "id_user":username+"_"+social_media, "time":analysis_results["date"][i]}
            analysis_ids.extend(self.postgresdb_object.insert_data(insert_query, [analysis_dict], [check_values]))
                    
        return analysis_ids
    
    def perform_profile_activity(self, username, analysis, social_media, 
                                 date_ini, date_fin):
        """
        Performs the Profiles Activity analysis since the beginning. The method
        will get the required user data from the Mongo database which belong to
        the provided range of dates. Then, the recovered data samples will be inserted
        in the Postgres database if they're not already. Finally, only the required
        fields will be recovered in order to perform this type of analysis and plot
        the results.

        Parameters
        ----------
        username : str
            It's the username of the user which is going to be studied.
        analysis : str
            It's the type of analysis to perform.
        social_media : str
            It's the social media source which the user data will be recovered.
        date_ini : str
            It's the initial date of the period of time to perform the analysis.
        date_fin : str
            It's the final date of the period of time to perform the analysis..

        Returns
        -------
        A dict whose keys are:
            - True if the analysis could be performed and saved in an image file.
            - The file name of the saved analysis results.
            - The ids of the inserted analysis results.
        """
        # 1. Get the required data from Mongo database
        collection = self.analysis_mongo_collections[analysis]
        mongo_data = self.get_data_from_mongodb(username, social_media, collection, [(date_ini, date_fin)])

        # 2. Insert the recovered data to Postgres database
        insert_query = self.analysis_postgres_insert_queries[analysis]
        check_query = self.postgresdb_object.check_queries[insert_query]
        check_keys = self.postgresdb_object.select_queries[check_query]['fields']
        for item in mongo_data:
            if (len(check_keys) > 0):
                check_dict = {key:item[key] for key in check_keys}
            # Insert the data and provide the check values, if there are any
            self.postgresdb_object.insert_data(insert_query, [dict(sorted(item.items()))], [check_dict])

        # 3. Get only the required fields to perform the analysis
        select_query = self.analysis_postgres_select_queries[analysis]
        select_values = {"username":username, "social_media":social_media,
                          "date_ini":date_ini, "date_fin":date_fin}
        required_data = self.postgresdb_object.get_data(select_query, select_values)
        
        # 4. Perform the analysis
        analysis_results = self.data_analyzer_object.user_activity(username, required_data)
        # Store the analysis results
        insert_query = self.analysis_results_insert_queries[analysis]
        analysis_ids = []
        for i in range(0, len(analysis_results["date"])):
            if("date" in str(type(analysis_results["date"][i]))):
                analysis_results["date"][i] = datetime.strftime(analysis_results["date"][i], "%d-%m-%Y")
                
            analysis_dict = {"date_fin":date_fin, "date_ini":date_ini, "id_user":username+"_"+social_media,
                             "mean_medias":analysis_results["n_posts"][i], 
                             "time":analysis_results["date"][i]}
            check_values = {"date_ini":date_ini, "date_fin":date_fin, 
                            "id_user":username+"_"+social_media, "time":analysis_results["date"][i]}
            analysis_ids.extend(self.postgresdb_object.insert_data(insert_query, [analysis_dict], [check_values]))
                
        return analysis_ids
    
    def insert_media_data(self, username, analysis, social_media, 
                                 date_ini, date_fin):
        """
        Recovers the required media data from the Mongo database and inserts the
        media data as well as their titles and comments.

        Parameters
        ----------
        username : str
            It's the username of the user which is going to be studied.
        analysis : str
            It's the type of analysis to perform.
        social_media : str
            It's the social media source which the user data will be recovered.
        date_ini : str
            It's the initial date of the period of time to perform the analysis.
        date_fin : str
            It's the final date of the period of time to perform the analysis.

        Returns
        -------
        None
        """
        # 1. Get the required data from Mongo database
        collection = "test_medias" if "test" in analysis else "medias"
        mongo_data = self.get_data_from_mongodb(username, social_media, collection, [(date_ini, date_fin)])
        # 2. Insert the recovered medias with their related id profile and title
        # to the Postgres database
        insert_medias_query = "insert_test_medias" if "test" in analysis else "insert_medias"
        insert_titles_query = "insert_test_media_titles" if "test" in analysis else "insert_media_titles"
        get_id_profile_query = "check_test_profile" if "test" in analysis else "check_profile"
        
        for item in mongo_data:
            for media in item["medias"]:
                # 2.1. Get the id of the profile which own the recovered medias
                postgres_data = self.get_data_from_postgresdb(get_id_profile_query, [{"username":username, 
                      "social_media":social_media, "date":item["date"].strftime("%Y-%m-%d")}])                    
                item["id_profile"] = postgres_data["ids"][0]
                # 2.2. Insert the media and recover the id in order to insert the title
                media_checks = {"id_media":media["id_media"], "date":item["date"]}
                media_to_insert = {"id_media":media["id_media"],
                         "id_profile":item["id_profile"],
                         "like_count":media["like_count"],
                         "comment_count":media["comment_count"],
                         "date":item["date"],
                         "uploaded_date":media["taken_at"]}
                media_id = self.postgresdb_object.insert_data(insert_medias_query,
                          [dict(sorted(media_to_insert.items()))], [media_checks])
                
                # 2.3. Preprocess the title of each media
                if (media["title"] != None and len(media_id) > 0):
                    preprocessed_title = self.common_data_object.clean_texts([media["title"]])[0]
                    # 2.4. Insert the preprocessed media title
                    got_media_id = media_id[0] if type(media_id) == list else media_id
                    title_check = {"id_media_aut":got_media_id, "original_text":media["title"], 
                                   "author":item["username"]}
                    title_to_insert = {"id_media_aut":got_media_id, "original_text":media["title"], 
                                       "preprocessed_text":preprocessed_title, 
                                       "author":item["username"], "date":item["date"]}
                    self.postgresdb_object.insert_data(insert_titles_query,
                          [dict(sorted(title_to_insert.items()))], [title_check])
                
                # 3. Insert the comments of the media if it's a comment analysis
                if ("comment" in analysis):
                    # Get the media id if it's not been got
                    if (len(media_id) == 0):
                        get_media_id_query = "check_test_media" if "test" in analysis else "check_media"
                        check_values = {"id_media":media["id_media"], "date":item["date"]}
                        media_id = self.postgresdb_object.get_data(get_media_id_query, check_values)
                    
                    collection = "test_comments" if "test" in analysis else "comments"
                    mongo_data = self.get_data_from_mongodb(username, social_media, collection, [(date_ini, date_fin)])
                    insert_query = "insert_test_media_comments" if "test" in analysis else "insert_media_comments"
                    got_media_id = media_id[0] if type(media_id) == list else media_id
                    for record in mongo_data:
                        for comment_item in record["comments"]:
                            # 3.1. Clean the comments
                            for comment in comment_item["texts"]:
                                prep_text = self.common_data_object.clean_texts([comment["text"]])[0]
                                # 3.2. Insert the preprocessed text
                                comment_to_insert = {"author":comment["user"], "date":item["date"],
                                                     "id_media_aut":got_media_id, "original_text":comment["text"],
                                                     "preprocessed_text":prep_text}
                                check_values = {"original_text":prep_text, "author":username, "id_media_aut":got_media_id}
                                self.postgresdb_object.insert_data(insert_query, [comment_to_insert], [check_values])
                    
    def perform_medias_evolution(self, username, analysis, social_media, 
                                 date_ini, date_fin):
        """
        Performs the Medias Evolution analysis since the beginning. The method
        will get the required user data from the Mongo database which belong to
        the provided range of dates. Then, the recovered data samples will be inserted
        in the Postgres database if they're not already. Finally, only the required
        fields will be recovered in order to perform this type of analysis and plot
        the results.

        Parameters
        ----------
        username : str
            It's the username of the user which is going to be studied.
        analysis : str
            It's the type of analysis to perform.
        social_media : str
            It's the social media source which the user data will be recovered.
        date_ini : str
            It's the initial date of the period of time to perform the analysis.
        date_fin : str
            It's the final date of the period of time to perform the analysis.

        Returns
        -------
        A dict whose keys are:
            - True if the analysis could be performed and saved in an image file.
            - The file name of the saved analysis results.
            - The ids of the inserted analysis results.
        """
        # 1. Get and insert the required medias to perform the analysis
        self.insert_media_data(username, analysis, social_media, date_ini, date_fin)
        # 2. Get only the required fields to perform the analysis
        select_query = self.analysis_postgres_select_queries[analysis]
        select_values = {"date_ini":date_ini, "date_fin":date_fin,
                         "username":username, "social_media":social_media}
        required_data = self.postgresdb_object.get_data(select_query, select_values)
        
        # 3. Perform the analysis
        analysis_results = self.data_analyzer_object.post_evolution(username, required_data)        
        insert_analysis_query = "insert_test_medias_evolution" if "test" in analysis else "insert_medias_evolution"
        inserted_analysis_ids = []
        # 4. Store the analysis results for each day or week
        for index in range(0, len(analysis_results["date"])):
            if("date" in str(type(analysis_results["date"][index]))):
                analysis_results["date"][index] = datetime.strftime(analysis_results["date"][index], "%d-%m-%Y")
    
            new_analysis_result = {"date_fin":date_fin, "date_ini":date_ini, "id_user":username+"_"+social_media,
                                   "mean_comments":analysis_results["comment_count"][index],
                                   "mean_likes":analysis_results["like_count"][index], "time":analysis_results["date"][index]}
            check_analysis_result = {"date_ini":date_ini, "date_fin":date_fin, 
                                     "id_user":username+"_"+social_media, "time":analysis_results["date"][index]}
            inserted_analysis_ids.append(self.postgresdb_object.insert_data(insert_analysis_query, [new_analysis_result], [check_analysis_result]))
        
        return inserted_analysis_ids
    
    def perform_medias_popularity(self, username, analysis, social_media, 
                                  date_ini, date_fin, population_mode="best"):
        """
        Performs the Medias Popularity analysis since the beginning. The method
        will get the required user data from the Mongo database which belong to
        the provided range of dates. Then, the recovered data samples will be inserted
        in the Postgres database if they're not already. Finally, only the required
        fields will be recovered in order to perform this type of analysis and plot
        the results.

        Parameters
        ----------
        username : str
            It's the username of the user which is going to be studied.
        analysis : str
            It's the type of analysis to perform.
        social_media : str
            It's the social media source which the user data will be recovered.
        date_ini : str
            It's the initial date of the period of time to perform the analysis.
        date_fin : str
            It's the final date of the period of time to perform the analysis..

        Returns
        -------
        A dict whose keys are:
            - True if the analysis could be performed and saved in an image file.
            - The file name of the saved analysis results.
            - The ids of the inserted analysis results.
        """
        # 1. Get and insert the required medias to perform the analysis
        self.insert_media_data(username, analysis, social_media, date_ini, date_fin)
        # 2. Get only the required fields to perform the analysis
        select_query = self.analysis_postgres_select_queries[analysis]
        select_values = {"date_ini":date_ini, "date_fin":date_fin,
                         "username":username, "social_media":social_media}
        required_data = self.postgresdb_object.get_data(select_query, select_values)
        
        # 3. Perform the analysis
        analysis_results = self.data_analyzer_object.post_popularity(username, required_data, population_mode)    
        insert_analysis_query = "insert_test_medias_popularity" if "test" in analysis else "insert_medias_popularity"
        inserted_analysis_ids = []
        # 4. Store the analysis results for each media
        for media in analysis_results:
            new_analysis_result = {"date_fin":date_fin, "date_ini":date_ini, "id_media":media[0],
                                   "id_user":username+"_"+social_media,
                                    "mean_comments":media[2], "mean_likes":media[1]}
            check_analysis_result = {"date_ini":date_ini, "date_fin":date_fin, 
                                      "id_user":username+"_"+social_media, "id_media":media[0]}
            inserted_analysis_ids.append(self.postgresdb_object.insert_data(insert_analysis_query, 
                                        [new_analysis_result], [check_analysis_result]))
        return inserted_analysis_ids
    
    def perform_sentiment_analysis(self, username, analysis, social_media, 
                                    date_ini, date_fin):
        """
        Performs the Text Sentiment analysis since the beginning. The method
        will get the required user data from the Mongo database which belong to
        the provided range of dates. Then, the recovered data samples will be inserted
        in the Postgres database if they're not already. Finally, only the required
        fields will be recovered in order to perform this type of analysis and plot
        the results.

        Parameters
        ----------
        username : str
            It's the username of the user which is going to be studied.
        analysis : str
            It's the type of analysis to perform.
        social_media : str
            It's the social media source which the user data will be recovered.
        date_ini : str
            It's the initial date of the period of time to perform the analysis.
        date_fin : str
            It's the final date of the period of time to perform the analysis..

        Returns
        -------
        A dict whose keys are:
            - True if the analysis could be performed and saved in an image file.
            - The file name of the saved analysis results.
            - The ids of the inserted analysis results.
        """
        # 1. Get and insert the required medias to perform the analysis
        self.insert_media_data(username, analysis, social_media, date_ini, date_fin)
        # 2. Get only the required fields to perform the analysis
        select_query = self.analysis_postgres_select_queries[analysis]
        select_values = {"comment_date_ini":date_ini, "comment_date_fin":date_fin,
                         "media_date_ini":date_ini, "media_date_fin":date_fin,
                         "username":username, "social_media":social_media}
        required_data = self.postgresdb_object.get_data(select_query, select_values)
        # 3. Perform the analysis
        analysis_results = self.data_analyzer_object.sentiment_analysis_text(username, required_data)   
        # 4. Store the sentiment analysis results for the analyzed texts and count
        # the number of each one as well as the average polarity
        total_sentiments = {'pos':0.0, 'neu':0.0, 'neg':0.0}
        total_degree = {'pos':0.0, 'neu':0.0, 'neg':0.0}
        if ("comment" in analysis):
            insert_analyzed_text_query = "insert_test_comment_sentiment_analysis" if "test" in analysis else "insert_comment_sentiment_analysis"
            for item in analysis_results:
                check_analyzed_text = [{"original_text":item["original_text"]}]
                self.postgresdb_object.insert_data(insert_analyzed_text_query, [item], check_analyzed_text)     
                # Count the number of sentiments and compute the average degree
                total_sentiments[item["sentiment"]] += 1
                total_degree[item["sentiment"]] += item["degree"]
        
        # Average of the polarity for each sentiment
        for key in total_degree: total_degree[key] = round(total_degree[key]/len(analysis_results), 2)
        # 5. Store the sentiment analysis results
        insert_analysis_query = "insert_test_sentiment_analysis" if "test" in analysis else "insert_sentiment_analysis"
        analysis_type = "titles" if "title" in analysis else "comments"
        new_analysis = [{"date_fin":date_fin, "date_ini":date_ini, "id_user":username+"_"+social_media,
                         "n_neg":total_sentiments["neg"], "n_neu":total_sentiments["neu"],
                         "n_pos":total_sentiments["pos"], "neg_degree":total_degree["neg"],
                         "neu_degree":total_degree["neu"], "pos_degree":total_degree["pos"],
                         "type":analysis_type}]
        check_values = [{"date_ini":date_ini, "date_fin":date_fin, 
                         "id_user":username+"_"+social_media, "type":analysis_type}]
        inserted_analysis = self.postgresdb_object.insert_data(insert_analysis_query, new_analysis, check_values)
        return inserted_analysis
    
    def perform_user_behaviours(self, username, analysis, social_media, 
                                    date_ini, date_fin):
        """
        Performs the User Behaviours analysis since the beginning. The method
        will get the identified sentiments from the provided comments in order
        to count the number of likers and haters per date. Finally, the analysis
        results will be stored and plotted in a chart.

        Parameters
        ----------
        username : str
            It's the username of the user which is going to be studied.
        analysis : str
            It's the type of analysis to perform.
        social_media : str
            It's the social media source which the user data will be recovered.
        date_ini : str
            It's the initial date of the period of time to perform the analysis.
        date_fin : str
            It's the final date of the period of time to perform the analysis.

        Returns
        -------
        A dict whose keys are:
            - True if the analysis could be performed and saved in an image file.
            - The file name of the saved analysis results.
            - The ids of the inserted analysis results.
        """
        # 1. Get the media comments as well as the authors
        get_comments_query = "test_get_comments_and_authors" if "test" in analysis else "get_comments_and_authors"
        query_values = {"comment_date_ini":date_ini, "comment_date_fin":date_fin, 
                        "media_date_ini":date_ini, "media_date_fin":date_fin,
                        "username":username, "social_media":social_media}
        recovered_comments = self.postgresdb_object.get_data(get_comments_query, query_values)
        # 2. Get the sentiments of the recovered comments
        get_sentiments_query = "test_get_comment_sentiment" if "test" in analysis else "get_comment_sentiment"
        data_to_analyze = []
        for comment in recovered_comments:
            recovered_sentiment = self.postgresdb_object.get_data(get_sentiments_query,
                                                                  {"original_text":comment[2]})
            
            if (len(recovered_sentiment) > 0):
                data_to_analyze.append({"date":comment[0].strftime("%d-%m-%Y"), "author":comment[1], 
                                        "sentiment":recovered_sentiment[0][0]})
                
        # 3. Analyze the user behaviours from the recovered analysed comments
        analysis_results = self.data_analyzer_object.user_behaviours(username, data_to_analyze)
        # 4. Insert the analysis results
        inserted_analysis = []
        insert_query = self.analysis_results_insert_queries[analysis]
        for i in range(0, len(analysis_results["date"])):
            new_analysis_results = [{"date_fin":date_fin, "date_ini":date_ini, "id_user":username+"_"+social_media,
                                     "n_haters":analysis_results["haters"][i],
                                     "n_likers":analysis_results["likers"][i],
                                     "time":analysis_results["date"][i]}]
            check_analysis_results = [{"date_ini":date_ini, "date_fin":date_fin, 
                                       "id_user":username+"_"+social_media, "time":analysis_results["date"][i]}]
            inserted_analysis.append(self.postgresdb_object.insert_data(insert_query, new_analysis_results, check_analysis_results))
        
        return inserted_analysis
    
    def format_previous_analysis(self, analysis_results, required_keys):
        """
        Preprocesses the recovered results from a previous analysis in order
        to plot them.

        Parameters
        ----------
        analysis_results : list of tuples
            It's the list which contains the previous analysis results in tuples.
        required_keys : list of str
            It's the list of metrics to preprocess in order to plot them for
            a specific analysis.

        Returns
        -------
        A dict which contains the analysis results separately.
        """
        formated_analysis_results = {key:[] for key in required_keys}
        for record in analysis_results:
            for i in range(0, len(required_keys)):
                formated_analysis_results[required_keys[i]].append(record[i])
        
        return formated_analysis_results
        
    def perform_analysis(self, username, analysis, social_media, date_ini, 
                         date_fin, population_mode="best"):
        """
        Performs the provided analysis by getting the required user data from the
        provided social media source between a specific period of time. There are
        three different cases:
            - Perform the analysis since the beginning because there aren't any
            similar analysis to reuse.
            - Show the analysis results directly because the current analysis
            has been performed previously.

        Parameters
        ----------
        username : str
            It's the username of the user which is going to be studied.
        analysis : str
            It's the type of analysis to perform.
        social_media : str
            It's the social media source which the user data will be recovered.
        date_ini : str
            It's the initial date of the period of time to perform the analysis.
        date_fin : str
            It's the final date of the period of time to perform the analysis.
        mode : str
            It's the type of order to sort the medias for the Medias Popularity analysis.

        Raises
        ------
        UsernameNotFound
            If the provided username is not a non-empty string.
        InvalidAnalysis
            If the provided analysis is not a non-empty string or does not exist.
        InvalidSocialMediaSource
            If the provided social media source is not a non-empty string or does
            not exist.
        InvalidDates
            If the provided range of dates is not two non-empty strings or the range
            is invalid.

        Returns
        -------
        A dict whose first key represents the state of the analysis, if it could
        be done or if it couldn't, and whose second key is the path and file name
        in which the analysis has been stored as an image.
        """
        # Check the provided username
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")
        # Check the provided analysis to perform
        if (type(analysis) != str or analysis == ""):
            raise InvalidAnalysis("ERROR. The analysis to perform should be a non-empty string.")
        # Check if the provided analysis exists
        if (not analysis in self.data_analyzer_object.avalaible_analysis):
            raise InvalidAnalysis("ERROR. The specified analysis does not exist.")
        
        # Check the provided social media source
        if (type(social_media) != str or social_media == ""):
            raise InvalidSocialMediaSource("ERROR. The social media source should be a non-empty string.")
        if (social_media.lower() not in self.common_data_object.social_media_sources):
            raise InvalidSocialMediaSource("ERROR. The provided social media is wrong.")
        
        # Check the provided range of dates
        if (type(date_ini) != str or date_ini == "" or len(date_ini) != 10
            or type(date_fin) != str or date_fin == "" or len(date_fin) != 10):
            raise InvalidDates("ERROR. The range of date should be two non-empty strings.")
        # Check if the range of dates is valid
        try:
            date_ini_datetime = datetime.strptime(date_ini, "%d-%m-%Y")
            date_fin_datetime = datetime.strptime(date_fin, "%d-%m-%Y")
        except:
            raise InvalidDates("ERROR. The range of date have a not valid format.")

        # Check that the initial date is lower than the final date
        if (date_ini_datetime >= date_fin_datetime):
            raise InvalidDates("ERROR. Invalid range of dates. The initial is greater than the final.")
        
        if ("profile_evolution" in analysis):
            analysis_values = {"date_ini":date_ini, "date_fin":date_fin, "id_user":username+"_"+social_media}
            previous_analysis = self.postgresdb_object.get_data(analysis, analysis_values)
            # 1. Check if the analysis have been performed before
            if (len(previous_analysis) > 0):
                return self.format_previous_analysis(previous_analysis, 
                              ["date", "n_followers", "n_followings", "n_medias"])
            # 2. Perform the analysis since the beginning
            return self.perform_profile_evolution(username, analysis, social_media, date_ini, date_fin)
        
        elif ("profile_activity" in analysis):
            analysis_values = {"date_ini":date_ini, "date_fin":date_fin, "id_user":username+"_"+social_media}
            previous_analysis = self.postgresdb_object.get_data(analysis, analysis_values)
            # 1. Check if the analysis have been performed before
            if (len(previous_analysis) > 0):
                return self.format_previous_analysis(previous_analysis, ["date", "n_medias"])
            # 2. Perform the analysis since the beginning
            return self.perform_profile_activity(username, analysis, social_media, date_ini, date_fin)
        
        elif ("media_evolution" in analysis):
            analysis_values = {"date_ini":date_ini, "date_fin":date_fin, "id_user":username+"_"+social_media}
            previous_analysis = self.postgresdb_object.get_data(analysis, analysis_values)
            # 1. Check if the analysis have been performed before
            if (len(previous_analysis) > 0):
                return self.format_previous_analysis(previous_analysis, 
                              ['date', 'like_count', 'comment_count'])
            # 2. Perform the analysis since the beginning
            return self.perform_medias_evolution(username, analysis, social_media, date_ini, date_fin)
        
        elif ("media_popularity" in analysis):
            analysis_values = {"date_ini":date_ini, "date_fin":date_fin, "id_user":username+"_"+social_media}
            previous_analysis = self.postgresdb_object.get_data(analysis, analysis_values)
            # 1. Check if the analysis have been performed before
            if (len(previous_analysis) > 0):
                # Compute the final metric to sort the medias
                formated_analysis = [round((int(item[0])+int(item[1]))/2) for item in previous_analysis]
                # Sort the medias according to the provided type of analysis
                formated_analysis.sort(reverse=True if population_mode == "best" else False)
                return formated_analysis[:10]
            
            # 2. Perform the analysis since the beginning
            return self.perform_medias_popularity(username, analysis, social_media, date_ini, date_fin)
        
        elif ("sentiment" in analysis):
            analysis_values = {"date_ini":date_ini, "date_fin":date_fin, "id_user":username+"_"+social_media}
            previous_analysis = self.postgresdb_object.get_data(analysis, analysis_values)
            # 1. Check if the analysis have been performed before
            if (len(previous_analysis) > 0):
                return {"sentiments":list(previous_analysis[0][0:3]), 
                        "degrees":list(previous_analysis[0][3:])}
            # 2. Perform the analysis since the beginning
            return self.perform_sentiment_analysis(username, analysis, social_media, date_ini, date_fin)
        
        elif ("user_behaviours" in analysis):
            analysis_values = {"date_ini":date_ini, "date_fin":date_fin, "id_user":username+"_"+social_media}
            previous_analysis = self.postgresdb_object.get_data(analysis, analysis_values)
            if (len(previous_analysis) > 0):
                return self.format_previous_analysis(previous_analysis, ["date", "likers", "haters"])
            # 2. Perform the analysis since the beginning
            return self.perform_user_behaviours(username, analysis, social_media, date_ini, date_fin)
            
# if __name__ == "__main__":
#     obj = MainOperations()
#     import time
#     start = time.time()
#     result = obj.perform_analysis("audispain", "profile_evolution", "Instagram", "27-10-2020", "14-12-2020")
#     end = time.time()
    # print("TIME : ",end - start)
    # import time
    # start = time.time()
    # obj = MainOperations()
    # user_data = obj.get_user_instagram_common_data("carlosriosq", 'real')
    # end = time.time()
    # print("\nTIME: ", end - start)