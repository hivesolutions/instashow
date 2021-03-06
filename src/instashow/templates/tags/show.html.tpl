{% extends "partials/layout_tags.html.tpl" %}
{% block title %}Tags{% endblock %}
{% block name %}Tags :: {{ tag }}{% endblock %}
{% block content %}
    <div class="images">
        {% for _media in media %}
            <a href="{{ url_for('show_photo', id = _media.id) }}">
                <img src="{{ _media.images.standard_resolution.url }}" height="320" width="320" />
            </a>
        {% endfor %}
    </div>
{% endblock %}
