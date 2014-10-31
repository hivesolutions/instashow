{% extends "partials/layout_full.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "show" %}
            <a href="{{ url_for('show_photo', id = media.id) }}" class="active">show</a>
        {% else %}
            <a href="{{ url_for('show_photo', id = media.id) }}">show</a>
        {% endif %}
        //
        {% if sub_link == "print" %}
            <a href="{{ url_for('print_photo', id = media.id) }}" class="active">print</a>
        {% else %}
            <a href="{{ url_for('print_photo', id = media.id) }}">print</a>
        {% endif %}
    </div>
{% endblock %}
