# Q1 — Student Management System

> **IA Question:** Design and develop a Student Management System using Django with MVT architecture, PostgreSQL, CRUD operations, search by course, and unique email validation.

---

## 🚀 Setup & Run

```bash
# 1. Install dependencies
pip install django psycopg2-binary

# 2. Create project & app
django-admin startproject student_project .
python manage.py startapp students

# 3. Copy all files from this folder into the 'students' app directory

# 4. In psql, create the database
CREATE DATABASE student_db;

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create admin superuser
python manage.py createsuperuser

# 7. Start the server
python manage.py runserver
```

**App URL:** http://127.0.0.1:8000/students/  
**Admin URL:** http://127.0.0.1:8000/admin/

---

## ⚙️ settings.py Changes

### INSTALLED_APPS — add your app:
```python
INSTALLED_APPS = [
    ...
    'students',
]
```

### DATABASES — switch to PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'student_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### project/urls.py — include app URLs:
```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/', include('students.urls')),
]
```

---

## 📁 File Structure

```
students/
├── models.py              — Student model (id, name, email, course, date_of_joining)
├── forms.py               — StudentForm (ModelForm)
├── views.py               — CRUD views + search by course
├── urls.py                — URL patterns
├── admin.py               — Admin registration
└── templates/students/
    ├── base.html          — Base layout (navbar, messages)
    ├── list.html          — Student table + search form
    ├── form.html          — Add / Edit form
    └── confirm_delete.html
```

---

## ✅ Features Implemented

| Feature | How |
|---|---|
| MVT Architecture | Model → View → Template |
| PostgreSQL | `psycopg2-binary` + settings.py config |
| Student Model | `id, name, email, course, date_of_joining` |
| List students | `Student.objects.all()` |
| Add student | `ModelForm` + `form.save()` |
| Edit student | `ModelForm(instance=student)` |
| Delete student | `student.delete()` via POST |
| Search by course | `filter(course__icontains=query)` |
| Unique email | `email = EmailField(unique=True)` |
| Migrations | `makemigrations` + `migrate` |
| Django Admin | `@admin.register(Student)` |
| Flash messages | `messages.success()` |
| CSRF protection | `{% csrf_token %}` in every form |
