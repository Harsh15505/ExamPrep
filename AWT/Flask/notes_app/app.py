from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# 1. Initialize the Flask application
app = Flask(__name__)

# 2. Configure the SQLite database
# This tells Flask-SQLAlchemy where to save our database file (it creates an 'instance' folder)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Initialize the Database object
db = SQLAlchemy(app)

# ==========================================
# 4. DATABASE MODEL (The Table Structure)
# ==========================================
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Note {self.title}>"

# ==========================================
# 5. ROUTES (Controllers)
# ==========================================

# READ (Display all notes)
@app.route('/')
def index():
    # Fetch all notes from the database
    all_notes = Note.query.all()
    # Pass the notes to our HTML template to be rendered
    return render_template('index.html', notes=all_notes)

# CREATE (Add a new note)
@app.route('/add', methods=['POST'])
def add_note():
    # Extract data from the HTML form using request.form
    note_title = request.form.get('title')
    note_content = request.form.get('content')
    
    # Validation: Ensure neither field is empty
    if note_title and note_content:
        # Create a new Note object in Python
        new_note = Note(title=note_title, content=note_content)
        # Add it to the database session and commit (save) it
        db.session.add(new_note)
        db.session.commit()
        
    # Redirect the user back to the home page (the index route)
    return redirect(url_for('index'))

# DELETE (Remove a note)
@app.route('/delete/<int:id>')
def delete_note(id):
    # Find the specific note by its ID (or show a 404 error if not found)
    note_to_delete = Note.query.get_or_404(id)
    
    # Delete it from the session and commit
    db.session.delete(note_to_delete)
    db.session.commit()
    
    return redirect(url_for('index'))

# UPDATE (Edit an existing note)
# Notice we allow both GET (to show the form) and POST (to save the changes)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    note_to_edit = Note.query.get_or_404(id)
    
    if request.method == 'POST':
        # If the user submitted the edit form, update the Python object's properties
        note_to_edit.title = request.form.get('title')
        note_to_edit.content = request.form.get('content')
        # Commit the changes to the database
        db.session.commit()
        return redirect(url_for('index'))
        
    # If it's a GET request, show a simple HTML form pre-filled with the current data
    return render_template('edit.html', note=note_to_edit)


# ==========================================
# 6. RUN THE APP
# ==========================================
if __name__ == "__main__":
    # Ensure the database tables are created before starting the server
    with app.app_context():
        db.create_all()
        
    # Start the Flask development server on port 5000 with debug mode enabled
    app.run(debug=True, port=5000)
