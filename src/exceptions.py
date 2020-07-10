#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains the specific exceptions for the project.

@author: Lidia Sánchez Mérida
"""

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

class ProfileDictNotFound(Exception):
    """Class exception to point out that there's not profile."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class ContactsListsNotFound(Exception):
    """Class exception to point out that the lists of followers and followings 
        don't exist."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class CollectionNotFound(Exception):
    """Class exception to point out that the current collection doesn't exist."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class InvalidSocialMediaSource(Exception):
    """Class exception to point out that the social media source is not right."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class NewItemNotFound(Exception):
    """Class exception to point out that the new item to insert doesn't exist."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class EmptyCollection(Exception):
    """Class exception to point out that the current collection is empty."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
    
class ItemNotFound(Exception):
    """Class exception to point out that the specific item doesn't exist."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class LikersListNotFound(Exception):
    """Class exception to point out that likers should be a list."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class CommentsDictNotFound(Exception):
    """Class exception to point out that post comments should be a list."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
                
class IdNotFound(Exception):
    """Class exception to point out that a record doesn't have an id."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class PostsDictNotFound(Exception):
    """Class exception to point out that a record doesn't have an id."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class UserDataNotFound(Exception):
    """Class exception to point out that there aren't any user data."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class TableNotFound(Exception):
    """Class exception to point out that the specified table is not right."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class DatabaseFieldsNotFound(Exception):
    """Class exception to point out that the item does not contain all the database
        fields which are required."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class InvalidFieldsToGet(Exception):
    """Class exception to point out that the fields to return in select procedures
        are not right."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class InvalidConditions(Exception):
    """Class exception to point out that the conditions for selecting some rows
        from the PostgresSQL database are not right."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class CommentsListNotFound(Exception):
    """Class exception to point out that post comments should be a list."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class SentimentAnalysisNotFound(Exception):
    """Class exception to point out that the sentiment analysis is not found."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class BehaviourAnalysisNotFound(Exception):
    """Class exception to point out that the behaviour patterns found by the
        sentiment analysis is not found."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class InvalidSentiment(Exception):
    """Class exception to point out that the specified sentiment for the behaviour
        patterns is not right."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class ProfilesListNotFound(Exception):
    """Class exception to point out that the list of profiles is not found."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class InvalidPlotData(Exception):
    """Class exception to point out that the provided data to draw some kind of plot are not right."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class InvalidPlotType(Exception):
    """Class exception to point out that the provided plot type is not right."""
    def __init__(self, mensaje):
        self.mensaje = mensaje