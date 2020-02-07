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