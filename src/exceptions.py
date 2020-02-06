#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains the specific exceptions for the project.

@author: Lidia Sánchez Mérida
"""
class ProfileNotFound(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje

class BasicProfileDataNotFound(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
