{% extends "partials/layout_photos.html.tpl" %}
{% block title %}Photo{% endblock %}
{% block name %}Photo :: {{ media.id }}{% endblock %}
{% block content %}
    {% if media.type == "video" %}
        <div class="video">
            {% if media.link %}
                <a href="{{ media.link }}">
                    <video src="{{ media.videos.standard_resolution.url }}" autoplay="1" loop="1" />
                </a>
            {% else %}
                <video src="{{ media.videos.standard_resolution.url }}" autoplay="1" loop="1" />
            {% endif %}
        </div>
    {% else %}
        <div class="image">
            {% if media.link %}
                <a href="{{ media.link }}">
                    <img src="{{ media.images.standard_resolution.url }}" />
                </a>
            {% else %}
                <img src="{{ media.images.standard_resolution.url }}" />
            {% endif %}
        </div>
    {% endif %}
{% endblock %}
