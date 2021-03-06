{% extends "partials/layout_full.html.tpl" %}
{% block title %}Photos{% endblock %}
{% block name %}Photos{% endblock %}
{% block content %}
    <div class="images">
        {% for _media in media %}
            <a href="{{ url_for('show_photo', id = _media.id) }}">
                <img src="{{ _media.images.standard_resolution.url }}" height="320" width="320" />
            </a>
        {% endfor %}
    </div>
{% endblock %}
