# 🌶️ Flask Zero-to-Hero Guide: Theory, Cheatsheet & Viva Questions

If you have *never* used Flask before, this is the only document you need to read to crush your 1-hour lab exam.

---

## 🧠 Section 1 — Flask Core Theory

### 1. What is Flask?
Flask is a "microframework" for building web applications in Python. 
- It is called "micro" because it does not require particular tools or libraries (unlike Django, which forces you to use its built-in database, admin panel, and forms).
- Flask is incredibly lightweight and flexible. Out of the box, it only handles **Routing** (matching URLs to Python functions) and **Templating** (rendering HTML).

### 2. The Request-Response Cycle
How does the internet work in Flask?
1. **Client (Browser):** A user types `http://localhost:5000/home` and hits enter. This sends an HTTP Request (GET) to the server.
2. **Server (Flask):** Flask looks at the URL (`/home`) and searches your `app.py` for an `@app.route('/home')` decorator.
3. **Controller Function:** Flask executes the Python function directly under that decorator. 
4. **Response:** The Python function returns a string, JSON, or an HTML template (`render_template`). Flask packages this into an HTTP Response and sends it back to the browser.

### 3. Routing Rules
Routing is how you bind URLs to Python functions.
- `@app.route('/')` binds the root URL.
- By default, routes ONLY accept `GET` requests.
- To accept form submissions, you MUST explicitly define `methods=['GET', 'POST']`.
- **Dynamic Routing:** You can pass variables through URLs. `@app.route('/user/<username>')` will extract the name and pass it to the function: `def profile(username):`.

### 4. Jinja2 Templating
Flask uses Jinja2 to dynamically generate HTML. Instead of writing static HTML, you can inject Python variables into the web page before sending it to the user.
- **Double curly braces `{{ }}`:** Prints a variable to the screen. E.g., `<h1>Hello {{ user.name }}</h1>`.
- **Percent brackets `{% %}`:** Used for control flow statements like loops and conditionals. E.g., `{% if user_logged_in %} ... {% endif %}`.
- **Template Inheritance:** The most powerful feature. You write one `base.html` containing your `<head>`, navbar, and scripts. All other pages `{% extends 'base.html' %}` and just fill in the blanks, preventing massive code duplication.

### 5. Flask-SQLAlchemy (The Database ORM)
Writing raw SQL queries (like `SELECT * FROM users WHERE id = 5`) is messy and prone to hacking (SQL injection). 
- **ORM (Object Relational Mapper):** SQLAlchemy converts Python Classes into database Tables, and Python objects into database Rows.
- When you do `User.query.all()`, the ORM automatically translates that into a secure SQL `SELECT` query under the hood, fetches the data, and returns it to you as easy-to-use Python lists.

---

## ⚡ Section 2 — Quick Revision Cheatsheet

### 🟢 Flask Routing Setup
| Task | Code Snippet |
|---|---|
| Initialize App | `from flask import Flask`<br>`app = Flask(__name__)` |
| Basic Route | `@app.route('/')`<br>`def home(): return "Hello"` |
| POST Route | `@app.route('/add', methods=['POST'])`<br>`def add(): pass` |
| Dynamic Route | `@app.route('/post/<int:id>')`<br>`def view_post(id): pass` |
| Render HTML | `return render_template('index.html', my_data=data)` |
| Redirect | `return redirect(url_for('home_function_name'))` |

### 📥 Handling Form Data
| Task | Code Snippet |
|---|---|
| Import Request | `from flask import request` |
| Get text input | `username = request.form.get('username')` |
| Check method | `if request.method == 'POST': ...` |

### 🍃 Flask-SQLAlchemy (Database)
| Task | Code Snippet |
|---|---|
| Define Model | `class User(db.Model):`<br>&nbsp;&nbsp;`id = db.Column(db.Integer, primary_key=True)`<br>&nbsp;&nbsp;`name = db.Column(db.String(50))` |
| Create Tables | `with app.app_context(): db.create_all()` |
| **Fetch All** | `users = User.query.all()` |
| **Fetch by ID** | `user = User.query.get_or_404(id)` |
| **Insert Row** | `new_user = User(name='Bob')`<br>`db.session.add(new_user)`<br>`db.session.commit()` |
| **Delete Row** | `db.session.delete(user_to_delete)`<br>`db.session.commit()` |

---

## 🗣️ Section 3 — 25 Viva Questions & Answers

**1. Q: What is Flask?**
> **A:** Flask is a lightweight WSGI web application framework in Python. It is classified as a "microframework" because it does not require particular tools or libraries, keeping the core simple but extensible.

**2. Q: Difference between Flask and Django?**
> **A:** Django is a "batteries-included" framework. It comes built-in with an ORM, admin panel, and authentication. Flask is a microframework; it provides only routing and templating out of the box, giving the developer complete freedom to choose their own database tools (like SQLAlchemy) and libraries.

**3. Q: What is routing in Flask?**
> **A:** Routing is the process of mapping web URLs to specific Python functions. When a user visits a specific URL, the function tied to that route via the `@app.route()` decorator is executed.

