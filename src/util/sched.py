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
from instashow import BASE_URL

SLEEP_TIME = 1.0
""" The amount of time the loop should sleep between
iterations in the scheduler loop """

class Scheduler(threading.Thread):
    """
    Scheduler class that handles all the processing
    of the printing of images contained in certain
    tags from time to time.

    This process should be able to control excessive
    user usage and should target certain tags only.
    """

    def __init__(self, tag, access_token, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)

        self.tag = tag
        self.access_token = access_token

    def run(self):
        threading.Thread.run(self)
        
        self.data = shelve.open("C:/tobias.schelve")

        try:
            self.running = True
            while self.running: self.iterate(); time.sleep(SLEEP_TIME)
        finally:
            self.data.close()

    def iterate(self):
        printed = self.data.get("printed", [])
        
        url = BASE_URL + "v1/tags/%s/media/recent" % self.tag
        contents_s = quorum.get_json(url, access_token = self.access_token)
        media = contents_s.get("data", [])

        for _media in media:
            media_id = _media["id"]
            if media_id in printed: continue
            printed.append(media_id)
            print media_id
            
def schedule_tag(tag):
    access_token = flask.session["instashow.access_token"]
    scheduler = Scheduler(tag, access_token)
    scheduler.start()
