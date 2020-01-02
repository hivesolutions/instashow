#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Instashow System
# Copyright (c) 2008-2020 Hive Solutions Lda.
#
# This file is part of Hive Instashow System.
#
# Hive Instashow System is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Instashow System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Instashow System. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import sys
import time
import shelve
import threading
import traceback

import flask

import quorum

from . import base
from . import printer
from . import storage

SLEEP_TIME = 10.0
""" The amount of time the loop should sleep between
iterations in the scheduler loop """

QUOTA_USER = 10
""" The quota for each user, meaning the maximum
number of prints per username """

class Scheduler(threading.Thread):
    """
    Scheduler class that handles all the processing
    of the printing of images contained in certain
    tags from time to time.

    This process should be able to control excessive
    user usage and should target certain tags only.
    """

    global_lock = threading.RLock()
    """ The global lock object that constrains the step
    execution to one at a time per process, avoiding
    unwanted behavior """

    def __init__(self, tag, access_token, quota = QUOTA_USER, initial = 0, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)

        self.tag = tag
        self.access_token = access_token
        self.max_quota = quota
        self.initial = initial

    def run(self):
        threading.Thread.run(self)

        # opens the shelve based data file that is going to be used
        # to store the information regarding the printing scheduler
        self.data = shelve.open("sched.shelve", protocol = 2, writeback = True)

        try:
            # sets the running flag to true and start the iteration
            # based on the flag, running a step of the iteration
            # process for each loop, and in each of them sleeps
            # the process for a while
            self.running = True
            while self.running:
                Scheduler.global_lock.acquire()
                try: self.step()
                except Exception: traceback.print_exc(file = sys.stdout)
                finally: Scheduler.global_lock.release()
                time.sleep(SLEEP_TIME)
        finally:
            # closes the data file, flushing the pending contents to
            # the file (avoids data corruption)
            self.data.close()

    def step(self):
        # retrieves the various elements from the data repository
        # dictionary, these elements are going to be used in the
        # processing of the step operation
        printed = self.data.get("printed", [])
        quotas = self.data.get("quotas", {})

        # retrieves the recent media objects for the
        # selected tag, this should provide the basis
        # for the iteration tick operation
        api = base.get_api(access_token = self.access_token)
        media = api.media_tag(self.tag)

        # iterates over the complete set of media objects
        # in order to set the printing order for them
        for _media in media:
            # retrieves the identifier of the media and
            # in case it's already presented in the printed
            # list continues (no need to execute operation)
            media_id = _media["id"]
            if media_id in printed: continue

            # retrieves the user object for the current media
            # and then uses it to retrieves the identifier of
            # the user, verifying if there's enough quota
            user = _media["user"]
            user_id = user["id"]
            quota = quotas.get(user_id, 0)
            if quota >= self.max_quota: continue

            # retrieves the created time value and compares it
            # with the initial value in case the value is lower
            # than the initial value the media is ignored
            created_time = _media["created_time"]
            created_time = int(created_time)
            if created_time < self.initial: continue

            # runs the print image operation in the media object
            # and then appends the media identifier to the list
            # of printed elements currently present
            printer.print_image(_media)
            printed.append(media_id)

            # updates the quota value for the user incrementing its
            # value by one, meaning that the user has one less photo
            # to be printed
            quotas[user_id] = quota + 1

        # updates the data object (repository) and the runs the
        # sync operation to flush its contents to the file
        self.data["printed"] = printed
        self.data["quotas"] = quotas
        self.data.sync()

def schedule_tag(tag, quota = QUOTA_USER, initial = 0):
    access_token = flask.session["ig.access_token"] if flask.session else None
    access_token = storage.get_value("ig.access_token", access_token)
    if not access_token: return
    quorum.debug("Starting tag scheduling for '%s'" % tag)
    scheduler = Scheduler(tag, access_token, quota = quota, initial = initial)
    scheduler.start()

def schedule_init():
    tag = quorum.conf("INSTAGRAM_SCHEDULE")
    if not tag: return
    quota = quorum.conf("INSTAGRAM_QUOTA", QUOTA_USER, cast = int)
    initial = quorum.conf("INSTAGRAM_INITIAL", 0, cast = int)
    schedule_tag(tag, quota = quota, initial = initial)
