#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains the specific exceptions for the project.

@author: Lidia Sánchez Mérida
"""
class ProfileNotFound(Exception):
    """Class exception to point out that there's not profile."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class BasicProfileDataNotFound(Exception):
    """Class exception to point out that the provided profile is not right."""
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
        
class EmptyCollection(Exception):
    """Class exception to point out that the current collection is empty."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
    
class ItemNotFound(Exception):
    """Class exception to point out that the specific item doesn't exist."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class SingletonClass(Exception):
    """Class exception to point out that the class API is a singleton class."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class InvalidCredentials(Exception):
    """Class exception to point out that the provided credentials are wrong."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class MaxRequestsExceed(Exception):
    """Class exception to point out that the maximum requests to the API has been
        exceed. You'll have to wait some time to do more."""
    def __init__(self, mensaje):
        self.mensaje = mensaje

class UsernameNotFound(Exception):
    """Class exception to point out that the username specified doesn't exist."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class RelathionshipsListNotFound(Exception):
    """Class exception to point out that the lists of followers and followings 
        don't exist."""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class LikersListNotFound(Exception):
    """Class exception to point out that likers should be a list."""
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