#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class which contains the common data to social networks and the preprocessing
methods to verify the values of the collected data.

@author: Lidia Sánchez Mérida
"""
import sys
sys.path.append("../")
from exceptions import ProfileNotFound, BasicProfileDataNotFound

class CommonData:
    
    def __init__(self, profileUser, followers, following):
        self.profileUser = profileUser
        self.followers = followers
        self.following = following
    
    def check_profile_field(self, field):
        field_value = None
        """Check if the field exists."""
        if (field in self.profileUser):
            """Check the value of the field."""
            if (field == None): self.profileUser[field] = "None"
            else: field_value = self.profileUser[field]
        else:
            self.profileUser[field] = "None"
            
        return field_value
            
    def profile_preprocessing(self):
        name_value = self.check_profile_field('name')
        username_value = self.check_profile_field('username')
        email_value = self.check_profile_field('email')
        self.check_profile_field('biography')
        self.check_profile_field('gender')
        self.check_profile_field('profile_pic')
        self.check_profile_field('location')
        self.check_profile_field('birthday')
        self.check_profile_field('data_joined')
        self.check_profile_field('private_account')
        """To string."""
        if (self.profileUser['private_account'] == True): self.profileUser['private_account'] = 'Yes'
        elif (self.profileUser['private_account'] == False): self.profileUser['private_account'] = 'No'
        
        if (name_value == None or username_value == None or email_value == None):
            raise BasicProfileDataNotFound("Basic profile data not found.")
                    
        return self.profileUser
    
    def preprocessing(self):
        """Check the provided profile."""
        if (self.profileUser == None or len(self.profileUser) == 0): raise ProfileNotFound("Profile not provided")
        self.profileUser = self.profile_preprocessing()
        """Check the followers and following fields."""
        if (self.followers == None): self.followers = {}
        if (self.following == None): self.following = {}
        data = {'profile':self.profileUser, 'followers':self.followers, 'following':self.following}
        return data