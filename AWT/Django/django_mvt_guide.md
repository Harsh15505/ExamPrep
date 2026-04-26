# Django MVT Guide — Library Management System
### *Quiz Prep: Write Any Small Django App From Memory*

---

## 🧠 Section 0 — Django Theory (The Why)

### What is Django?
Django is a **batteries-included** Python web framework. It follows the **MVT (Model-View-Template)** pattern, which is Django's version of MVC.

| Django Term | What It Does | MVC Equivalent |
|---|---|---|
| **Model** | Defines data structure & talks to DB | Model |
| **View** | Business logic — fetches data, decides what to show | Controller |
| **Template** | HTML rendered with dynamic data | View |

> Django calls it MVT but the "View" acts like a Controller and "Template" acts like a View. Don't let the naming confuse you.

### Django's Core Philosophy
- **DRY** — Don't Repeat Yourself. Write code once, reuse everywhere.
- **Explicit is better than implicit** — You wire things up manually (URLs → Views).
- **Convention over config** — Django has strong defaults (e.g., templates go in `templates/`, static files in `static/`).
- **Pluggable apps** — A Django project is a collection of apps. Each app is a self-contained module (e.g., `library_app`, `auth`, `admin`).

---

## 🔄 Section 0.1 — Full Request Lifecycle (How Django Works)

When a browser hits `http://localhost:8000/books/`, here's what happens step by step:

```
1. Django starts → reads settings.py (DB, apps, middleware, etc.)

2. Browser sends:  GET /books/

3. Django checks:  project/urls.py
                    → finds: path('', include('library_app.urls'))

4. Django checks:  library_app/urls.py
                    → finds: path('books/', views.book_list)

5. Django calls:   views.book_list(request)
                    → view talks to Model: Book.objects.all()
                    → Model runs SQL: SELECT * FROM library_app_book;
                    → DB returns rows as Python objects

6. View prepares context dict: {'books': [<Book>, <Book>, ...]}

7. Django renders: templates/library_app/book_list.html
                    → replaces {{ book.title }} with actual values
                    → loops through {% for %} blocks

8. Browser receives: Full HTML page
```

---

## ⚔️ Section 0.2 — Django vs Node.js (Since You Know Node!)

You already understand the web. Django just uses different vocabulary.

### High-Level Comparison

| Concept | Node.js (Express) | Django (Python) |
|---|---|---|
| Language | JavaScript | Python |
| Framework style | Minimal, you add what you need | Batteries-included — everything built-in |
| Server startup | `node index.js` / `npm start` | `python manage.py runserver` |
| Package manager | `npm` | `pip` |
| Package file | `package.json` | `requirements.txt` |
| Entry point | `index.js` / `app.js` | `manage.py` |
| Config file | `.env` + often `config.js` | `settings.py` |
| ORM | Sequelize / Prisma / Mongoose | Django ORM (built-in) |
| Migrations | `npx prisma migrate` | `python manage.py migrate` |
| Routing | `app.get('/books', handler)` | `path('books/', views.book_list)` |
| Route handler | A function with `(req, res)` | A function with `(request)` |
| Sending a response | `res.render('template', data)` | `return render(request, 'template.html', context)` |
| Middleware | `app.use(middleware)` | `MIDDLEWARE = [...]` in settings.py |
| Static files | `express.static('public')` | `django.contrib.staticfiles` |
| Auth system | Passport.js / custom | Built into Django (`django.contrib.auth`) |
| Admin panel | Custom or third-party | Built-in at `/admin/` (free!) |

---

### Code-Level Parallels

#### 1. Routing

**Node.js (Express):**
```javascript
// app.js or routes/books.js
const express = require('express');
const router = express.Router();

router.get('/books', bookController.listBooks);
app.use('/', router);
```

**Django:**
```python
# library_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list),   # same idea, different syntax
]
```

---

#### 2. Route Handler / Controller vs View

**Node.js (Express Controller):**
```javascript
// controllers/bookController.js
const Book = require('../models/Book');

exports.listBooks = async (req, res) => {
    const books = await Book.findAll();     // Sequelize ORM
    res.render('books', { books });         // Pass to template
};
```

**Django View:**
```python
# views.py
from .models import Book
from django.shortcuts import render

def book_list(request):                     # request = req
    books = Book.objects.all()             # Django ORM
    return render(request, 'book_list.html', {'books': books})  # res.render()
```

