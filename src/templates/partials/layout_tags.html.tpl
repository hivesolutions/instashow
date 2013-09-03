{% extends "partials/layout_full.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "show" %}
            <a href="{{ url_for('show_tag', tag = tag) }}" class="active">show</a>
        {% else %}
            <a href="{{ url_for('show_tag', tag = tag) }}">show</a>
        {% endif %}
        //
        {% if sub_link == "slideshow" %}
            <a href="{{ url_for('slideshow_tag', tag = tag) }}" class="active">slideshow</a>
        {% else %}
            <a href="{{ url_for('slideshow_tag', tag = tag) }}">slideshow</a>
        {% endif %}
        //
        {% if sub_link == "schedule" %}
            <a href="{{ url_for('schedule_tag', tag = tag) }}" class="active">schedule</a>
        {% else %}
            <a href="{{ url_for('schedule_tag', tag = tag) }}">schedule</a>
        {% endif %}
    </div>
{% endblock %}
