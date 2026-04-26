# Q2 — Library Management System

> **IA Question:** Develop a Library Management System using Django with MVT architecture, PostgreSQL, models for Book/Member/IssueRecord with relationships, CRUD, issue/return books, availability check, and overdue book queries.

---

## 🚀 Setup & Run

```bash
# 1. Install dependencies
pip install django psycopg2-binary

# 2. Create project & app
django-admin startproject library_project .
python manage.py startapp library_app

# 3. Copy all files from this folder into the 'library_app' directory

# 4. In psql, create the database
CREATE DATABASE library_db;

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create admin superuser
python manage.py createsuperuser

# 7. Start the server
python manage.py runserver
```

| Page | URL |
|---|---|
| Books | http://127.0.0.1:8000/library/books/ |
| Members | http://127.0.0.1:8000/library/members/ |
| Issue Book | http://127.0.0.1:8000/library/issue/ |
| All Issues | http://127.0.0.1:8000/library/issue/list/ |
| Overdue | http://127.0.0.1:8000/library/overdue/ |
| Admin | http://127.0.0.1:8000/admin/ |

---

## ⚙️ settings.py Changes

### INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...
    'library_app',
]
```

### DATABASES:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'library_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### project/urls.py:
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('library/', include('library_app.urls')),
]
```

---

## 🗄️ Model Relationships

```
Book  ←──ForeignKey──  IssueRecord  ──ForeignKey──→  Member
 │                          │                            │
 id                         id                          id
 title                      book (FK)                   name
 author                     member (FK)                 email
 isbn                       issue_date                  phone
 total_copies               due_date                    joined_date
 available_copies           return_date
                            returned (Bool)
```

- `IssueRecord.book` → **ForeignKey** to `Book` (many issues per book)
- `IssueRecord.member` → **ForeignKey** to `Member` (many issues per member)
- `on_delete=CASCADE` → deleting a Book/Member removes their IssueRecords

---

## 📁 File Structure

```
library_app/
├── models.py              — Book, Member, IssueRecord
├── forms.py               — BookForm, MemberForm, IssueForm
├── views.py               — All views (CRUD + issue/return + overdue)
├── urls.py                — 13 URL patterns
├── admin.py               — All 3 models registered
└── templates/library/
    ├── base.html
    ├── book_list.html
    ├── member_list.html
    ├── form.html
    ├── issue_form.html
    ├── issue_list.html
    ├── overdue.html
    ├── member_books.html
    ├── return_confirm.html
    └── confirm_delete.html
```

---

## ✅ Features Implemented

| Feature | How |
|---|---|
| MVT Architecture | Model → View → Template |
| PostgreSQL | `psycopg2-binary` + settings.py config |
| Book model | `title, author, isbn, total_copies, available_copies` |
| Member model | `name, email, phone, joined_date` |
| IssueRecord model | `book (FK), member (FK), issue_date, due_date, return_date, returned` |
| Book CRUD | List, Add, Edit, Delete |
| Member CRUD | List, Add, Edit, Delete |
| Issue a book | Checks `available_copies > 0`, decrements on issue |
| Return a book | Sets `returned=True`, increments `available_copies` |
| Availability check | `book.is_available()` → `available_copies > 0` |
| Overdue books query | `filter(returned=False, due_date__lt=today)` |
| Books by member | `filter(member=member)` |
| Django ORM | `select_related()` for JOIN queries |
| Migrations | `makemigrations` + `migrate` |
| Django Admin | All 3 models with search & filter |
