#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains the common data to social networks and the preprocessing
methods to verify the values of the collected data.

@author: Lidia Sánchez Mérida
"""
import sys
sys.path.append("../")
import mongodb
from exceptions import ProfileDictNotFound, UsernameNotFound, ContactsListsNotFound \
    , PostsListNotFound, PostDictNotFound, InvalidMongoDbObject, LikersListNotFound \
    , CommentsListNotFound, PostCommentNotFound, CommentDictNotFound, UserDataNotFound \
    , CollectionNotFound, InvalidSocialMediaSource, IdNotFound, DuplicatedPost

from datetime import date
from googletrans import Translator
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import emoji

class CommonData:

    def __init__(self, mongodb=None):
        """Constructor. Creates a CommonData instance with or without a MongoDB
            object initialized and connected to the Mongo database."""
        self.mongodb = mongodb
        self.social_media_sources = ['instagram']
    
    def set_mongodb_connection(self, mongodb_connection):
        """Method which receives a MongoDB object to store it in a CommonData
            object as an attribute in order to connect to the database."""
        if (type(mongodb_connection) != mongodb.MongoDB):
            raise InvalidMongoDbObject("ERROR. The connection to the MongoDB database "+
                                       "should be a MongoDB object.")
        self.mongodb = mongodb_connection
        return self.mongodb

    def preprocess_profile(self, user_profile):
        """Method which checks an user profile and the fields in the dict. If some 
            required field is not found, it'll be added with a default value.
            This behaviour allows to preprocess profiles from different social medias.
        """
        # Check the data type
        if (type(user_profile) != dict or user_profile == None):
            raise ProfileDictNotFound("ERROR. User profile should be a dict.")
        """Username has to exist because it identifiers the user."""
        if ('username' not in user_profile):
            raise UsernameNotFound("ERROR. The field 'username' is required.")
        elif (type(user_profile['username']) != str or user_profile['username'] == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")

        """Allowed fields into a user profile. """
        required_fields = ['userid', 'username', 'name', 'biography', 'gender', 'profile_pic',
          'location', 'birthday', 'date_joined', 'n_followers', 'n_followings', 'n_medias', 
          'date', 'id', 'social_media']
        """Copy of the user profile to remove non-required fields."""
        preprocessed_user_profile = {}
        for field in user_profile:
            if field in required_fields:
                preprocessed_user_profile[field] = user_profile[field]
                if user_profile[field] == None:
                    preprocessed_user_profile[field] = 'None'
        return preprocessed_user_profile

    def preprocess_contacts(self, followers, followings):
        """Method which preprocesses the list of followers and followings of a
            specific user. If some of them are empty, they will be initialized as
            empty lists."""
        # Check the data type
        if (type(followers) != list or type(followings) != list):
            raise ContactsListsNotFound("ERROR. Followers/followings should be non-empty lists.")
            
        """Followers and followings only can contain non-empty strings (usernames)."""
        validFollowers = [follower for follower in followers if type(follower) == str and follower != ""]
        validFollowings = [following for following in followings if type(following) == str and following != ""]

        return {'followers':validFollowers, 'followings':validFollowings}

    def preprocess_posts(self, posts):
        """Method which preprocesses the list of posts of a specific user. Each post
            should be a dict with its id and the number of likes and comments. Both 
            previous fields should be numbers."""
        preprocessed_posts = []
        # Check posts type
        if (type(posts) != list or posts == None):
            raise PostsListNotFound("ERROR. Posts should be a non-empty list of dicts.")
        
        id_posts_shown = []
        for post in posts:
            # Check the type of each post
            if (type(post) != dict or len(post) == 0):
                raise PostDictNotFound("ERROR. Each post should be a non-empty dict.")
            # Check the fields of each post dict
            if ('id_post' not in post or 'likes' not in post or 'comments' not in post):
                raise PostDictNotFound("ERROR. Each post should have an id and the number of "+
                                        "likes and comments.")
            # Check the type of the number of likes and comments
            if (type(post['id_post']) != str or post['id_post'] == "" or
                type(post['likes']) != int or post['likes'] < 0 or
                type(post['comments']) != int or post['comments'] < 0):
                raise ValueError("ERROR. The id of the post should be a non-emtpy "+
                                 "string, likers and comments should be positive numbers.")
            
            if (post['id_post'] in id_posts_shown):
                raise DuplicatedPost("ERROR. Each post only should appear once in the same list of posts.")
            
            """Store the preprocessed post and its id."""
            preprocessed_posts.append({'id_post':post['id_post'], 'likes':post['likes'], 'comments':post['comments']})
            id_posts_shown.append(post['id_post'])
            
        return preprocessed_posts

    def preprocess_likers(self, likers):
        """Method which preprocesses the list of likers of the posts of a specific
            user. Each item should be a tuple like (user, number of likes)."""
        # Check if the likers are in a list
        if (type(likers) != list or len(likers) == 0):
            raise LikersListNotFound("ERROR. Likers should be a non-empty list.")
        
        """Check that each item is a tuple (str, int)"""
        for record in likers:
            if (type(record) != tuple or len(record) == 0):
                raise LikersListNotFound("ERROR. Each likers should be a tuple like (user, number of likes).")
            if (type(record[0]) != str or len(record[0]) == 0 or
                type(record[1]) != int or record[1] < 0):
                raise LikersListNotFound("ERROR. Each username should be a non-empty string and the number of likes should be a positive number.")
    
        return likers

    def preprocess_comments(self, comments_list):
        """Method which preprocesses a list of comments of the posts of a specific user.
            Each one should have the id of the post and the list of comments written in it."""
        # Check the data type
        if (type(comments_list) != list or len(comments_list) == 0):
            raise CommentsListNotFound("ERROR. The comments of every post should be a non-empty list.")
        
        """Check if each post data is a dict"""
        for post in comments_list:
            if (type(post) != dict or len(post) == 0):
                raise PostCommentNotFound("ERROR. Each post data should be a non-empty dict.")
            # Check the fields of the dict
            if ('id_post' not in post or 'comments' not in post):
                raise PostCommentNotFound("ERROR. Each post data should have an id and a list of comments.")
            # Check the type of each field
            if (type(post['id_post']) != str or post['id_post'] == "" or type(post['comments']) != list):
                raise PostCommentNotFound("ERROR. The post id should be a non-empty string and the comments should be a list.")
            
            """Check the list of comment dicts. It could be empty."""
            for comment in post['comments']:
                # Check if each comment data is a dict
                if (type(comment) != dict or len(comment) == 0):
                    raise CommentDictNotFound("ERROR. Each comment should be a non-empty dict.")
                # Check the keys of the comment dict
                if ('user' not in comment or 'comment' not in comment):
                    raise CommentDictNotFound("ERROR. Each comment should have an user and their comment.")
                # Check the type of the values 
                if (type(comment['user']) != str or comment['user'] == "" or
                    type(comment['comment']) != str or comment['comment'] == ""):
                    raise CommentDictNotFound("ERROR. The user and the comment should be non-empty strings.")
        
        return comments_list

    def preprocess_user_data(self, user_data):
        """Method which preprocesses each user data using the previous methods which checl every
            type of user data such as:
                - The user profile.
                - The posts, likers and their comments.
                - The followers and followings."""
        profile = self.preprocess_profile(user_data['profile'])
        contacts = self.preprocess_contacts(followers=user_data['followers'], followings=user_data['followings'])
        posts = self.preprocess_posts(user_data['posts'])
        likers = self.preprocess_likers(user_data['likers'])
        comments = self.preprocess_comments(user_data['comments'])
        data = {'profile':profile, 'posts':posts, 'likers':likers, 'comments':comments,
                'followers':contacts['followers'], 'followings':contacts['followings']}
        return data

    def preprocess_text_comments(self, comments_list):
        """Method which preprocesses the text of the post comments in order to clean this kind
            of data to analyze them later. The next techniques will be used:
                - Translate the text to English language.
                - Transform each letter to lower-case.
                - Transform emojis to text.
                - Remove punctuation marks, stop words, numbers and non-sense words.
                
            Previously, the list of comments will preprocessed before preprocessing the text of
            the comments.
        """
        # Check the comments of each post
        preprocessed_comments = self.preprocess_comments(comments_list)
        ############# TEXT COMMENTS PREPROCESSING ###############
        """Google Translator object."""
        translator = Translator()
        """Pattern to get the stop words in English"""
        pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
        preprocessed_text_comments = []
        
        for post in preprocessed_comments:
            for comment in post['comments']:
                # Translate to English
                p_com = (translator.translate(comment['comment'], dest="en")).text
                # Lower-case
                p_com = p_com.lower()
                # Emojis to text
                p_com = emoji.demojize(p_com)
                p_com = p_com.replace(":"," ")
                p_com = ' '.join(p_com.split())
                # Remove numbers
                p_com = re.sub(r"\d+", "", p_com)
                # Remove stop words in English
                p_com = pattern.sub('', p_com)
                # Remove punctuation marks
                p_com = re.sub(r'[¡#@¿\'\"\[!#?\],.:\_\-";*]', ' ', p_com)
                # Remove non-sense words, like loose letters
                p_com = ' '.join( [w for w in p_com.split() if len(w)>1] )
                """Store the preprocessed comment text"""
                preprocessed_text_comments.append({'user':comment['user'], 'preproc_comment':p_com})
        
        return preprocessed_text_comments

    ###########################################################################
    ############################ MONGODB OPERATIONS ###########################
    def add_user_data(self, username, user_data, collection, social_media):
        """Method which inserts user data into a MongoDB collection adding three fields:
            - An id which is the provided username.
            - The current date, which along the previous field, they are the 'primary key'.
            - The social media source from the user data have been downloaded.
        
            The user data to insert should have been preprocessed previously.
        """
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. The username should be a non-empty string.")
        if (len(user_data) == 0 or type(user_data) != dict):
            raise UserDataNotFound("ERROR. The user data should be a non-empty dict.")
        if (collection == "" or type(collection) != str):
            raise CollectionNotFound("ERROR. The collection name should be a non-empty string.")
        if (type(social_media) != str or social_media == "" or social_media.lower() not in self.social_media_sources):
            raise InvalidSocialMediaSource("ERROR. The social media should be a non-empty string "+
                                           "a valid source: [Instagram].")
        # Check the current MongoDB object
        if (type(self.mongodb) != mongodb.MongoDB):
                raise InvalidMongoDbObject("ERROR. The connection to the MongoDB database "+
                                       "should be a MongoDB object.")

        """Stores user data in the specified collection of a Mongo database."""
        # Primary keys: (user id, date)
        user_data['id'] = username
        user_data['date'] = (date.today()).strftime("%d-%m-%Y")
        # Social media data source
        user_data['social_media'] = social_media
        # Update the collection
        self.mongodb.set_collection(collection)

        return [self.mongodb.insert(user_data), user_data]

    def get_user_data(self, username):
        """Method which makes queries to a MongoDB collection in order to get
            all of records from a specific username."""
        if (type(username) != str or username == ""):
            raise UsernameNotFound("You should specify a valid username.")
        # Check the MongoDB object
        if (type(self.mongodb) != mongodb.MongoDB):
                raise InvalidMongoDbObject("ERROR. The connection to the MongoDB database "+
                                       "should be a MongoDB object.")
        userData = self.mongodb.get_item_records('id', username)
        if (userData == None or len(userData) == 0):
            raise IdNotFound("The specified username doesn't exist in the database.")

        return userData