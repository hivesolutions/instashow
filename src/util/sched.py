#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Instashow System
# Copyright (C) 2008-2012 Hive Solutions Lda.
#
# This file is part of Hive Instashow System.
#
# Hive Instashow System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Instashow System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Instashow System. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import time
import shelve
import threading

from instashow import flask
from instashow import quorum
from instashow import print_image
from instashow import BASE_URL

SLEEP_TIME = 10.0
""" The amount of time the loop should sleep between
iterations in the scheduler loop """

QUOTA_USER = 5
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

    def __init__(self, tag, access_token, quota = QUOTA_USER, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)

        self.tag = tag
        self.access_token = access_token
        self.max_quota = quota

    def run(self):
        threading.Thread.run(self)

        # opens the shelve based data file that is going to be used
        # to store the information regarding the printing scheduler
        self.data = shelve.open("sched.shelve")

        try:
            # sets the running flag to true and start the iteration
            # based on the flag, running a step of the iteration
            # process for each loop, and in each of them sleeps
            # the process for a while
            self.running = True
            while self.running:
                Scheduler.global_lock.acquire()
                try: self.step()
                except: pass
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
        url = BASE_URL + "v1/tags/%s/media/recent" % self.tag
        contents_s = quorum.get_json(url, access_token = self.access_token)
        media = contents_s.get("data", [])

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

            # runs the print image operation in the media object
            # and then appends the media identifier to the list
            # of printed elements currently present
            print_image(_media)
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

def schedule_tag(tag, quota = QUOTA_USER):
    access_token = flask.session["instashow.access_token"]
    scheduler = Scheduler(tag, access_token, quota = quota)
    scheduler.start()
