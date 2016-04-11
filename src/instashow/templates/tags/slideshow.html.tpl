{% extends "partials/layout_complete.html.tpl" %}
{% block title %}Tags{% endblock %}
{% block name %}Tags :: {{ tag }}{% endblock %}
{% block content %}
    <div class="instashow {{ tag }}" data-url="{{ url_for('latest_tag_json', tag = tag) }}" data-timeout="{{ timeout }}">
        <div class="initial">
            <div class="page-container">
                {% if title %}<h1>{{ title }}</h1>{% endif %}
                {% if sub_title %}<h2>{{ sub_title }}</h2>{% endif %}
                {% if image %}
                    <img class="banner" src="{{ image }}" />
                {% else %}
                    <div class="instagram"></div>
                {% endif %}
                <p>
                    Publica as tuas fotos ou vídeos no Instagram <br />
                    incluindo na descrição a hashtag:
                    <div class="hashtag">
                        <strong>#{{ tag }}</strong>
                    </div>
                </p>
                <div class="icon"></div>
            </div>
        </div>
        {% for _media in media %}
            <div class="item">
                {% if _media.type == "video" %}
                    <video src="{{ _media.videos.standard_resolution.url }}" loop="1"></video>
                {% else %}
                    <img src="{{ _media.images.standard_resolution.url }}" />
                {% endif %}
                <div class="box">
                    <div class="left">
                        <h2 class="double">{{ _media.caption.text }}</h2>
                    </div>
                    <div class="right">
                        <h2>@{{ _media.user.username }}</h2>
                        <h3>{{ _media.user.full_name }}</h3>
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
{% endblock %}
