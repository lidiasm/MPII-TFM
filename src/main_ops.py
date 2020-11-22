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
    , InvalidDates, CollectionNotFound, InvalidQuery, InvalidAnalysisResults

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
            'test_title_sentiment_analysis':'test_medias',
            
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
            "test_title_sentiment_analysis":"insert_test_medias",
            
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
            "test_profile_activity":"test_get_profiles_activity",
            "test_media_evolution":"test_get_medias",
            "test_media_popularity":"test_get_medias_popularity",
            "test_comment_sentiment_analysis":"test_get_media_comment",
            "test_title_sentiment_analysis":"test_get_media_title_for_sentiment",
            
            "profile_evolution":"get_profiles",
            "profile_activity":"get_profiles_activity",
            "media_evolution":"get_medias",
            "media_popularity":"get_medias_popularity",
            "comment_sentiment_analysis":"get_media_comment",
            "title_sentiment_analysis":"get_media_title_for_sentiment",
        }
        # Postgre insert queries to add the analysis results
        self.analysis_results_insert_queries = {
            "test_profile_evolution":"insert_test_profile_evolution",
            "test_profile_activity":"insert_test_profile_activity",
            "test_media_evolution":"insert_test_medias_evolution",
            "test_media_popularity":"insert_test_medias_popularity",
            "test_comment_sentiment_analysis":"insert_test_sentiment_analysis",
            "test_title_sentiment_analysis":"insert_test_title_sentiment_analysis",
            
            "profile_evolution":"insert_profile_evolution",
            "profile_activity":"insert_profile_activity",
            "media_evolution":"insert_medias_evolution",
            "media_popularity":"insert_medias_popularity",
            "comment_sentiment_analysis":"insert_sentiment_analysis",
            "title_sentiment_analysis":"insert_title_sentiment_analysis",
        }
        # Postgre insert queries to add the data sample which have participated
        # in each analysis
        self.analysis_ids_insert_queries = {
            "test_profile_evolution":"insert_test_profile_test_profile_evolution",
            "test_profile_activity":"insert_test_profile_test_profile_activity",
            "test_media_evolution":"insert_test_medias_test_medias_evolution",
            "test_media_popularity":"insert_test_medias_test_medias_popularity",
            
            "profile_evolution":"insert_profile_profile_evolution",
            "profile_activity":"insert_profile_profile_activity",
            "media_evolution":"insert_medias_medias_evolution",
            "media_popularity":"insert_medias_medias_popularity",
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
    
    def insert_data_to_postgres(self, query, user_data):
        """
        Inserts new user data into a specific table in the Postgres database if
        the data samples are not already in the database. In order to check that,
        the method will create the values to check if each data sample already exists
        before it's added.

        Parameters
        ----------
        query : str
            It's the insert query to make in the Postgres database.
        user_data : list of dicts
            It's the new data to insert in a specific table in the Postgres database.

        Raises
        ------
        InvalidQuery
            If the provided query is not a non-empty string or does not exist.
        UserDataNotFound
            If the provided user data to add is not a non-empty list of dicts.

        Returns
        -------
        True if all data samples could be inserted, False if some of them couldn't.
        """
        # Check the provided query
        if (type(query) != str or query == ""):
            raise InvalidQuery("ERROR. The insert query should be a non-empty string.")
        # Check the provided data to insert
        if (type(user_data) != list or len(user_data) == 0 or
            not (all(isinstance(item, dict) for item in user_data))):
            raise UserDataNotFound("ERROR. The user data should be a non-empty list of dicts.")
        
        # Values to check if the new data to insert are already in the database
        postgres_check_values = []
        postgres_insert_values = []
        check_keys = []
        check_query = None
        if (query in self.postgresdb_object.check_queries):
            check_query = self.postgresdb_object.check_queries[query]
            check_keys = self.postgresdb_object.select_queries[check_query]["fields"]
        
        # Particular case for query 'check_test_media'
        if (check_query == "check_test_media" or check_query == "check_media"):
            media_results = []
            for item in user_data:
                for media in item["medias"]:
                    postgres_check_values = []
                    postgres_insert_values = []
                    media_check = {"id_media":media["id_media"], "date":item["date"]}
                    # Add the checks for each data sample
                    postgres_check_values.append(media_check)
                    # Separate each media 
                    media_to_insert = {"id_media":media["id_media"],
                                       "id_profile":item["id_profile"],
                                       "like_count":media["like_count"],
                                       "comment_count":media["comment_count"],
                                       "date":item["date"],
                                       "uploaded_date":media["taken_at"]}
                    
                    # Add the data to insert in a specific order
                    postgres_insert_values.append(dict(sorted(media_to_insert.items())))
                    media_id = self.postgresdb_object.insert_data(query, postgres_insert_values, postgres_check_values)
                    media_results.append(media_id)
                    # The media could be already inserted
                    if (len(media_id) == 0):
                        select_values = [{"id_media":media["id_media"], "date":item["date"]}]
                        found_media = self.get_data_from_postgresdb(check_query, select_values)
                        media_id = found_media["ids"]
                    # Insert the titles too if the media have one
                    if (media["title"] != None and len(media_id) > 0):
                        postgres_check_values = []
                        postgres_insert_values = []
                        got_media_id = media_id[0] if type(media_id) == list else media_id
                        title_to_insert = {"id_media_aut":got_media_id, "text":media["title"], 
                                           "author":item["username"], "date":item["date"]}
                        # Add the data to the related table
                        postgres_insert_values.append(dict(sorted(title_to_insert.items())))
                        # Add the check values
                        check_values = {"id_media_aut":got_media_id, "text":media["title"], 
                                        "author":item["username"]}
                        postgres_check_values.append(check_values)
                        title_query = "insert_test_media_titles" if "test" in query else "insert_media_titles"
                        title_id = self.postgresdb_object.insert_data(title_query, postgres_insert_values, postgres_check_values)
                        media_results.append(title_id)
                        
            return media_results
        elif ("comments" in query):
            comment_results = []
            # Insert each comment of each media
            for record in user_data:
                for media in record["comments"]:
                    for comment in media["texts"]:
                        comment_to_insert = {"id_media_aut":media["id_media_aut"], "date":record["date"],
                                             "author":comment["user"], "text":comment["text"]}
                        values_to_check = {"text":comment["text"], "author":comment["user"], "id_media_aut":media["id_media_aut"]}
                        comment_results.append(self.postgresdb_object.insert_data(query, 
                              [dict(sorted(comment_to_insert.items()))], [values_to_check]))
                
            return comment_results
        else:
            results = []
            for item in user_data:
                # Get the check values
                if (len(check_keys) > 0):
                    item_check = {}
                    for key in check_keys:
                        item_check[key] = item[key]
                    # Add the new element
                    results.append(self.postgresdb_object.insert_data(query, [dict(sorted(item.items()))], [item_check]))
                else:
                    # Add the new element
                    results.append(self.postgresdb_object.insert_data(query, [dict(sorted(item.items()))]))
                    
            return results
        
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
    
    def insert_media_popularity_results(self, date_ini, date_fin, analysis, analysis_results):
        """
        Inserts the results from the Medias Popularity analysis in a different way.
        Each analysis result is related to a different studied post during a specific
        period of time. This analysis could have more than one result on the same
        range of dates, so there won't be any check query to make previously.

        Parameters
        ----------
        date_ini : str
            It's the initial date of the performed analysis.
        date_fin : str
            It's the final date of the performed analysis.
        analysis : str
            It's the performed analysis name.
        analysis_results : dict
            It's the dict which contains the ids from the involved data samples
            under the 'ids' key, as well as the analysis results under the 'data' key.

        Raises
        ------
        InvalidAnalysisResults
            If the provided analysis results are not in a non-empty dict or don't
            have the 'ids' and 'data' keys.

        Returns
        -------
        A dict whose first key is the list of inserted analysis ids, and whose second
        key is the list of the inserted relationships ids.
        """
        # Check the provided analysis results
        if (type(analysis_results) != list or len(analysis_results) == 0 or
            not all(isinstance(item, tuple) for item in analysis_results)):
            raise InvalidAnalysisResults("ERROR. The post popularity results should be a non-empty list of tuples.")
        
        list_analysis_ids = []
        list_relationships_ids = []
        # Get the insert query
        insert_results_query = self.analysis_results_insert_queries[analysis]
        insert_ids_query = self.analysis_ids_insert_queries[analysis]
        for media in analysis_results:
            # Insert the analysis results for each different media
            user_data = [{"date_fin":date_fin, "date_ini":date_ini,
                          "mean_likes":media[1], "mean_comments":media[2]}]
            analysis_id = self.insert_data_to_postgres(insert_results_query, user_data)
        
            if (len(analysis_id) > 0):
                analysis_id = analysis_id[0][0]
                list_analysis_ids.append(analysis_id)
                # Insert the relationships between each media from each date and the
                # related analysis
                medias_ids = []
                for idd in media[0]:
                    medias_ids.append({"id_media_aut":idd, "id_media_popularity":analysis_id})
                # Insert the ids
                list_relationships_ids.append(self.insert_data_to_postgres(insert_ids_query, medias_ids))
        
        return {"id":list_analysis_ids, "relationships":list_relationships_ids}
    
    def top_ten_medias_popularity(self, username, date_ini, date_fin, social_media, analysis, analysis_results):
        """
        Gets the top ten of the best and worst medias from a specific user based
        on the average of likes and comments during the provided period of time.
        The media data to plot will be:
            - Title/Content of the media.
            - The date in which the media was uploaded.
            - The studied range of dates.
            - The average of likes during that period of time.
            - The average of comments during that period of time.

        Parameters
        ----------
        username : str
            It's the owner user of the medias.
        social_media : str
            It's the social media source which the medias came from.
        date_ini : str
            It's the initial date of the performed analysis.
        date_fin : str
            It's the final date of the performed analysis.
        analysis : str
            It's the performed analysis name.
        analysis_results : dict
            It's the dict which contains the ids from the involved data samples
            under the 'ids' key, as well as the analysis results under the 'data' key.


        Raises
        ------
        InvalidAnalysisResults
            If the provided analysis results are not a non-empty list of tuples.

        Returns
        -------
        A dict whose first values are the top ten of the best medias according to
        the specific metrics, and whose second values are the top ten of the worst
        medias.
        """
        # Check the provided analysis results
        if (type(analysis_results) != list or len(analysis_results) == 0 or
            not all(isinstance(item, tuple) for item in analysis_results)):
            raise InvalidAnalysisResults("ERROR. The post popularity results should be a non-empty list of tuples.")
        
        # Sort the posts to choose the best and the worst TOP 10 by likes and comments
        medias = {i:round((analysis_results[i][1]+analysis_results[i][2])/2) for i in range(0, len(analysis_results))}
        worst_sorted_medias = {k: v for k, v in sorted(medias.items(), key=lambda item: item[1])}
        best_sorted_medias = {k: v for k, v in sorted(medias.items(), key=lambda item: item[1], reverse=True)}
        # Complete the BEST TOP 10
        best_top_ten = []
        top_ten_keys = list(best_sorted_medias.keys())[:10]
        for key in top_ten_keys:
            # If it's an Instagram post, get the title
            if (social_media.lower() == "instagram"):
                # Get the title
                query_title = "test_get_media_title" if "test" in analysis else "get_media_title"
                values = [{"id_media_aut":analysis_results[key][0][0], "author":username}]
                title = self.get_data_from_postgresdb(query_title, values)
                # Get the uploaded date
                query_date = "test_get_medias_for_popularity" if "test" in analysis else "get_medias_for_popularity"
                date_values = [{"id_media_aut":analysis_results[key][0][0]}]
                uploaded_date = self.get_data_from_postgresdb(query_date, date_values)
                format_uploaded_date = datetime.strptime(uploaded_date["data"][0][0], 
                                                         '%Y-%m-%d').strftime('%d-%m-%Y')
                best_top_ten.append((title["data"][0][0], format_uploaded_date, 
                     date_ini, date_fin, analysis_results[key][1], analysis_results[key][2]))
        
        worst_top_ten = []
        worst_ten_keys = list(worst_sorted_medias.keys())[:10]
        for key in worst_ten_keys:
            # If it's an Instagram post, get the title
            if (social_media.lower() == "instagram"):
                # Get the title
                query_title = "test_get_media_title" if "test" in analysis else "get_media_title"
                values = [{"id_media_aut":analysis_results[key][0][0], "author":username}]
                title = self.get_data_from_postgresdb(query_title, values)
                # Get the uploaded date
                query_date = "test_get_medias_for_popularity" if "test" in analysis else "get_medias_for_popularity"
                date_values = [{"id_media_aut":analysis_results[key][0][0]}]
                uploaded_date = self.get_data_from_postgresdb(query_date, date_values)
                format_uploaded_date = datetime.strptime(uploaded_date["data"][0][0], 
                                                         '%Y-%m-%d').strftime('%d-%m-%Y')
                worst_top_ten.append((title["data"][0][0], format_uploaded_date, 
                     date_ini, date_fin, analysis_results[key][1], analysis_results[key][2]))
        
        return {"best":best_top_ten, "worst":worst_top_ten}
    
    def insert_many_analysis_results(self, date_ini, date_fin, analysis, analysis_results):
        """
        Inserts the results from a performed analysis as well as the relationships
        between the data sample which have participated in the analysis and itself
        in the related Postgres tables.

        Parameters
        ----------
        date_ini : str
            It's the initial date of the performed analysis.
        date_fin : str
            It's the final date of the performed analysis.
        analysis : str
            It's the performed analysis name.
        analysis_results : dict
            It's the dict which contains the ids from the involved data samples
            under the 'ids' key, as well as the analysis results under the 'data' key.

        Raises
        ------
        InvalidAnalysisResults
            If the provided analysis results are not in a non-empty dict or don't
            have the 'ids' and 'data' keys.

        Returns
        -------
        A dict which contains the analysis id under the 'id' key as well as
        the relationships ids under the 'relationships' key from the involved
        data samples.
        """
        # Check the provided analysis results
        if (type(analysis_results) != dict or len(analysis_results) == 0):
            raise InvalidAnalysisResults("ERROR. The analysis results should be a non-empty dict.")
        if ('ids' not in analysis_results or 'data' not in analysis_results):
            raise InvalidAnalysisResults("ERROR. The analysis results should have 'ids' and 'data' keys.")
        
        # 1. Prepare and insert the analysis data 
        analysis_data = analysis_results["data"]
        analysis_data = dict(sorted(analysis_data.items()))
        # Delete the "date" key because it's useless
        del analysis_data["date"]
        # Compute the average of all the weeks for each key
        analysis_values = [date_fin, date_ini]
        for key in analysis_data:
            int_values = [int(value) for value in analysis_data[key]]
            analysis_values.append(round(sum(int_values) / len(int_values)))
        
        # Turn the list of values to a dict with the provided insert query keys
        insert_results_query = self.analysis_results_insert_queries[analysis]
        result_fields = self.postgresdb_object.insert_queries[insert_results_query]["fields"]
        analysis_data_dict = dict(zip(result_fields, analysis_values))
        
        # Insert the analysis result to its related table in the Postgres database
        insert_data_query = self.analysis_results_insert_queries[analysis]
        analysis_id = self.insert_data_to_postgres(insert_data_query, [analysis_data_dict])
        #### IMPORTANT!!!
        # If the analysis couldn't be inserted, then the method can't continue
        if (type(analysis_id) != list or len(analysis_id[0]) == 0):
            raise InvalidAnalysisResults("ERROR. The analysis results couldn't be inserted.")        
        
        analysis_id = [float(x) for [x] in analysis_id]
        # 2. Insert the relationship between the inserted analysis and the data samples
        # which have participated.
        relationship_ids = []
        if (analysis in self.analysis_ids_insert_queries):
            insert_ids_query = self.analysis_ids_insert_queries[analysis]
            ids_fields = self.postgresdb_object.insert_queries[insert_ids_query]["fields"]
            analysis_ids_list = []
            for idd in analysis_results["ids"]:
                data_sample_id = idd[0] if type(idd) == list else idd
                analysis_ids_list.append(dict(zip(ids_fields, [data_sample_id, analysis_id[0]])))
            # Insert the data ids
            insert_ids_query = self.analysis_ids_insert_queries[analysis]
            relationship_ids = self.insert_data_to_postgres(insert_ids_query, analysis_ids_list)
        
        return {"id":analysis_id, "relationships":relationship_ids}
            
    def perform_analysis(self, username, analysis, social_media, date_ini, date_fin):
        """
        Performs the provided analysis by getting the required user data from the
        provided social media source between a specific period of time. There are
        three different cases:
            - Perform the analysis since the beginning because there aren't any
            similar analysis to reuse.
            - Perform a partial analysis because there is a similar analysis stored
            in the database which will help to perform the current faster. This situation
            will only be considered if the period of time is more than 7 days.
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
            It's the final date of the period of time to perform the analysis..

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
        
        # 1. Check if some similar analysis have been performed for the user
        values = {"date_ini":date_ini, "date_fin":date_fin, "username":username, "social_media":social_media}
        if ("sentiment" in analysis):
            values = {"media_date_ini":date_ini, "media_date_fin":date_fin, 
                      "comment_date_ini":date_ini, "comment_date_fin":date_fin, 
                      "username":username, "social_media":social_media}
        if ("users" not in analysis):
            previous_analysis = self.postgresdb_object.get_data(analysis, values)
            select_query = None
            select_values = None
            # Yes, there are some previous analysis
            # if (len(previous_analysis) > 0):
            #     # Pick the most suitable to the current analysis by dates
            #     # Find the missing dates in order to get that data from Mongo database
            #     print("yes")
            # # No, there aren't any similar previous analysis
            # else:
            # Get all the required data from the related Mongo collection
            collection = self.analysis_mongo_collections[analysis]
            mongo_data = self.get_data_from_mongodb(username, social_media, collection, [(date_ini, date_fin)])
        
        analysis_copy = analysis
        # Get the profile id if it's a medias analysis
        media_analysis = ["media_evolution", "test_media_evolution",
                          "media_popularity", "test_media_popularity",
                          "test_title_sentiment_analysis", "title_sentiment_analysis"]
        if (analysis in media_analysis):
            # Prepare the query and the values to get the required data
            select_query = self.analysis_postgres_select_queries[analysis]
            select_values = [{"date_ini":date_ini, "date_fin":date_fin,
                              "username":username, "social_media":social_media}]
            for item in mongo_data:
                check_query = "check_test_profile" if "test" in analysis else "check_profile"
                postgres_data = self.get_data_from_postgresdb(check_query, 
                   [{"username":username, "social_media":social_media, "date":item["date"].strftime("%Y-%m-%d")}])                    
                item["id_profile"] = postgres_data["ids"][0]
                # Preprocess the title of each media
                for media in item["medias"]:
                    # Clean the title
                    media["title"] = self.common_data_object.clean_texts([media["title"]])[0]
            # For Title Sentiment Analysis
            if ("sentiment" in analysis):
                select_values = [{"comment_date_ini":date_ini, "comment_date_fin":date_fin,
                              "media_date_ini":date_ini, "media_date_fin":date_fin,
                              "username":username, "social_media":social_media}]
        elif ("comment" in analysis or "users" in analysis):
            analysis = "comment_sentiment_analysis" if "test" not in analysis_copy else "test_comment_sentiment_analysis"
            # Prepare the query and the values to get the required data
            select_query = self.analysis_postgres_select_queries[analysis]
            select_values = [{"comment_date_ini":date_ini, "comment_date_fin":date_fin,
                              "media_date_ini":date_ini, "media_date_fin":date_fin,
                              "username":username, "social_media":social_media}]
            
            # In the first place, the medias will be inserted
            collection = "test_medias" if "test" in analysis else "medias" 
            mongo_medias = self.get_data_from_mongodb(username, social_media, collection, [(date_ini, date_fin)])
            for item in mongo_medias:
                check_query = "check_test_profile" if "test" in analysis else "check_profile"
                postgres_data = self.get_data_from_postgresdb(check_query, 
                   [{"username":username, "social_media":social_media, "date":item["date"].strftime("%Y-%m-%d")}])                    
                item["id_profile"] = postgres_data["ids"][0]
            # Insert the Mongo data to the related Postgres table
            insert_query = "insert_test_medias" if "test" in analysis else "insert_medias"
            self.insert_data_to_postgres(insert_query, mongo_medias)
            
            # Get the comments for that dates
            collection = "test_comments" if "test" in analysis else "comments" 
            mongo_data = self.get_data_from_mongodb(username, social_media, collection, [(date_ini, date_fin)])
            for record in mongo_data:
                for item in record["comments"]:
                    check_query = "check_test_medias_for_comment" if "test" in analysis else "check_medias_for_comment"
                    postgres_data = self.get_data_from_postgresdb(check_query, 
                       [{"id_media":item["id_media"], "date":record["date"].strftime("%Y-%m-%d"), "username":username, "social_media":social_media}])                    
                    item["id_media_aut"] = postgres_data["ids"][0]
                    # Clean the comment texts
                    # for comment in item["texts"]:
                    #     comment["text"] = self.common_data_object.clean_texts([comment["text"]])[0]
            
        else:
            # Prepare the query and the values to get the required data
            select_query = self.analysis_postgres_select_queries[analysis]
            select_values = [{"username":username, "social_media":social_media,
                             "date_ini":date_ini, "date_fin":date_fin}]
        
        # Insert the Mongo data to the related Postgres table
        insert_query = self.analysis_postgres_insert_queries[analysis]
        self.insert_data_to_postgres(insert_query, mongo_data)
            
        # Get the required data from the Postgres database to perform the specified analysis
        analysis = analysis_copy
        if ("users" in analysis):
            required_data = []
            # Get the comments id as well as the authors
            select_comments = [{"comment_date_ini":date_ini, "comment_date_fin":date_fin,
                              "media_date_ini":date_ini, "media_date_fin":date_fin,
                              "username":username, "social_media":social_media}]
            query_comments = "test_comment_users_behaviours" if "test" in analysis else "comment_users_behaviours"
            required_comments = self.get_data_from_postgresdb(query_comments, select_comments)
            # Get the sentiment for each text
            query_sentiments = "test_sentiment_users_behaviours" if "test" else "sentiment_users_behaviours"
            for index in range(0, len(required_comments["ids"])):
                select_sentiments = [{"id_text":required_comments["ids"][index]}]
                result = self.get_data_from_postgresdb(query_sentiments, select_sentiments)
                required_data.append((required_comments["data"][index][0].strftime("%d-%m-%Y"), 
                                      required_comments["data"][index][1],
                                      result["ids"][0]))
        else:
            required_data = self.get_data_from_postgresdb(select_query, select_values)

        # Perform the analysis with the got data
        analysis_results = []
        if (analysis == "profile_evolution" or analysis == "test_profile_evolution"):
            analysis_results = self.data_analyzer_object.profile_evolution(username, required_data["data"])
        elif (analysis == "profile_activity" or analysis == "test_profile_activity"):
            analysis_results = self.data_analyzer_object.user_activity(username, required_data["data"])
        elif (analysis == "media_evolution" or analysis == "test_media_evolution"):
            analysis_results = self.data_analyzer_object.post_evolution(username, required_data["data"])
        elif (analysis == "media_popularity" or analysis == "test_media_popularity"):
            analysis_results = self.data_analyzer_object.post_popularity(username, required_data) 
            self.insert_media_popularity_results(date_ini, date_fin, analysis, analysis_results)
            return self.top_ten_medias_popularity(username, date_ini, date_fin, social_media, analysis, analysis_results)
        elif ("sentiment" in analysis):
            analysis_results = self.data_analyzer_object.sentiment_analysis_text(username, required_data)
            if ("title" in analysis):
                insert_query = "insert_test_title_sentiment_analysis" if "test" in analysis else "insert_title_sentiment_analysis"
            else:
                insert_query = "insert_test_sentiment_analysis" if "test" in analysis else "insert_sentiment_analysis"
            self.insert_data_to_postgres(insert_query, analysis_results["data"])
        elif ("users" in analysis):
            analysis_results = self.data_analyzer_object.user_behaviours(username, required_data)
            
        # Insert the analysis results only if there are more than 7 days of user data
        if ("weeks" in analysis_results["file"]):
            final_result = self.insert_many_analysis_results(date_ini, date_fin, analysis,
                  {"ids":required_data["ids"], "data":analysis_results["data"]})
            return {"state":analysis_results["state"], "file":analysis_results["file"],
                    "analysis_id":final_result["id"], "samples_ids":final_result["relationships"]}
        
        return {"state":analysis_results["state"], "file":analysis_results["file"]}
        
# if __name__ == "__main__":
#     obj = MainOperations()
#     import time
#     start = time.time()
#     result = obj.perform_analysis("audispain", "title_sentiment_analysis", "Instagram", "27-10-2020", "28-10-2020")
#     end = time.time()
#     print("TIME : ",end - start)
#     import time
#     start = time.time()
#     obj = MainOperations()
#     user_data = obj.get_user_instagram_common_data("carlosriosq", 'real')
#     end = time.time()
#     print("\nTIME: ", end - start)