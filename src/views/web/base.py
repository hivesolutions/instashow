#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Instashow System
# Copyright (C) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import instagram

import util

from instashow import app
from instashow import flask
from instashow import quorum

CLIENT_ID = "78ccf26cf6724f18840d078afc1ed591"
""" The id of the instagram client to be used """

CLIENT_SECRET = "b4104e1376c041129519f92db0785a40"
""" The secret key value to be used to access the
instagram api as the client """

BASE_URL = "https://api.instagram.com/"
""" The base url to be used to compose the various
complete url values for the various operations """

REDIRECT_URL = "http://hq.hive.pt:8585/oauth"
""" The redirect base url to be used as the base value
for the construction of the base url instances """

CALLBACK_URL = "http://hq.hive.pt:8585/notify"
""" The url to be used by the instagram server to notify
the client (should be available externally) """

@app.route("/", methods = ("GET",))
@app.route("/index", methods = ("GET",))
def index():
    return list_photos()

@app.route("/about", methods = ("GET",))
def about():
    return flask.render_template(
        "about.html.tpl",
        link = "about"
    )

@app.route("/oauth", methods = ("GET",))
def oauth():
    code = quorum.get_field("code")
    state = quorum.get_field("state")

    api = _get_api()
    access_token = api.oauth_access(code)
    flask.session["ig.access_token"] = access_token
    flask.session["ig.user_id"] = api.user_id

    return flask.redirect(
        state or flask.url_for("index")
    )

@app.route("/subscribe/<tag>", methods = ("GET",))
def subscribe(tag):
    api = _get_api()
    api.subscribe(
        object = "tag",
        aspect = "media",
        object_id = tag,
        callback_url = CALLBACK_URL
    )
    return flask.redirect(
        flask.url_for("index")
    )

@app.route("/unsubscribe/<tag>", methods = ("GET",))
def unsubscribe(tag):
    api = _get_api()
    api.unsubscribe(
        object = "tag",
        aspect = "media",
        object_id = tag,
        callback_url = CALLBACK_URL
    )
    return flask.redirect(
        flask.url_for("index")
    )

@app.route("/notify", methods = ("GET", "POST"))
def notify():
    if flask.request.method == "GET":
        quorum.debug("Notification verification from instagram")
        chalenge = flask.request.args.get("hub.challenge", None)
        return chalenge
    else:
        quorum.debug("Notification received from instagram")
        return ""

@app.route("/tags/<tag>", methods = ("GET",))
def show_tag(tag):
    url = _ensure_api()
    if url: return flask.redirect(url)

    api = _get_api()
    media = api.media_tag(tag)

    return flask.render_template(
        "tags/show.html.tpl",
        link = "tags",
        sub_link = "show",
        tag = tag,
        media = media
    )

@app.route("/tags/<tag>/slideshow", methods = ("GET",))
def slideshow_tag(tag):
    url = _ensure_api()
    if url: return flask.redirect(url)

    timeout = quorum.get_field("timeout", 10000, cast = int)

    api = _get_api()
    media = api.media_tag(tag)

    return flask.render_template(
        "tags/slideshow.html.tpl",
        link = "tags",
        sub_link = "slideshow",
        tag = tag,
        media = media,
        timeout = timeout
    )

@app.route("/tags/<tag>/latest.json", methods = ("GET",), json = True)
def latest_tag_json(tag):
    url = _ensure_api()
    if url: return flask.redirect(url)

    api = _get_api()
    media = api.media_tag(tag)

    return media

@app.route("/tags/<tag>/schedule", methods = ("GET",))
def schedule_tag(tag):
    url = _ensure_api()
    if url: return flask.redirect(url)

    quota = quorum.get_field("quota", util.QUOTA_USER, int)

    util.schedule_tag(tag, quota = quota)

    return flask.redirect(
        flask.url_for("show_tag", tag = tag)
    )

@app.route("/photos", methods = ("GET",))
def list_photos():
    url = _ensure_api()
    if url: return flask.redirect(url)

    api = _get_api()
    media = api.popular_media()

    return flask.render_template(
        "photos/list.html.tpl",
        link = "photos",
        id = id,
        media = media
    )

@app.route("/photos/<id>", methods = ("GET",))
def show_photo(id):
    url = _ensure_api()
    if url: return flask.redirect(url)

    api = _get_api()
    media = api.get_media(id)

    return flask.render_template(
        "photos/show.html.tpl",
        link = "photos",
        sub_link = "show",
        id = id,
        media = media
    )

@app.route("/photos/<id>/print", methods = ("GET",))
def print_photo(id):
    url = _ensure_api()
    if url: return flask.redirect(url)

    api = _get_api()
    media = api.get_media(id)
    print_image(media)

    return flask.redirect(
        flask.url_for("show_photo", id = id)
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

@app.errorhandler(instagram.appier.OAuthAccessError)
def handler_oauth(error):
    return str(error)

def print_image(media):
    images = media.get("images", {})
    image = images.get("standard_resolution", {})
    url = image.get("url", None)
    if not url: raise RuntimeError("No url available for image")

    data = quorum.get(url)
    util.print_data(data)

def _ensure_api():
    access_token = flask.session.get("ig.access_token", None)
    if access_token: return
    api = _get_api()
    return api.oauth_authorize()

def _get_api():
    access_token = flask.session and flask.session.get("ig.access_token", None)
    user_id = flask.session and flask.session.get("ig.user_id", None)
    api = util.get_api()
    api.access_token = access_token
    api.user_id = user_id
    return api