> **Key insight:** Django's `request` ≈ Node's `req`. Django's `render()` ≈ `res.render()`.

---

#### 3. Models / Database Schema

**Node.js (Sequelize):**
```javascript
// models/Book.js
const { DataTypes } = require('sequelize');
module.exports = sequelize.define('Book', {
    title:  { type: DataTypes.STRING },
    author: { type: DataTypes.STRING },
});
```

**Django:**
```python
# models.py
from django.db import models

class Book(models.Model):
    title  = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
```

> Django auto-creates the table name as `appname_modelname` (e.g., `library_app_book`).

---

#### 4. Templating

**Node.js (EJS):**
```html
<% books.forEach(book => { %>
  <li><%= book.title %></li>
<% }) %>
```

**Django Templates:**
```html
{% for book in books %}
  <li>{{ book.title }}</li>
{% endfor %}
```

> Almost identical concept! Django uses `{% %}` for logic, `{{ }}` for output.

---

#### 5. Environment / Project Setup

**Node.js:**
```bash
npm init -y                  # create project
npm install express          # install dependency
node index.js                # run server
```

**Django:**
```bash
pip install django            # install dependency
django-admin startproject library_project .   # create project
python manage.py startapp library_app         # create app
python manage.py runserver    # run server
```

---

#### 6. Middleware

**Node.js:**
```javascript
app.use(express.json());         // parse JSON body
app.use(cors());                 // cross-origin
app.use(authMiddleware);         // custom
```

**Django (settings.py):**
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # ... built-in ones are already there
]
```

> In Django, middleware is configured in `settings.py` not in code.

---

#### 7. What Django Has That Node Doesn't (Out of the Box)

| Feature | Node.js | Django |
|---|---|---|
| Admin Panel | ❌ Build it yourself | ✅ `/admin/` — FREE |
| User auth system | ❌ Use Passport.js | ✅ Built-in (`User` model, sessions, login views) |
| ORM | ❌ Need Sequelize/Prisma | ✅ Django ORM built-in |
| Migrations | ❌ Need a separate tool | ✅ `makemigrations` + `migrate` |
| Form validation | ❌ Use Joi or similar | ✅ Django Forms built-in |

---

## 🔧 Section 0.3 — General Django App Workflow (Step by Step)

This is the order you always follow when building any Django app:

```
Step 1:  django-admin startproject myproject .
          → Creates settings.py, urls.py, wsgi.py, manage.py

Step 2:  python manage.py startapp myapp
          → Creates models.py, views.py, admin.py, apps.py

Step 3:  Register app in settings.py
          INSTALLED_APPS = [..., 'myapp']

Step 4:  Define models in myapp/models.py
          class MyModel(models.Model): ...

Step 5:  Run migrations
          python manage.py makemigrations
          python manage.py migrate

Step 6:  Write views in myapp/views.py
          def my_view(request): ...

Step 7:  Create myapp/urls.py and define URL patterns
          urlpatterns = [path('...', views.my_view)]

Step 8:  Include app URLs in project urls.py
          path('', include('myapp.urls'))

Step 9:  Create templates in myapp/templates/myapp/
          book_list.html, etc.

Step 10: Register model in admin.py (optional but useful)
          admin.site.register(MyModel)

Step 11: python manage.py runserver
          → Visit http://127.0.0.1:8000/
```

---


## 🗺️ The Big Picture — Django MVT Architecture

```
Browser Request
      ↓
   urls.py          ← "Which view handles this URL?"
      ↓
   views.py         ← "Fetch data from Model, send to Template"
      ↓          ↖
  models.py         ← "Talk to the database"
      ↓
  templates/        ← "Render HTML with the data"
      ↓
Browser Response
```

**Project name:** `library_project`  
**App name:** `library_app`

---

## Step 0 — Project Structure
```
library_project/
│
├── library_project/        ← Project config folder
│   ├── settings.py
│   ├── urls.py             ← Root URL config
│   └── wsgi.py
│
├── library_app/            ← Your app folder
│   ├── models.py
│   ├── views.py
│   ├── urls.py             ← App-level URL config
│   └── templates/
│       └── library_app/
│           └── book_list.html
│
└── manage.py
```

---

## 1. `settings.py` — Database Configuration

> The question will usually ask you to configure MySQL or SQLite.

### SQLite (default — no install needed)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### MySQL
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'library_db',
        'USER': 'root',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Also register your app in `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ... default apps ...
    'library_app',   # ← Add this line
]
```

---

## 2. `models.py` — Model Definition

> The question will give you a model name + field names. Just map them.

```python
from django.db import models

