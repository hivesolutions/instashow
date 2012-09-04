{% extends "partials/layout.html.tpl" %}{% block content %}    {% for _data in data %}        <img src="{{ _data.images.standard_resolution.url }}" />    {% endfor %}
{% endblock %}
