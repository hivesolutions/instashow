{% extends "partials/layout_full.html.tpl" %}{% block title %}Index{% endblock %}{% block name %}Index{% endblock %}{% block content %}    <div class="images">        {% for _data in data %}            <img src="{{ _data.images.standard_resolution.url }}" height="320" width="320" />        {% endfor %}    </div>
{% endblock %}