**4. Q: How does Flask handle dynamic URLs?**
> **A:** By adding variable sections to the route path inside angle brackets, like `@app.route('/user/<username>')`. The variable is then passed as an argument to the associated Python function.

**5. Q: What is `render_template`?**
> **A:** It is a Flask function that looks for an HTML file in the `templates/` folder, processes any Jinja2 syntax inside it (injecting Python variables), and sends the final HTML to the user's browser.

**6. Q: What is Jinja2?**
> **A:** Jinja2 is the default templating engine used by Flask. It allows developers to embed Python-like logic (such as `if` statements and `for` loops) and dynamic variables directly into HTML files.

**7. Q: Explain the difference between `{{ }}` and `{% %}` in Jinja2.**
> **A:** `{{ variable }}` is used as a print statement to output data to the webpage. `{% logic %}` is used to execute control flow statements like loops, conditionals, or template inheritance.

**8. Q: What is Template Inheritance in Flask?**
> **A:** It is a Jinja2 feature that allows you to build a base "skeleton" template (`base.html`) containing common elements like navigation bars and footers. Other templates can `{% extends 'base.html' %}` to inherit that layout and only override specific `{% block content %}` sections.

**9. Q: What is the `request` object in Flask?**
> **A:** The `request` object contains all the data the client (browser) sends to the server. This includes form data (`request.form`), query parameters (`request.args`), and the HTTP method used (`request.method`).

**10. Q: By default, what HTTP methods does a Flask route accept?**
> **A:** By default, a route only answers to `GET` requests. To handle form submissions, you must explicitly add `methods=['POST']` (or both) to the `@app.route` decorator.

**11. Q: What does `url_for()` do?**
> **A:** It generates a URL for a given endpoint (function name). This is highly recommended over hard-coding URLs in your templates, because if you change the route string later, `url_for()` will automatically update everywhere in your app.

**12. Q: What is `redirect()`?**
> **A:** It returns an HTTP response that instructs the client's browser to navigate to a different URL. It is almost always used in combination with `url_for()` after a successful `POST` request (like submitting a form) to prevent duplicate submissions.

**13. Q: What is SQLAlchemy?**
> **A:** SQLAlchemy is a popular SQL toolkit and Object Relational Mapper (ORM) for Python. `Flask-SQLAlchemy` is an extension that simplifies using it within Flask applications.

**14. Q: What is an ORM (Object Relational Mapper)?**
> **A:** An ORM is a technique that lets you query and manipulate data from a database using an object-oriented paradigm. Instead of writing raw SQL strings (`INSERT INTO table...`), you create Python classes, and the ORM translates your Python code into secure SQL automatically.

**15. Q: Why use an ORM instead of raw SQL?**
> **A:** ORMs speed up development, make the code much more readable, allow you to easily switch database engines (e.g., from SQLite to PostgreSQL) without rewriting queries, and provide automatic protection against SQL injection attacks.

**16. Q: Explain `db.session.add()` and `db.session.commit()`.**
> **A:** When you create a new Python object representing a database row, `db.session.add()` places it in a staging area. `db.session.commit()` permanently saves all staged changes to the actual database file.

**17. Q: How do you query all rows from a table in Flask-SQLAlchemy?**
> **A:** By calling `.query.all()` on the Model class. For example: `all_users = User.query.all()`.

**18. Q: What does `get_or_404(id)` do?**
> **A:** It queries the database for a row with the specified primary key ID. If it finds it, it returns the object. If the ID does not exist, it aborts the request and automatically displays a 404 Not Found error page, preventing the server from crashing.

**19. Q: What is the purpose of `app.config['SQLALCHEMY_DATABASE_URI']`?**
> **A:** It tells Flask-SQLAlchemy exactly which database engine to use and where the database file or server is located (e.g., `'sqlite:///notes.db'`).

**20. Q: What does `db.create_all()` do?**
> **A:** It inspects all the Models you have defined in your Python code and generates the corresponding SQL `CREATE TABLE` commands to initialize the database structure. It does nothing if the tables already exist.

**21. Q: Why do we wrap `db.create_all()` inside `app.app_context()`?**
> **A:** In modern Flask, the database extension needs to know which application it is attached to in order to read configuration variables. The `app_context()` provides this environment so the database can be created safely.

**22. Q: What does `app.run(debug=True)` do?**
> **A:** Enabling debug mode does two critical things: 1) It automatically restarts the server whenever you save changes to your Python files. 2) It provides an interactive, detailed traceback page in the browser if your code crashes.

**23. Q: What is a Primary Key?**
> **A:** A primary key is a column (or set of columns) in a database table that uniquely identifies every row. In SQLAlchemy, it is defined using `primary_key=True` (usually on an integer `id` column).

**24. Q: How do you serve static files like CSS or images in Flask?**
> **A:** You must place them inside a special directory named `static/` located in the same folder as `app.py`. Flask automatically serves files from this directory.

**25. Q: What is a Python Virtual Environment (`venv`)?**
> **A:** It is an isolated environment that allows you to install Python packages (like Flask) specific to a single project, rather than installing them globally on your operating system. This prevents version conflicts between different projects.
