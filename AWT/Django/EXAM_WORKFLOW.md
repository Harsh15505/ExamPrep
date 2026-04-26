# 🧠 Django Exam Workflow: The CRUD Mental Model

When you sit down for your exam tomorrow, the question will likely give you a **database schema (models)** and ask you to implement **CRUD operations** (Create, Read, Update, Delete) with templates. 

Don't panic or jump around between files randomly. Follow this **strict, linear, step-by-step workflow**.

---

## 🚦 Phase 1: Project & App Setup (5 mins)
*Goal: Get the basic skeleton running.*

1. **Initialize Project:**
   ```bash
   django-admin startproject myproject .
   python manage.py startapp myapp
   ```
2. **Configure `settings.py`:**
   - Add `'myapp'` to `INSTALLED_APPS`.
   - Update `TEMPLATES` to find your templates if you are using a global folder:
     `'DIRS': [BASE_DIR / 'templates'],`
   - (If the exam asks for PostgreSQL, update the `DATABASES` dictionary now).

---

## 💾 Phase 2: Models & Database (10 mins)
*Goal: Translate the exam paper's schema into Python code.*

1. **Write Models (`myapp/models.py`):**
   - Translate the fields exactly as requested.
   - Example: `models.CharField`, `models.IntegerField`, `models.DecimalField`, `models.DateField(auto_now_add=True)`.
   - **Crucial:** Always add a `def __str__(self):` method so the records look nice in the admin panel.
2. **Run Migrations (VERY IMPORTANT):**
   ```bash
   python manage.py makemigrations myapp
   python manage.py migrate
   ```
3. **Register in Admin (`myapp/admin.py`):**
   ```python
   from django.contrib import admin
   from .models import MyModel
   admin.site.register(MyModel)
   ```
4. **Create a Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

---

## 📝 Phase 3: Forms (5 mins)
*Goal: Create the mechanism for taking user input. Do this BEFORE views!*

1. **Create `myapp/forms.py` (New File).**
2. **Use `ModelForm` (The ultimate time-saver):**
   ```python
   from django import forms
   from .models import MyModel

   class MyModelForm(forms.ModelForm):
       class Meta:
           model = MyModel
           fields = '__all__'  # Or a list: ['name', 'price', 'category']
   ```

---

## 🌐 Phase 4: URL Routing (5 mins)
*Goal: Define the "doors" (endpoints) to your application.*

1. **Project `myproject/urls.py`:**
   ```python
   from django.urls import path, include
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('myapp.urls')), # Route everything to your app
   ]
   ```
2. **App `myapp/urls.py` (New File):**
   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       path('', views.item_list, name='item_list'),                  # READ (All)
       path('add/', views.item_create, name='item_create'),          # CREATE
       path('<int:pk>/', views.item_detail, name='item_detail'),     # READ (One)
       path('<int:pk>/edit/', views.item_update, name='item_update'),# UPDATE
       path('<int:pk>/delete/', views.item_delete, name='item_delete'),# DELETE
   ]
   ```

---

## 🧠 Phase 5: Views (15 mins)
*Goal: The brain of the app. Connecting URLs, Models, Forms, and Templates.*

Write these in `myapp/views.py`. Always import:
```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import MyModel
from .forms import MyModelForm
```

**1. READ (List):**
```python
def item_list(request):
    items = MyModel.objects.all()
    return render(request, 'myapp/item_list.html', {'items': items})
```

**2. CREATE:**
```python
def item_create(request):
    if request.method == 'POST':
        form = MyModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = MyModelForm()
    return render(request, 'myapp/item_form.html', {'form': form})
```

**3. UPDATE:** *(Same as Create, but with an existing instance)*
```python
def item_update(request, pk):
    item = get_object_or_404(MyModel, pk=pk)
    # Pass instance=item so the form is pre-filled!
    if request.method == 'POST':
        form = MyModelForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = MyModelForm(instance=item)
    return render(request, 'myapp/item_form.html', {'form': form})
```

**4. DELETE:**
```python
def item_delete(request, pk):
    item = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST': # Deletions should happen via POST
        item.delete()
        return redirect('item_list')
    return render(request, 'myapp/item_confirm_delete.html', {'item': item})
```

---

## 🎨 Phase 6: Templates (10 mins)
*Goal: The frontend. Create the `.html` files in your `templates/myapp/` folder.*

**1. `base.html` (Optional but highly recommended)**
- Put your `<html>`, `<head>`, Bootstrap CSS, and a `{% block content %}{% endblock %}`.

**2. `item_list.html`**
```html
<a href="{% url 'item_create' %}">Add New</a>
<ul>
{% for item in items %}
    <li>
        {{ item.name }} - {{ item.price }}
        <a href="{% url 'item_update' item.pk %}">Edit</a>
        <a href="{% url 'item_delete' item.pk %}">Delete</a>
    </li>
{% endfor %}
</ul>
```

**3. `item_form.html` (Used for both Create and Update!)**
```html
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
```

**4. `item_confirm_delete.html`**
```html
<p>Are you sure you want to delete "{{ item.name }}"?</p>
<form method="POST">
    {% csrf_token %}
    <button type="submit">Yes, Delete</button>
    <a href="{% url 'item_list' %}">Cancel</a>
</form>
```

---

## 💡 Top 3 Traps to Avoid in the Exam

1. **Forgetting `{% csrf_token %}`:** If you forget this inside a `<form method="POST">`, Django will block the submission and throw a 403 Forbidden error.
2. **Missing Migrations:** If you edit `models.py` but forget `makemigrations` + `migrate`, you'll get an `OperationalError: no such table` or `no such column`.
3. **Putting Logic in the Wrong Place:** Keep files strictly isolated.
   - Database schemas? **models.py**
   - Taking user input? **forms.py**
   - Querying the DB and deciding what to show? **views.py**
   - HTML and variables? **templates**
