#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Instashow System
# Copyright (c) 2008-2016 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier
import werkzeug

from instashow import util

from instashow.main import app
from instashow.main import flask
from instashow.main import quorum

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
    flask.session.permanent = True

    util.set_value("ig.access_token", access_token)

    return flask.redirect(
        state or flask.url_for("index")
    )

@app.route("/subscribe/<tag>", methods = ("GET",))
def subscribe(tag):
    base_url = quorum.conf("BASE_URL")
    callback_url = base_url + "/notify"
    api = _get_api()
    api.subscribe(
        object = "tag",
        aspect = "media",
        object_id = tag,
        callback_url = callback_url
    )
    return flask.redirect(
        flask.url_for("index")
    )

@app.route("/unsubscribe/<tag>", methods = ("GET",))
def unsubscribe(tag):
    base_url = quorum.conf("BASE_URL")
    callback_url = base_url + "/notify"
    api = _get_api()
    api.unsubscribe(
        object = "tag",
        aspect = "media",
        object_id = tag,
        callback_url = callback_url
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

    title = quorum.conf("TITLE", "Instashow")
    sub_title = quorum.conf("SUB_TITLE", "Instagram + steroids")
    image = quorum.conf("IMAGE", None)
    timeout = quorum.get_field("timeout", 10000, cast = int)
    title = quorum.get_field("title", title)
    sub_title = quorum.get_field("sub_title", sub_title)
    image = quorum.get_field("image", image)

    api = _get_api()
    media = api.media_tag(tag)

    return flask.render_template(
        "tags/slideshow.html.tpl",
        link = "tags",
        sub_link = "slideshow",
        tag = tag,
        media = media,
        title = title,
        sub_title = sub_title,
        image = image,
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

@app.errorhandler(appier.OAuthAccessError)
def handler_oauth(error):
    if "ig.access_token" in flask.session: del flask.session["ig.access_token"]
    if "ig.user_id" in flask.session: del flask.session["ig.user_id"]
    return flask.redirect(
        flask.request.url
    )

@app.errorhandler(BaseException)
def handler_exception(error):
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
    url = flask.request.url
    url = werkzeug.iri_to_uri(url)
    return api.oauth_authorize(state = url)

def _get_api():
    access_token = flask.session and flask.session.get("ig.access_token", None)
    user_id = flask.session and flask.session.get("ig.user_id", None)
    api = util.get_api()
    api.access_token = access_token
    api.user_id = user_id
    return api
