#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains the common data to social networks and the preprocessing
methods to verify the values of the collected data.

@author: Lidia Sánchez Mérida
"""
import sys
sys.path.append("../")
from exceptions import ProfileDictNotFound, UsernameNotFound, ContactsListsNotFound \
    , LikersListNotFound, IdNotFound, PostsDictNotFound, CommentsDictNotFound \
    , UserDataNotFound, CollectionNotFound, InvalidSocialMediaSource

from datetime import date
from googletrans import Translator
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import emoji

class CommonData:

    def __init__(self, mongodb, user_data={}):
        """Constructor. You can create an instance from this class using two different ways.
            1) Only passing the database object to connect to it and sending queries.
            2) Also passing the user data to preprocess and insert them to the database."""
        self.mongodb = mongodb
        self.user_data = user_data

    def preprocess_profile(self):
        """Check the values of the profile and the fields on it. If there isn't some
            mandatory field, it'll be added with default value."""
        if ('profile' in self.user_data):
            user_profile = self.user_data['profile']
            """Check the type."""
            if (type(user_profile) != dict or user_profile == None):
                raise ProfileDictNotFound("ERROR. User profile should be a dict.")
            """Username has to exist because it identifiers the user."""
            if ('username' not in user_profile):
                raise UsernameNotFound("Username not provided.")
            elif (user_profile['username'] == None or user_profile['username'] == ""):
                raise UsernameNotFound("Username not provided.")

            """Mandatory fields"""
            required_fields = ['userid', 'username', 'name', 'biography', 'gender', 'profile_pic',
              'location', 'birthday', 'date_joined', 'n_followers', 'n_followings']
            """Copy of the user profile to remove not required fields."""
            preprocessed_user_profile = {}
            for field in user_profile:
                if field in required_fields:
                    preprocessed_user_profile[field] = user_profile[field]
                    if user_profile[field] == None:
                        preprocessed_user_profile[field] = 'None'
            return preprocessed_user_profile
        else:
            raise ProfileDictNotFound("ERROR. User profile not provided.")

    def preprocess_contacts(self):
        """Checks the followers/followings of an user. If there aren't, both lists
            will be initialized as empty lists."""
        user_followers = []
        user_followings = []
        if ('followers' in self.user_data): user_followers = self.user_data['followers']
        if ('followings' in self.user_data): user_followings = self.user_data['followings']
        """Check types."""
        if (type(user_followers) != list or user_followers == None or
            type(user_followings) != list or user_followings == None):
            raise ContactsListsNotFound('ERROR. Followings and followers should be lists.')

        """Removes 'None' followings/followers."""
        validFollowers = [follower for follower in user_followers if follower is not None]
        validFollowings = [following for following in user_followings if following is not None]

        return {'followers':validFollowers, 'followings':validFollowings}

    def preprocess_posts(self):
        """Checks the user posts provdided."""
        posts = {}
        if ('posts' in self.user_data):
            posts = self.user_data['posts']
            """Check type"""
            if (type(posts) != dict or posts == None):
                raise PostsDictNotFound("ERROR. Posts should be a dict.")
            """Check likers and comments fields. They should be integers."""
            for id_post in posts:
                if (id_post == None or id_post == "" or type(id_post) != str):
                    raise IdNotFound("ERROR. Invalid id post.")
                try:
                    int(posts[id_post]['likes'])
                    int(posts[id_post]['comments'])
                    posts[id_post]['likes'] = str(posts[id_post]['likes'])
                    posts[id_post]['comments'] = str(posts[id_post]['comments'])
                except ValueError:
                    raise ValueError("ERROR. Likers and comments should be numbers.")
        return posts

    def preprocess_likers(self):
        """Checks if there are some posts. If there are, then it checks the people
            who like them."""
        if ('posts' in self.user_data):
            likers = []
            if ('likers' in self.user_data):
                likers = self.user_data['likers']
            """Check type."""
            if (type(likers) != list or likers == None):
                raise LikersListNotFound("ERROR. Likers should be a list.")

            return likers
        else:
            raise PostsDictNotFound("There aren't any posts so likers can't be analyzed.")

    def preprocess_comments(self):
        """Checks if there are some posts. If there are, then it checks the comments
            on them."""
        if ('posts' in self.user_data):
            comments = {}
            if ('comments' in self.user_data):
                comments = self.user_data['comments']
            """Check type."""
            if (type(comments) != dict or comments == None):
                raise CommentsDictNotFound("ERROR. Post comments should be a list.")

            return comments
        else:
            raise PostsDictNotFound("There aren't any posts so their comments can't be analyzed.")

    def preprocess_user_data(self):
        """Checks all user data using the previous methods which preprocess each
            type of user data such as the profile, posts, likers, comments, and so on."""
        profile = self.preprocess_profile()
        data = {'profile':profile}
        contacts = self.preprocess_contacts()
        posts = self.preprocess_posts()
        likers = self.preprocess_likers()
        comments = self.preprocess_comments()
        data = {'profile':profile, 'posts':posts, 'likers':likers, 'comments':comments,
                'followers':contacts['followers'], 'followings':contacts['followings']}
        return data

    def preprocess_text_comments(self):
        """Preprocesses the text of the post comments in order to clean this kind
            of data to analyze them later. The next techniques will be used:
                - Translate the text to English language.
                - Remove punctuation marks, stop words, numbers and non-sense words.
                - Transform each letter to lower-case.
                - Transform emojis to text."""
        # Check if there are comments
        if ('comments' in self.user_data):
            comments = self.user_data['comments']
            if (type(comments) != dict or len(comments) == 0):
                raise CommentsDictNotFound("ERROR. Post comments should be a non-empty list.")

            preprocessed_comments = []
            """Google Translator object."""
            translator = Translator()
            """Pattern to get the stop words in English"""
            pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
            for post in comments:
                for comment in comments[post]:
                    # Translate to English
                    p_com = (translator.translate(comment['comment'], dest="en")).text
                    # Lower-case
                    p_com = p_com.lower()
                    # Remove numbers
                    p_com = re.sub(r"\d+", "", p_com)
                    # Remove stop words in English
                    p_com = pattern.sub('', p_com)
                    # Remove punctuation marks
                    p_com = re.sub(r'[¡#@¿\'\"\[!#?\],.:";*]', '', p_com)
                    # Remove non-sense words, like loose letters
                    p_com = ' '.join( [w for w in p_com.split() if len(w)>1] )
                    # Emojis to text
                    p_com = emoji.demojize(p_com)
                    p_com = p_com.replace(":"," ")
                    p_com = ' '.join(p_com.split())
                    """Store the preprocessed comment text"""
                    preprocessed_comments.append({'user':comment['user'], 'preproc_comment':p_com})

            return preprocessed_comments
        else:
            raise CommentsDictNotFound("ERROR. There aren't any comments to preprocess.")

    ###########################################################################
    ############################ MONGODB OPERATIONS ###########################
    def add_user_data(self, username, user_data, collection, social_media):
        """Inserts user data into a MongoDB collection adding three fields:
            - An id which is the username.
            - The current date, which along the previous field, they are the 'primary key'.
            - The social media source from the user data have been downloaded."""
        if (type(username) != str or username == ""):
            raise UsernameNotFound("ERROR. Invalid username.")
        if (len(user_data) == 0 or type(user_data) != dict):
            raise UserDataNotFound("ERROR. There aren't any user data to store.")
        if (collection == "" or type(collection) != str):
            raise CollectionNotFound("ERROR. Invalid collection name.")
        if (type(social_media) != str or social_media == ""):
            raise InvalidSocialMediaSource("ERROR. Invalid social media source.")

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
        """Gets all rows related to a username from a collection."""
        if (type(username) != str or username == ""):
            raise UsernameNotFound("You should specify a valid username.")

        userData = self.mongodb.get_item_records('id', username)
        if (userData == None or len(userData) == 0):
            raise IdNotFound("The specified username doesn't exist in the database.")

        return userData