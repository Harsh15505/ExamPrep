# Flask Notes Application: Detailed Code Breakdown

This guide explains exactly how our Flask application works line-by-line. It's written specifically for someone who has never touched Flask before!

---

## 🚀 Setup & Run Instructions

```bash
# 1. Install Flask and Flask-SQLAlchemy (The ORM for database operations)
pip install flask flask-sqlalchemy

# 2. Open terminal in the 'notes_app' directory and run the app
python app.py

# 3. Open your browser and go to: http://127.0.0.1:5000
```

---

## 🐍 `app.py` — The Python Backend

```python
from flask import Flask, render_template, request, redirect, url_for
# render_template: Loads an HTML file and sends it to the browser.
# request: Contains all data sent from the user (like form submissions).
# redirect: Forwards the user to a different URL.
# url_for: Automatically generates a URL based on the name of a Python function.

from flask_sqlalchemy import SQLAlchemy
# Flask-SQLAlchemy is an Object Relational Mapper (ORM). 
# It lets us write Python code instead of raw SQL queries (like INSERT INTO...) to interact with our database.

app = Flask(__name__)
# Initializes the core Flask application. `__name__` is a special Python variable that tells Flask where to look for templates and static files.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
# Configuration setting: Tells SQLAlchemy to use a SQLite database named 'notes.db'. 
# The '///' means it will be created in a hidden 'instance' folder right next to app.py.

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Disables a feature that tracks every modification to the database. We turn it off because it uses a lot of memory and isn't needed.

db = SQLAlchemy(app)
# Links our SQLAlchemy instance to our Flask app.


# ==========================================
# DATABASE MODEL
# ==========================================
class Note(db.Model):
# We create a Python class that inherits from db.Model. 
# This automatically creates a table called 'note' in our database!

    id = db.Column(db.Integer, primary_key=True)
    # Creates an 'id' column. Integer type. Primary Key means it auto-increments (1, 2, 3...) and uniquely identifies a row.

    title = db.Column(db.String(100), nullable=False)
    # Creates a 'title' column. Max length 100 chars. nullable=False means it CANNOT be empty.

    content = db.Column(db.Text, nullable=False)
    # Creates a 'content' column. Text type (unlimited length). Also cannot be empty.


# ==========================================
# ROUTES (Controllers)
# ==========================================

@app.route('/')
# This is a Route Decorator. It tells Flask: "When a user visits the root URL (http://localhost:5000/), execute the function below it."
def index():
    all_notes = Note.query.all()
    # ORM Magic! This is the equivalent of "SELECT * FROM note". It fetches everything from the database and stores it in a Python list.

    return render_template('index.html', notes=all_notes)
    # Opens 'templates/index.html' and passes the list of notes to it under the variable name 'notes'.


@app.route('/add', methods=['POST'])
# This route specifically handles POST requests (which happen when a user submits an HTML form).
def add_note():
    note_title = request.form.get('title')
    note_content = request.form.get('content')
    # Extracts the data typed into the HTML input fields. 
    # 'title' and 'content' must match the `name="..."` attribute in the HTML form!

    if note_title and note_content:
        # Basic validation: ensure both aren't completely empty.

        new_note = Note(title=note_title, content=note_content)
        # Creates a new row in memory (an instance of the Note class).

        db.session.add(new_note)
        # Adds the new row to the database staging area.

        db.session.commit()
        # Permanently saves (commits) the changes to the database.

    return redirect(url_for('index'))
    # Sends the user back to the home page so they can see their newly added note.
    # url_for('index') specifically looks for the function named `index()` and generates its URL ('/').


@app.route('/delete/<int:id>')
# Dynamic Route: <int:id> acts as a variable. If the URL is /delete/5, Flask passes '5' into the `id` argument of the function.
def delete_note(id):
    note_to_delete = Note.query.get_or_404(id)
    # Equivalent to "SELECT * FROM note WHERE id = X". 
    # If the ID doesn't exist, it automatically shows a 404 Error page instead of crashing the server!

    db.session.delete(note_to_delete)
    db.session.commit()
    # Removes the row from the database and saves the change.

    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
# Accepts BOTH GET (user simply visiting the URL) and POST (user submitting the edit form).
def edit_note(id):
    note_to_edit = Note.query.get_or_404(id)
    # Fetch the specific note we want to edit.
    
    if request.method == 'POST':
        # If the user clicked "Update Note" (submitting the form)...
        
        note_to_edit.title = request.form.get('title')
        note_to_edit.content = request.form.get('content')
        # We simply update the properties of the Python object with the new form data.
        
        db.session.commit()
        # We DON'T need db.session.add() here because the object is already in the database. We just commit the changes.
        
        return redirect(url_for('index'))
        
    return render_template('edit.html', note=note_to_edit)
    # If it's a GET request, load the edit page and pass the specific note to it so we can pre-fill the input fields.


# ==========================================
# SERVER BOOTSTRAP
# ==========================================
if __name__ == "__main__":
# This checks if the script is being run directly (e.g., `python app.py`) rather than being imported elsewhere.

    with app.app_context():
        db.create_all()
        # Crucial Step! This looks at our `Note` class and actually creates the SQLite database file and tables if they don't exist yet.
        
    app.run(debug=True, port=5000)
    # Starts the server. debug=True means the server will automatically restart if you save changes to the code, and it will show detailed error pages if it crashes.
```

---

## 🎨 HTML Templates (Jinja2)

Flask uses **Jinja2**, a templating engine. It lets us write normal HTML but insert Python logic inside special brackets!
- `{{ variable }}` is used to print/output data to the screen.
- `{% logic %}` is used for loops (`for`, `if`) and layout inheritance.

### `base.html`
```html
{% block content %}
{% endblock %}
<!-- This defines a "placeholder". Other HTML files can inherit this layout and inject their own code exactly where this block sits. -->
```

### `index.html`
```html
{% extends 'base.html' %}
<!-- Tells Jinja2: "Load base.html first, then put the stuff below into the content block!" -->

<form action="/add" method="POST">
<!-- Form Submission: The data here goes to @app.route('/add', methods=['POST']) in app.py -->

{% for note in notes %}
<!-- A Jinja2 For Loop. It loops over the 'notes' array we passed in render_template() -->

    <h5 class="card-title">{{ note.title }}</h5>
    <!-- Outputs the title of the specific note from the loop onto the webpage -->

    <a href="/delete/{{ note.id }}" class="btn btn-danger">Delete</a>
    <!-- Generates a dynamic link! If the note's ID is 3, this becomes href="/delete/3" -->

{% else %}
<!-- Jinja2 supports an 'else' attached directly to a 'for' loop. It runs ONLY if the list is completely empty. -->
    <h5>No notes found.</h5>
{% endfor %}
```
