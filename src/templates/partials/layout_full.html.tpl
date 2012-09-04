{% include "partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "partials/content_type.html.tpl" %}
        {% include "partials/includes.html.tpl" %}
        <title>Instashow</title>
    {% endblock %}
</head>
<body class="ux full">
    <div id="overlay"></div>
    <div id="header">
        {% block header %}
            <h1>{% block name %}{% endblock %}</h1>
            <div class="links">
                {% if link == "home" %}
                    <a href="#" class="active">home</a>
                {% else %}
                    <a href="#">home</a>
                {% endif %}
                //
                {% if link == "sets" %}
                    <a href="#" class="active">sets</a>
                {% else %}
                    <a href="#">sets</a>
                {% endif %}
                //
                {% if link == "cameras" %}
                    <a href="#" class="active">cameras</a>
                {% else %}
                    <a href="#">cameras</a>
                {% endif %}
                //
                {% if link == "devices" %}
                    <a href="#" class="active">devices</a>
                {% else %}
                    <a href="#">devices</a>
                {% endif %}
                //
                {% if link == "about" %}
                    <a href="#" class="active">about</a>
                {% else %}
                    <a href="#">about</a>
                {% endif %}
            </div>
        {% endblock %}
    </div>
    <div id="content">{% block content %}{% endblock %}</div>
    {% include "partials/footer.html.tpl" %}
</body>
{% include "partials/end_doctype.html.tpl" %}
