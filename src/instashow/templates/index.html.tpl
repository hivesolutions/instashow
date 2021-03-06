{% extends "partials/layout_full.html.tpl" %}
{% block title %}Home{% endblock %}
{% block name %}Instashow{% endblock %}
{% block content %}
    <div class="images">
        {% for _media in media %}
            {% if _media.link %}
                <a href="{{ _media.link }}">
                    <img src="{{ _media.images.standard_resolution.url }}" height="320" width="320" />
                </a>
            {% else %}
                <img src="{{ _media.images.standard_resolution.url }}" height="320" width="320" />
            {% endif %}
        {% endfor %}
    </div>
{% endblock %}
