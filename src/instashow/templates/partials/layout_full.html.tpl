{% include "partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "partials/content_type.html.tpl" %}
        {% include "partials/includes.html.tpl" %}
        <title>Instashow</title>
    {% endblock %}
</head>
<body class="ux full">
    <div id="overlay" class="overlay"></div>
    <div id="header">
        {% block header %}
            <h1>{% block name %}{% endblock %}</h1>
            <div class="links">
                {% if link == "photos" %}
                    <a href="{{ url_for('list_photos') }}" class="active">photos</a>
                {% else %}
                    <a href="{{ url_for('list_photos') }}">photos</a>
                {% endif %}
                //
                {% if link == "tags" %}
                    <a href="{{ url_for('show_tag', tag = 'portugal') }}" class="active">tags</a>
                {% else %}
                    <a href="{{ url_for('show_tag', tag = 'portugal') }}">tags</a>
                {% endif %}
                //
                {% if link == "about" %}
                    <a href="{{ url_for('about') }}" class="active">about</a>
                {% else %}
                    <a href="{{ url_for('about') }}">about</a>
                {% endif %}
            </div>
        {% endblock %}
    </div>
    <div id="content">{% block content %}{% endblock %}</div>
    {% include "partials/footer.html.tpl" %}
</body>
{% include "partials/end_doctype.html.tpl" %}
