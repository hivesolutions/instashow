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
import hashlib
import datetime

import extras

SECRET_KEY = "dzhneqksmwtuinay5dfdljec19pi765p"
""" The "secret" key to be at the internal encryption
processes handled by flask (eg: sessions) """

PASSWORD_SALT = "cameria"
""" The salt suffix to be used during the encoding
of the password into an hash value """

CURRENT_DIRECTORY = os.path.dirname(__file__)
CURRENT_DIRECTORY_ABS = os.path.abspath(CURRENT_DIRECTORY)
SETS_FOLDER = os.path.join(CURRENT_DIRECTORY_ABS, "sets")
CAMERAS_FOLDER = os.path.join(CURRENT_DIRECTORY_ABS, "cameras")
DEVICES_FOLDER = os.path.join(CURRENT_DIRECTORY_ABS, "devices")
SETTINGS_FOLDER = os.path.join(CURRENT_DIRECTORY_ABS, "settings")

app = flask.Flask(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(31)

@app.route("/", methods = ("GET",))
@app.route("/index", methods = ("GET",))
@extras.ensure("index")
def index():
    return flask.render_template(
        "index.html.tpl",
        link = "home"
    )

@app.route("/signin", methods = ("GET",))
def signin():
    return flask.render_template(
        "signin.html.tpl"
    )

@app.route("/signin", methods = ("POST",))
def login():
    # retrieves both the username and the password from
    # the flask request form, these are the values that
    # are going to be used in the username validation
    username = flask.request.form.get("username", None)
    password = flask.request.form.get("password", None)

    # retrieves the structure containing the information
    # on the currently available users and unpacks the
    # various attributes from it (defaulting to base values)
    users = get_users()
    user = users.get(username, None)
    _password = user.get("password", None)

    # encodes the provided password into an sha1 hash appending
    # the salt value to it before the encoding
    password_sha1 = hashlib.sha1(password + PASSWORD_SALT).hexdigest()

    # checks that both the user structure and the password values
    # are present and that the password matched, if one of these
    # values fails the login process fails and the user is redirected
    # to the signin page with an error string
    if not user or not _password or not password_sha1 == _password:
        return flask.render_template(
            "signin.html.tpl",
            username = username,
            error = "Invalid user name and/or password"
        )

    # retrieves the tokens and cameras sequence from the user to set
    # them in the current session
    tokens = user.get("tokens", ())
    cameras = user.get("cameras", None)

    # updates the current user (name) in session with
    # the username that has just be accepted in the login
    flask.session["username"] = username
    flask.session["tokens"] = tokens
    flask.session["cameras"] = cameras

    # makes the current session permanent this will allow
    # the session to persist along multiple browser initialization
    flask.session.permanent = True

    return flask.redirect(
        flask.url_for("index")
    )

@app.route("/signout", methods = ("GET", "POST"))
def logout():
    if "username" in flask.session: del flask.session["username"]
    if "tokens" in flask.session: del flask.session["tokens"]
    if "cameras" in flask.session: del flask.session["cameras"]

    return flask.redirect(
        flask.url_for("signin")
    )

@app.route("/about", methods = ("GET",))
@extras.ensure("about")
def about():
    return flask.render_template(
        "about.html.tpl",
        link = "about"
    )

@app.route("/sets", methods = ("GET",))
@extras.ensure("sets.list")
def list_set():
    sets = get_sets()
    sets = extras.ensure_sets_f(sets)

    return flask.render_template(
        "sets_list.html.tpl",
        link = "sets",
        sets = sets
    )

@app.route("/sets/<id>", methods = ("GET",))
@extras.ensure("sets.show")
def show_set(id):
    set = get_set(id)
    cameras = set.get("cameras", [])
    extras.ensure_cameras(cameras)

    return flask.render_template(
        "sets_show.html.tpl",
        link = "sets",
        sub_link = "show",
        set = set
    )

@app.route("/sets/<id>/settings", methods = ("GET",))
@extras.ensure("sets.settings")
def settings_set(id):
    set = get_set(id)

    return flask.render_template(
        "sets_settings.html.tpl",
        link = "sets",
        sub_link = "settings",
        set = set
    )

@app.route("/cameras", methods = ("GET",))
@extras.ensure("cameras.list")
def list_camera():
    cameras = get_cameras()
    cameras = extras.ensure_cameras_f(cameras)

    return flask.render_template(
        "cameras_list.html.tpl",
        link = "cameras",
        cameras = cameras
    )

@app.route("/cameras/<id>", methods = ("GET",))
@extras.ensure("cameras.show")
def show_camera(id):
    camera = get_camera(id)
    filter(camera)
    extras.ensure_camera(camera)

    return flask.render_template(
        "cameras_show.html.tpl",
        link = "cameras",
        sub_link = "show",
        camera = camera
    )

@app.route("/cameras/<id>/settings", methods = ("GET",))
@extras.ensure("cameras.settings")
def settings_camera(id):
    camera = get_camera(id)
    extras.ensure_camera(camera)

    return flask.render_template(
        "cameras_settings.html.tpl",
        link = "cameras",
        sub_link = "settings",
        camera = camera
    )

@app.route("/devices", methods = ("GET",))
@extras.ensure("devices.list")
def list_device():
    devices = get_devices()

    return flask.render_template(
        "devices_list.html.tpl",
        link = "devices",
        devices = devices
    )

@app.route("/device/<id>", methods = ("GET",))
@extras.ensure("devices.show")
def show_device(id):
    device = get_device(id = id)

    return flask.render_template(
        "devices_show.html.tpl",
        link = "devices",
        sub_link = "show",
        device = device
    )

@app.route("/user/<username>", methods = ("GET",))
@extras.ensure("users.show")
def show_user(username):
    user = get_user(username = username)
    username = user["username"]
    extras.ensure_user(username)

    return flask.render_template(
        "users_show.html.tpl",
        link = "users",
        sub_link = "show",
        user = user
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

def get_users():
    users_path = os.path.join(SETTINGS_FOLDER, "users.json")
    if not os.path.exists(users_path): raise RuntimeError("Users file does not exist")
    users_file = open(users_path, "rb")
    try: users = json.load(users_file)
    finally: users_file.close()

    return users

def get_user(username):
    users = get_users()
    user = users.get(username, None)
    if not user: raise RuntimeError("User '%s' not found" % username)

    return user

def get_sets():
    sets_directory = os.path.join(SETS_FOLDER)
    if not os.path.exists(sets_directory): raise RuntimeError("Sets directory does not exist")
    entries = os.listdir(sets_directory)
    entries.sort()

    sets = []

    for entry in entries:
        base, extension = os.path.splitext(entry)
        if not extension == ".json": continue

        set = get_set(base)
        sets.append(set)

    return sets

def get_set(id):
    # retrieves the path to the (target) set (configuration) file and
    # check if it exists then opens it and loads the json configuration
    # contained in it to set it in the template
    set_path = os.path.join(SETS_FOLDER, "%s.json" % id)
    if not os.path.exists(set_path): raise RuntimeError("Set file does not exist")
    set_file = open(set_path, "rb")
    try: set = json.load(set_file)
    finally: set_file.close()

    cameras = set.get("cameras", [])
    _camera = set.get("camera", {})

    for camera in cameras:
        id = camera["id"]
        __camera = get_camera(id)

        merge(camera, __camera)
        merge(camera, _camera)

        filter(camera)

    return set

def get_cameras():
    cameras_directory = os.path.join(CAMERAS_FOLDER)
    if not os.path.exists(cameras_directory): raise RuntimeError("Cameras directory does not exist")
    entries = os.listdir(cameras_directory)
    entries.sort()

    cameras = []

    for camera in entries:
        base, extension = os.path.splitext(camera)
        if not extension == ".json": continue

        camera = get_camera(base)
        cameras.append(camera)

    return cameras

def get_camera(id):
    camera_path = os.path.join(CAMERAS_FOLDER, "%s.json" % id)
    if not os.path.exists(camera_path): raise RuntimeError("Camera file does not exist")
    camera_file = open(camera_path, "rb")
    try: camera = json.load(camera_file)
    finally: camera_file.close()

    return camera

def get_devices():
    devices_directory = os.path.join(DEVICES_FOLDER)
    if not os.path.exists(devices_directory): raise RuntimeError("Devices directory does not exist")
    entries = os.listdir(devices_directory)
    entries.sort()

    devices = []

    for device in entries:
        base, extension = os.path.splitext(device)
        if not extension == ".json": continue

        type, model = base.split("_", 1)

        device = get_device(type, model)
        devices.append(device)

    return devices

def get_device(type = None, model = None, id = None):
    id = id or "%s_%s" % (type, model)
    device_path = os.path.join(DEVICES_FOLDER, "%s.json" % id)
    if not os.path.exists(device_path): raise RuntimeError("Device file does not exist")
    device_file = open(device_path, "rb")
    try: device = json.load(device_file)
    finally: device_file.close()

    return device

def merge(first, second, override = True):
    for key, value in second.items():
        if key in first and not override: continue
        first[key] = value

def filter(camera):
    type = camera.get("type", "axis")
    model = camera.get("model", "211")

    device = get_device(type, model)
    _camera = device.get("camera", {})
    settings = device.get("settings", {})

    merge(camera, _camera, override = False)

    for key, value in settings.items():
        if value: continue
        if not key in camera: continue
        del camera[key]

def run():
    # sets the debug control in the application
    # then checks the current environment variable
    # for the target port for execution (external)
    # and then start running it (continuous loop)
    debug = os.environ.get("DEBUG", False) and True or False
    reloader = os.environ.get("RELOADER", False) and True or False
    port = int(os.environ.get("PORT", 5000))
    not debug and extras.SSLify(app)
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