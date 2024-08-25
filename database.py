<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TomyVet</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <nav>
        <ul>
            <li><a href="{{ url_for('home') }}">Home</a></li>
            <li><a href="{{ url_for('dashboard') }}">Dashboard</a></li>
            <li><a href="{{ url_for('animales') }}">Animales</a></li>
            <li><a href="{{ url_for('appointments') }}">Citas</a></li>
            <li><a href="{{ url_for('inventory') }}">Inventario</a></li>
            <li><a href="{{ url_for('invoices') }}">Facturas</a></li>
            {% if 'username' in session %}
                <li><a href="{{ url_for('logout') }}">Logout</a></li>
            {% else %}
                <li><a href="{{ url_for('login') }}">Iniciar Sesión</a></li>
                <li><a href="{{ url_for('register') }}">Registrar</a></li>
            {% endif %}
        </ul>
    </nav>
    <main>
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            <ul class="flashes">
            {% for category, message in messages %}
              <li class="{{ category }}">{{ message }}</li>
            {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </main>
    <footer>
        Derechos de autor © Estudiante Pablo Abarca Tala de la Universidad Andres Bello
    </footer>
</body>
</html>
