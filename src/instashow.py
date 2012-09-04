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

import os
import json
import flask
import urllib
import urllib2
import datetime

SECRET_KEY = "ibyzsCBsaAydjIPgZKegzKOxngdImyMh"
""" The "secret" key to be at the internal encryption
processes handled by flask (eg: sessions) """

CLIENT_ID = "78ccf26cf6724f18840d078afc1ed591"
""" The id of the instagram client to be used """

CLIENT_SECRET = "b4104e1376c041129519f92db0785a40"
""" The secret key value to be used to access the
instagram api as the client """

BASE_URL = "https://api.instagram.com/"
""" The base url to be used to compose the various
complete url values for the various operations """

app = flask.Flask(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(31)

@app.route("/", methods = ("GET",))
@app.route("/index", methods = ("GET",))
def index():
    url = _ensure_token()
    if url: return flask.redirect(url)

    url = BASE_URL + "v1/media/popular"
    contents_s = _get_data(url)
    media = contents_s.get("data", [])

    return flask.render_template(
        "index.html.tpl",
        media = media
    )

@app.route("/oauth", methods = ("GET",))
def oauth():
    code = flask.request.args.get("code", None)

    url = BASE_URL + "oauth/access_token"
    values = {
        "client_id" : CLIENT_ID,
        "client_secret" : CLIENT_SECRET,
        "grant_type" : "authorization_code",
        "redirect_uri" : "http://localhost:5000/oauth",
        "code" : code
    }

    contents_s = _post_data(url, values, authenticate = False)
    access_token = contents_s["access_token"]
    flask.session["access_token"] = access_token

    return flask.redirect(
        flask.url_for("index")
    )

@app.route("/subscribe/<tag>", methods = ("GET",))
def subscribe(tag):
    url = BASE_URL + "v1/subscriptions/"
    values = {
        "client_id" : CLIENT_ID,
        "client_secret" : CLIENT_SECRET,
        "object" : "tag",
        "aspect" : "media",
        "object_id" : tag,
        "callback_url" : "http://hivespeed.dyndns.org:5005/notify"
    }

    contents_s = _post_data(url, values, authenticate = False)
    print contents_s

    return flask.redirect(
        flask.url_for("index")
    )

@app.route("/notify", methods = ("GET", "POST"))
def notify():
    if flask.request.method == "GET":
        chalenge = flask.request.args.get("hub.challenge", None)
        return chalenge
    else:
        print "notificacao !!!!"
        return ""

@app.route("/tags/<tag>", methods = ("GET",))
def tags(tag):
    url = _ensure_token()
    if url: return flask.redirect(url)

    url = BASE_URL + "v1/tags/%s/media/recent" % tag
    contents_s = _get_data(url)
    media = contents_s.get("data", [])

    return flask.render_template(
        "tags.html.tpl",
        tag = tag,
        media = media
    )

@app.errorhandler(404)
def handler_404(error):
    return str(error)

@app.errorhandler(413)
def handler_413(error):
    return str(error)

@app.errorhandler(BaseException)
def handler_exception(error):
    return str(error)

def _get_data(url, values = None, authenticate = True):
    values = values or {}
    if authenticate: values["access_token"] = flask.session["access_token"]
    data = urllib.urlencode(values)
    url = url + "?" + data
    response = urllib2.urlopen(url)
    contents = response.read()
    contents_s = json.loads(contents)
    return contents_s

def _post_data(url, values = None, authenticate = True):
    values = values or {}
    if authenticate: values["access_token"] = flask.session["access_token"]
    data = urllib.urlencode(values)
    request = urllib2.Request(url, data)
    response = urllib2.urlopen(request)
    contents = response.read()
    contents_s = json.loads(contents)
    return contents_s

def _ensure_token():
    access_token = flask.session.get("access_token", None)
    if access_token: return None

    url = BASE_URL + "oauth/authorize/"
    values = {
        "client_id" : CLIENT_ID,
        "redirect_uri" : "http://localhost:5000/oauth",
        "response_type" : "code"
    }

    data = urllib.urlencode(values)
    url = url + "?" + data
    return url

def run():
    # sets the debug control in the application
    # then checks the current environment variable
    # for the target port for execution (external)
    # and then start running it (continuous loop)
    debug = os.environ.get("DEBUG", False) and True or False
    reloader = os.environ.get("RELOADER", False) and True or False
    port = int(os.environ.get("PORT", 5000))
    app.debug = debug
    app.secret_key = SECRET_KEY
    app.run(
        use_debugger = debug,
        debug = debug,
        use_reloader = reloader,
        host = "0.0.0.0",
        port = port
    )

if __name__ == "__main__":
    run()
