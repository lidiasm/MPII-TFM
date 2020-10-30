#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains the specific exceptions for the project.

@author: Lidia Sánchez Mérida
"""
################################## CLASS API ##################################
class InvalidCredentials(Exception):
    """Class exception to point out that the provided credentials are wrong."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class UsernameNotFound(Exception):
    """Class exception to point out that the provided profile is not right."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class MaxRequestsExceed(Exception):
    """Class exception to point out that the maximum requests to the API has been
        exceed. You'll have to wait some time to do more."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class InvalidUserId(Exception):
    """Class exception to point out that the provided user id is not right."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class InvalidLimit(Exception):
    """Class exception to point out that the provided limit is not right."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class PostDictNotFound(Exception):
    """Class exception to point out a post should be a dict."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class PostListNotFound(Exception):
    """Class exception to point out that the list of profiles is not found."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class ProfileDictNotFound(Exception):
    """Class exception to point out that there's not profile."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
############################## CLASS COMMONDATA ###############################
class ValuesNotFound(Exception):
    """Class exception to point out that there is not a list of values to analyze."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class KeysNotFound(Exception):
    """Class exception to point out that there is not a list of keys to analyze."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class ExpectedSameSize(Exception):
    """Class exception to point out that the provided data have not the same size."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class InvalidSocialMediaSource(Exception):
    """Class exception to point out that the provided social media source is wrong."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class InvalidMongoDbObject(Exception):
    """Class exception to point out that the provided MongoDB object is not found."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class ContactDictNotFound(Exception):
    """Class exception to point out that the dict of contacts don't exist."""
    def __init__(self, mensaje):
        self.mensaje = mensaje        
        
class InvalidMediaId(Exception):
    """Class exception to point out that the media id is not found or is invalid."""
    def __init__(self, mensaje):
        self.mensaje = mensaje 
        
class MediaListNotFound(Exception):
    """Class exception to point out that the list of media from an user account
    doesn't exist."""
    def __init__(self, mensaje):
        self.mensaje = mensaje   

class MediaDictNotFound(Exception):
    """Class exception to point out that the provided media is not a dict."""
    def __init__(self, mensaje):
        self.mensaje = mensaje   

class LikerListNotFound(Exception):
    """Class exception to point out that likers should be a list."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class LikerDictNotFound(Exception):
    """Class exception to point out that each liker should be in a dict."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class TextListNotFound(Exception):
    """Class exception to point out that the list of texts from medias is not valid."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class TextDictNotFound(Exception):
    """Class exception to point out that the texts from a media are not dicts."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class UserDataNotFound(Exception):
    """Class exception to point out that there aren't any user data."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class InvalidTextList(Exception):
    """Class exception to point out that the provided list of texts is not right"""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
############################### CLASS MONGODB #################################
class ConnectionNotFound(Exception):
    """Class exception to point out that the connection to the database doesn't exist."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class CollectionNotFound(Exception):
    """Class exception to point out that the current collection doesn't exist."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class NewItemNotFound(Exception):
    """Class exception to point out that the new item to insert doesn't exist."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class InvalidDatabaseCredentials(Exception):
    """Class exception to point out that the provided credentials to connect to
        some database are wrong."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class InvalidQuery(Exception):
    """Class exception to point out that the provided query is wrong"""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
############################ CLASS POSTGRESQL #############################
class InvalidDatabaseConditions(Exception):
    """Class exception to point out that the provided conditions to make the query
    in the SQL database are wrong."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class InvalidTableName(Exception):
    """Class exception to point out that the provided table name is not valid."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class InvalidQueryValues(Exception):
    """Class exception to point out that the provided values to make the query
    is not valid."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
############################ CLASS DATAANALYZER #############################        
class InvalidLinePlotData(Exception):
    """Class exception to point out that the data provided to draw a line plot
    is wrong."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class InvalidBarPlotData(Exception):
    """Class exception to point out that the data provided to draw a bar plot
    is wrong."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class InvalidPiePlotData(Exception):
    """Class exception to point out that the data provided to draw a pie chart
    is wrong."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class ProfilesNotFound(Exception):
    """Class exception to point out that the list of profiles to analyze is not found"""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class UserActivityNotFound(Exception):
    """Class exception to point out that the user activity to analyze is not found"""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class PostInteractionsNotFound(Exception):
    """Class exception to point out that there is not list of post interactions to analyze."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class PostPopularityNotFound(Exception):
    """Class exception to point out that there is not list of post popularity to analyze."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class TextTupleNotFound(Exception):
    """Class exception to point out that the provided list of texts is not a 
    list of tuples."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

############################ CLASS MAINOPERATIONS #############################
class InvalidMode(Exception):
    """Class exception to point out that the provided mode is not valid."""
    def __init__(self, mensaje):
        self.mensaje = mensaje