class Book(models.Model):
    title       = models.CharField(max_length=200)
    author      = models.CharField(max_length=100)
    published   = models.DateField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
```

### Common Field Types (memorize these!)

| Field | Use For |
|---|---|
| `CharField(max_length=N)` | Short text (names, titles) |
| `TextField()` | Long text (descriptions) |
| `IntegerField()` | Whole numbers |
| `FloatField()` | Decimal numbers |
| `BooleanField()` | True/False |
| `DateField()` | Date only |
| `DateTimeField()` | Date + time |
| `EmailField()` | Email address |
| `ForeignKey(Model, on_delete=models.CASCADE)` | Many-to-one relation |

### After defining models, run:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 3. `views.py` — View Logic

> The question will ask for a function-based view. Always: **fetch → render**.

```python
from django.shortcuts import render
from .models import Book

# List all books
def book_list(request):
    books = Book.objects.all()          # Fetch all records
    context = {'books': books}          # Pack into context dict
    return render(request, 'library_app/book_list.html', context)

# (Optional) Detail view for one book
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'library_app/book_detail.html', {'book': book})
```

### ORM Cheat Sheet (memorize these!)

```python
Book.objects.all()               # Get ALL records
Book.objects.filter(author="Rowling")  # Filter records
Book.objects.get(id=1)           # Get ONE record by id
Book.objects.order_by('title')   # Sort results
Book.objects.count()             # Count records
```

---

## 4. `urls.py` — URL Configuration

### App-level: `library_app/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
]
```

### Project-level: `library_project/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library_app.urls')),  # ← Include app URLs
]
```

---

## 5. `templates/library_app/book_list.html` — Template

```html
<!DOCTYPE html>
<html>
<head>
    <title>Library — Book List</title>
</head>
<body>
    <h1>All Books</h1>

    {% if books %}
        <ul>
            {% for book in books %}
                <li>{{ book.title }} — {{ book.author }} ({{ book.published }})</li>
            {% endfor %}
        </ul>
    {% else %}
        <p>No books found.</p>
    {% endif %}

</body>
</html>
```

### Django Template Syntax (memorize these!)

| Syntax | Purpose |
|---|---|
| `{{ variable }}` | Print a variable |
| `{{ book.title }}` | Print a field of an object |
| `{% for item in list %}` ... `{% endfor %}` | Loop |
| `{% if condition %}` ... `{% endif %}` | Conditional |
| `{% url 'view_name' %}` | Generate a URL by name |
| `{% block content %}` ... `{% endblock %}` | Template inheritance |

---

## 6. `admin.py` — Register Model (bonus — often asked)

```python
from django.contrib import admin
from .models import Book

admin.site.register(Book)
```

---

## ⚡ Quiz Answer Formula

When you get a question like: *"Build a Student Record app with fields `name`, `roll_no`, `grade`"*, just follow this mental map:

```
1. settings.py   → DATABASES dict (MySQL/SQLite)
                 → Add app to INSTALLED_APPS

2. models.py     → class Student(models.Model):
                       name    = CharField
                       roll_no = IntegerField
                       grade   = CharField

3. views.py      → def list_students(request):
                       students = Student.objects.all()
                       return render(request, 'template.html', {'students': students})

4. app/urls.py   → path('students/', views.list_students, name='list_students')

5. project/urls.py → include('app.urls')

6. template.html → {% for s in students %} {{ s.name }} {% endfor %}
```

---

## 🧠 Things to Remember Off the Top of Your Head

1. **`from django.shortcuts import render`** — always needed in views
2. **`from .models import ModelName`** — import your model (note the `.`)
3. **`request`** is always the first argument in every view function
4. **`context`** is a **dictionary** passed to the template
5. **`objects.all()`** returns a QuerySet (like a list of model instances)
6. Django template tags use `{% %}`, variables use `{{ }}`
7. URLs use `path()`, not `url()` (old syntax)
8. Always `include()` app urls in the project urls

---

## 📝 Full Example Answer (for reference)

**Question:** *"Project: `campus_hub`, App: `library_app`. Create a Book model with `title`, `author`, `published_date`. Write a view `list_books` that fetches all books and renders `books.html`. Configure MySQL database."*

### `settings.py`
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'campus_hub_db',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'library_app',   # ← your app
]
```

