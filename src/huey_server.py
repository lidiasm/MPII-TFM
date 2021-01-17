#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File which includes the automatic and periodic tasks to download data of a specific
user and from a particular social media source.

@author: Lidia Sánchez Mérida
"""
from huey import SqliteHuey, crontab
huey = SqliteHuey(filename='/tmp/huey_sqlite.db')

from main_ops import MainOperations

@huey.periodic_task(crontab(day='*/1', hour='19'))
def get_user_data():
    """
    Function to download the data of a specific user from the selected social media
    source every day at 7 o'clock.
    """
    mainops_object = MainOperations()
    collected_data = {}
    if (mainops_object.social_media_source.lower() == "instagram"):
        collected_data = mainops_object.get_user_instagram_common_data(mainops_object.user_to_study, "real")

    return collected_data

