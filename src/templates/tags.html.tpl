{% extends "partials/layout_full.html.tpl" %}{% block title %}Tags{% endblock %}{% block name %}Tags :: {{ tag }}{% endblock %}{% block content %}    <div class="images">        {% for _media in media %}            <a href="{{ _media.link }}">                <img src="{{ _media.images.standard_resolution.url }}" height="320" width="320" />            </a>        {% endfor %}    </div>{% endblock %}