### `models.py`
```python
from django.db import models

class Book(models.Model):
    title          = models.CharField(max_length=200)
    author         = models.CharField(max_length=100)
    published_date = models.DateField()

    def __str__(self):
        return self.title
```

### `views.py`
```python
from django.shortcuts import render
from .models import Book

def list_books(request):
    books = Book.objects.all()
    return render(request, 'library_app/books.html', {'books': books})
```

### `library_app/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
]
```

### `campus_hub/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library_app.urls')),
]
```

### `templates/library_app/books.html`
```html
<!DOCTYPE html>
<html>
<head><title>Book List</title></head>
<body>
    <h1>Books</h1>
    <ul>
        {% for book in books %}
            <li>{{ book.title }} by {{ book.author }} — {{ book.published_date }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```

---

> **Good luck on your quiz! 🎯** Remember: Model → View → Template. Each file has ONE job.


---

## 🎤 Section 7 — Viva Questions & Answers (25 Q&A)

---

### Q1. What is Django? Why is it called "batteries included"?
**Answer:**
Django is a high-level, open-source Python web framework for rapid development. It is called "batteries included" because it ships with everything built-in — ORM, Admin Panel, Authentication, URL routing, Template Engine, Form handling, and Security Middleware — without needing external packages.

---

### Q2. Explain MVT Architecture. How is it different from MVC?
**Answer:**
MVT = Model-View-Template. Django's version of MVC.

| MVC | MVT | Role |
|---|---|---|
| Model | Model | Data + DB |
| Controller | View | Business Logic |
| View | Template | HTML/Presentation |

In Django, the **framework itself acts as the Controller** — it handles URL routing and dispatches to the correct View. The developer only writes Models, Views, and Templates.

---

### Q3. What is Django's ORM? What are its advantages?
**Answer:**
ORM (Object Relational Mapper) lets you interact with the database using Python objects instead of raw SQL.

**Advantages:**
1. **Database agnostic** — same code works with SQLite, PostgreSQL, MySQL
2. **No SQL injection** — ORM parameterizes queries automatically
3. **Pythonic** — use Python syntax instead of SQL strings
4. **Auto migrations** — model changes auto-generate SQL

```python
# ORM
Student.objects.filter(course="B.Tech")
# SQL equivalent: SELECT * FROM students WHERE course = 'B.Tech';
```

---

### Q4. What is the difference between `makemigrations` and `migrate`?
**Answer:**

| Command | What it does |
|---|---|
| `makemigrations` | Reads `models.py`, creates migration files in `migrations/`. **Does NOT touch the DB.** |
| `migrate` | Reads migration files and **executes them against the database** — creates/alters/drops tables. |

**Analogy:** `makemigrations` writes a recipe. `migrate` cooks the food.

---

### Q5. What is CSRF? Why does Django require `{% csrf_token %}` in forms?
**Answer:**
**CSRF (Cross-Site Request Forgery)** — an attack where a malicious site tricks a logged-in user's browser into submitting a request to your site.

Django's protection:
- Generates a unique secret token per session
- `{% csrf_token %}` embeds it as a hidden field in every POST form
- Middleware validates it on every POST — missing/wrong token → **403 Forbidden**

**Rule:** Every `<form method="POST">` MUST have `{% csrf_token %}`.

---

### Q6. What is `get_object_or_404()`? Why use it over `Model.objects.get()`?
**Answer:**
```python
# Bad — raises unhandled exception → 500 Server Error
student = Student.objects.get(pk=pk)

# Good — returns a proper 404 page
student = get_object_or_404(Student, pk=pk)
```
`get_object_or_404()` catches the `DoesNotExist` exception and returns a clean 404 response instead of crashing the server.

---

### Q7. What is the difference between `null=True` and `blank=True`?
**Answer:**

| Option | Level | Effect |
|---|---|---|
| `null=True` | Database | Allows NULL in the DB column |
| `blank=True` | Form/Validation | Allows empty value in forms |

- String fields (CharField, TextField): use `blank=True`, not `null=True`
- Non-string fields (DateField, ForeignKey): use `null=True, blank=True` to make optional

---

### Q8. Explain Django Template Inheritance (`{% extends %}` and `{% block %}`).
**Answer:**
Template inheritance lets child templates reuse a base layout (DRY principle).

**base.html** defines placeholders:
```html
{% block content %}{% endblock %}
```

**child.html** fills them:
```html
{% extends 'base.html' %}
{% block content %}
  <h1>My Content</h1>
{% endblock %}
```
The child gets the full base layout (navbar, footer) and only overrides the blocks it needs.

---

### Q9. What is `ModelForm`? How is it different from a regular Form?
**Answer:**

| Feature | `forms.Form` | `forms.ModelForm` |
|---|---|---|
| Fields | Manually defined | Auto-generated from Model |
| Validation | Manual | Includes model-level validation (unique, etc.) |
| Saving | Manual | Built-in `.save()` method |

```python
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']
```

---

### Q10. What is the POST-Redirect-GET pattern? Why use `redirect()` after form submit?
**Answer:**
After a successful POST, always redirect to a GET request.

```python
if form.is_valid():
    form.save()
    return redirect('book-list')  # POST-Redirect-GET
```

**Why?** Without redirect, pressing F5/Refresh after POST resubmits the form → duplicate records. Redirect breaks that cycle.

---

### Q11. What is `__icontains` in Django ORM? Name other field lookups.
**Answer:**
`__icontains` = case-insensitive SQL `ILIKE '%value%'`

```python
Book.objects.filter(title__icontains="python")
# Matches "Python", "PYTHON", "python crash course"
```

**Common lookups:**
| Lookup | SQL |
|---|---|
| `__exact` | `= 'value'` |
| `__icontains` | `ILIKE '%value%'` |
| `__startswith` | `LIKE 'value%'` |
| `__gt / __lt` | `> / <` |
| `__in` | `IN (v1, v2)` |
| `__isnull` | `IS NULL` |

---

### Q12. What is `manage.py`? Name 5 important commands.
**Answer:**
`manage.py` is Django's CLI tool created automatically with `startproject`.

| Command | Purpose |
|---|---|
| `runserver` | Start development server |
| `makemigrations` | Create migration files |
| `migrate` | Apply migrations to DB |
| `createsuperuser` | Create admin user |
| `startapp` | Create a new app |
| `shell` | Interactive Python shell with Django loaded |

---

### Q13. What is the difference between a Django Project and a Django App?
**Answer:**

| | Project | App |
|---|---|---|
| Created by | `django-admin startproject` | `python manage.py startapp` |
| Contains | `settings.py`, root `urls.py` | `models.py`, `views.py`, `templates/` |
| Scope | One per website | Multiple per project |

Example: Project = `university_portal`, Apps = `students`, `library`, `faculty`

---

### Q14. How does Django connect to PostgreSQL? What package is required?
**Answer:**
Requires `psycopg2-binary`: `pip install psycopg2-binary`

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

### Q15. What is Django Middleware?
**Answer:**
Middleware is a pipeline of hooks that processes **requests before reaching the View** and **responses before sending to the browser**.

```
Request → [Security] → [Session] → [CSRF] → View
Response ← [Security] ← [Session] ← [CSRF] ← View
```

Examples: `SecurityMiddleware`, `CsrfViewMiddleware`, `SessionMiddleware`, `AuthenticationMiddleware`

---

### Q16. What is `{% url %}` tag? Why use it over hardcoding URLs?
**Answer:**
`{% url %}` performs reverse URL lookup — generates a URL from a named URL pattern.

```html
<!-- BAD — breaks if URL changes -->
<a href="/books/3/edit/">Edit</a>

<!-- GOOD — auto-updates when URL changes -->
<a href="{% url 'edit-book' book.pk %}">Edit</a>
```

---

### Q17. How does `unique=True` validate email uniqueness automatically?
**Answer:**
`unique=True` does TWO things:
1. **DB level** — PostgreSQL adds a `UNIQUE` constraint on the column
2. **Form level** — `ModelForm.is_valid()` queries the DB to check for duplicates and adds a field error automatically: *"with this Email already exists."*

No extra validation code needed.

---

### Q18. What are Django's `context` and `render()` function?
**Answer:**
`context` = a Python dictionary passed from View to Template. Keys become template variables.

```python
return render(request, 'books/list.html', {
    'books': Book.objects.all(),   # accessed as {{ books }}
    'title': 'Book List',          # accessed as {{ title }}
})
```

`render()` loads the template, injects context, and returns an `HttpResponse`.

---

### Q19. What is the `instance` parameter in ModelForm?
**Answer:**
Tells `ModelForm` to **UPDATE** an existing record instead of **INSERT** a new one.

```python
# Without instance → INSERT
form = BookForm(request.POST)

# With instance → UPDATE
book = get_object_or_404(Book, pk=pk)
form = BookForm(request.POST, instance=book)
form.save()
```

For GET (pre-fill edit form): `form = BookForm(instance=book)`

---

### Q20. What is `request.method` and what HTTP methods does Django use?
**Answer:**

```python
if request.method == 'POST':
    # process form
else:
    # show empty form (GET)
```

| Method | Used for | Data in |
|---|---|---|
| `GET` | Reading/fetching, search | `request.GET` |
| `POST` | Create/update via forms | `request.POST` |

HTML forms only support GET and POST. PUT/DELETE are used in REST APIs.

---

### Q21. What is Django Admin? How do you register a model?
**Answer:**
Built-in auto-generated admin UI to manage DB records. Access at `/admin/`.

```python
# admin.py
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author']
    search_fields = ['title', 'author']
    list_filter = ['published_date']
```

Create superuser: `python manage.py createsuperuser`

---

### Q22. What are Django Template Filters? Give examples.
**Answer:**
Filters transform variables in templates. Syntax: `{{ variable|filter }}`

| Filter | Example | Output |
|---|---|---|
| `length` | `{{ books\|length }}` | Count |
| `upper` | `{{ title\|upper }}` | "DJANGO" |
| `date:"d M Y"` | `{{ doj\|date:"d M Y" }}` | "26 Apr 2026" |
| `default:"N/A"` | `{{ phone\|default:"N/A" }}` | "N/A" if empty |
| `truncatewords:5` | `{{ bio\|truncatewords:5 }}` | "This is a..." |

---

### Q23. What is a QuerySet? Is it lazy?
**Answer:**
A QuerySet is a collection of DB objects from the ORM — represents a SELECT query.

**Yes, QuerySets are lazy** — they don't hit the DB until evaluated (iterated, sliced, printed, or passed to a template).

```python
books = Book.objects.filter(author="Guido")  # No DB hit yet
# DB hit happens when template does {% for book in books %}
```

Chaining multiple filters still results in ONE SQL query.

---

### Q24. What is `__str__` in a Django model? Why is it important?
**Answer:**
`__str__` defines the human-readable string representation of a model object.

```python
def __str__(self):
    return self.title
```

**Why important:**
- Django Admin displays objects using `__str__` in list views and dropdowns
- Without it, admin shows `Book object (1)` — useless

---

### Q25. What is `include()` in Django URLs?
**Answer:**
`include()` delegates URL patterns to an app's `urls.py`, keeping things modular.

```python
# project/urls.py
urlpatterns = [
    path('books/', include('library_app.urls')),
]
```

Any URL starting with `books/` is handed off to `library_app/urls.py`.

**Benefits:** Organized, reusable apps, avoids one giant `urls.py`.

---

## 🎯 Quick Revision Cheatsheet

| Topic | Key Point |
|---|---|
| MVT | Model=Data, View=Logic, Template=HTML |
| ORM | Python → SQL, database agnostic |
| `makemigrations` | Creates migration files (no DB change) |
| `migrate` | Applies migrations to DB |
| CSRF | Token required in every POST form |
| `ModelForm` | Auto-generates form, has `.save()` |
| `render()` | Template + context → HttpResponse |
| `redirect()` | POST-Redirect-GET pattern |
| `get_object_or_404` | Safe fetch — returns 404 if not found |
| `__icontains` | Case-insensitive LIKE search |
| `unique=True` | DB constraint + auto form validation |
| `{% csrf_token %}` | Required in every POST form |
| `{% extends %}` | Template inheritance |
| `{% url %}` | Reverse URL lookup by name |
| `instance=` | Tells ModelForm to UPDATE not INSERT |
| `__str__` | Human-readable object in admin |
| QuerySet | Lazy — hits DB only when evaluated |

---

> **Good luck on your exam! 🎯** Remember: Model → View → Template. Each file has ONE job.
