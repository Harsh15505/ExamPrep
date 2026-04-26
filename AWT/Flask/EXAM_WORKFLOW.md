# 🧠 Flask Exam Workflow: The CRUD Mental Model

In a Flask exam question, you are typically asked to create a single-file application (or a small module) using **Flask** and **Flask-SQLAlchemy**.

Follow this strict, linear workflow to ensure you don't miss any critical configurations.

---

## 🚦 Phase 1: Setup & Configuration (5 mins)
*Goal: Get the server running and connected to a database.*

1. **Imports and Initialization:**
   ```python
   from flask import Flask, render_template, request, redirect, url_for
   from flask_sqlalchemy import SQLAlchemy

   app = Flask(__name__)
   ```

2. **Database Configuration:**
   ```python
   # Set up SQLite database
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exam_db.sqlite3'
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   
   db = SQLAlchemy(app)
   ```

---

## 💾 Phase 2: Models (5 mins)
*Goal: Translate the exam schema into SQLAlchemy.*

1. **Create the Model:**
   ```python
   class Item(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(100), nullable=False)
       price = db.Column(db.Float, nullable=False)
       
       def __repr__(self):
           return f"<Item {self.name}>"
   ```

2. **Initialize the Database:**
   *(Do this right after your model, before your routes)*
   ```python
   with app.app_context():
       db.create_all()
   ```

---

## 🌐 Phase 3: Routes & Logic (CRUD) (15 mins)
*Goal: Define the endpoints and database interactions. In Flask, Routes and Views are the same thing.*

**1. READ (List All):**
```python
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)
```

**2. CREATE:**
```python
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # 1. Get data from form
        name = request.form['name']
        price = request.form['price']
        
        # 2. Create object
        new_item = Item(name=name, price=price)
        
        # 3. Save to DB
        db.session.add(new_item)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('add_form.html')
```

**3. UPDATE:**
```python
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get_or_404(id)
    
    if request.method == 'POST':
        # Update fields
        item.name = request.form['name']
        item.price = request.form['price']
        
        db.session.commit() # Just commit to save changes
        return redirect(url_for('index'))
        
    return render_template('edit_form.html', item=item)
```

**4. DELETE:**
```python
@app.route('/delete/<int:id>', methods=['POST'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))
```

---

## 🎨 Phase 4: Templates (Jinja2) (10 mins)
*Goal: Build the HTML files inside a `templates/` folder.*

**1. `index.html`**
```html
<a href="{{ url_for('add_item') }}">Add New</a>
<ul>
{% for item in items %}
    <li>
        {{ item.name }} - ${{ item.price }}
        <a href="{{ url_for('edit_item', id=item.id) }}">Edit</a>
        
        <!-- Delete should be a POST request via a form -->
        <form action="{{ url_for('delete_item', id=item.id) }}" method="POST" style="display:inline;">
            <button type="submit">Delete</button>
        </form>
    </li>
{% endfor %}
</ul>
```

**2. `add_form.html` & `edit_form.html`**
*(Make sure `<input name="...">` matches the keys you use in `request.form['...']`)*
```html
<form method="POST">
    <label>Name:</label>
    <!-- Use value="{{ item.name }}" for the edit form! -->
    <input type="text" name="name" required>
    
    <label>Price:</label>
    <input type="number" step="0.01" name="price" required>
    
    <button type="submit">Save</button>
</form>
```

---

## 🏃 Phase 5: Run the App
```python
if __name__ == '__main__':
    app.run(debug=True)
```

## 💡 Top 3 Flask Traps to Avoid
1. **Forgetting `app.app_context()`:** In modern Flask, `db.create_all()` will fail if it's not wrapped in the app context.
2. **Missing `methods=['GET', 'POST']`:** By default, routes only accept `GET`. If your form submits but you get a "Method Not Allowed" error, you forgot this!
3. **Template Folder Name:** Flask STRICTLY looks for a folder named exactly `templates` in the same directory as your python script. Misspelling it guarantees a `TemplateNotFound` error.
