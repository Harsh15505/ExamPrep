# PYQ — E-Commerce Product Catalog: Complete Guide

> **Source:** Pandit Deendayal Energy University — Practical End Semester Exam, April-May 2025
> **Subject:** Advanced Web Technology (20cp308p) | **Semester:** 6th B.Tech CSE

---

## 📋 Question (SET-1)

> Create a Django web application for an **E-Commerce product catalog** using the **MVT architecture** and connect it to a **SQLite database**. Define a `Product` model with fields: `name, description, price, category, available_stock, created_at`. Configure the default SQLite database. Implement views to:
> 1. **Add** new products
> 2. **Display a list** of all products
> 3. **View detailed information** for each product using its ID
>
> Set up URL routing, create HTML templates, and ensure all data operations (insert and retrieve) are handled through Django's ORM.

---

## 🚀 Setup & Run

```bash
# 1. Install Django (SQLite is built into Python — no extra install needed)
pip install django

# 2. Create project and app
django-admin startproject ecommerce_project .
python manage.py startapp catalog

# 3. In settings.py → add 'catalog' to INSTALLED_APPS

# 4. In project urls.py → include catalog URLs

# 5. Run migrations (creates SQLite DB automatically)
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser for admin
python manage.py createsuperuser

# 7. Start server
python manage.py runserver
```

**URLs:**
| Page | URL |
|---|---|
| Product List | http://127.0.0.1:8000/products/ |
| Add Product | http://127.0.0.1:8000/products/add/ |
| Product Detail | http://127.0.0.1:8000/products/3/ |
| Admin | http://127.0.0.1:8000/admin/ |

---

## ⚙️ settings.py Configuration

```python
# Add app to INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'catalog',   # ← your app name
]

# SQLite is the DEFAULT — no changes needed to DATABASES
# Django auto-creates db.sqlite3 in your project folder on first migrate
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',    # file path to SQLite DB file
    }
}
```

**In project `urls.py`:**
```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('catalog.urls')),
]
```

---

## 📄 models.py — Line by Line

```python
from django.db import models
# Imports the base Model class and all field types

class Product(models.Model):
    # Inherits from models.Model — makes this a DB-backed class
    # Table name: catalog_product (appname_classname)
    # Django auto-adds: id = AutoField(primary_key=True)

    name = models.CharField(max_length=200)
    # CharField: short text → VARCHAR(200) in DB
    # max_length is REQUIRED for CharField

    description = models.TextField()
    # TextField: unlimited length text → TEXT in DB
    # No max_length needed. Use for paragraphs/long content.
    # Difference from CharField: TextField → <textarea>, CharField → <input>

    price = models.DecimalField(max_digits=10, decimal_places=2)
    # DecimalField: exact decimal number — CRITICAL for money values
    # max_digits=10: total digits across both sides of decimal
    # decimal_places=2: digits after decimal → e.g., 49999.99
    # WHY NOT FloatField? Floats have binary rounding errors (0.1 + 0.2 ≠ 0.3)
    # DecimalField stores EXACT values using Python's Decimal type

    category = models.CharField(max_length=100)
    # Product category: "Electronics", "Clothing", "Books", etc.

    available_stock = models.PositiveIntegerField(default=0)
    # PositiveIntegerField: only 0 or positive whole numbers (no negatives)
    # default=0: if not specified when creating, defaults to 0 units

    created_at = models.DateTimeField(auto_now_add=True)
    # DateTimeField: stores date AND time → "2025-04-29 16:30:00"
    # auto_now_add=True: AUTOMATICALLY set to current datetime on INSERT
    # NOT editable — you can never change it after creation
    # Not shown in forms — Django handles it internally

    def __str__(self):
        return f"{self.name} (₹{self.price})"
        # When Django Admin shows this product, it displays: "Laptop (₹49999.00)"
        # Also used in shell: print(product) → "Laptop (₹49999.00)"
```

---

## 📄 forms.py — Line by Line

```python
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    # ModelForm: auto-generates form fields from Product model
    # Handles validation and .save() to DB

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'available_stock']
        # 'created_at' is NOT included — auto_now_add sets it automatically
        # 'id' is NOT included — Django auto-manages primary key

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',     # Bootstrap styling
                'placeholder': 'Product name'
            }),
            # Renders: <input type="text" class="form-control" placeholder="Product name">

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,                   # Height of textarea (4 lines visible)
                'placeholder': 'Product description'
            }),
            # Renders: <textarea class="form-control" rows="4">...</textarea>
            # Textarea is the widget for TextField (long text)

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',   # Allows decimals: 49999.99 (not just integers)
                'placeholder': '0.00'
            }),
            # Renders: <input type="number" step="0.01" ...>

            'category': forms.TextInput(attrs={'class': 'form-control'}),

            'available_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            # Renders: <input type="number" ...> (integers only)
        }
```

---

## 📄 views.py — Line by Line

```python
from django.shortcuts import render, redirect, get_object_or_404
# render:            template + context → HttpResponse
# redirect:          HTTP 302 to a different URL
# get_object_or_404: fetch by pk or show 404

from django.contrib import messages
from .models import Product
from .forms import ProductForm


# ══════════════════════════════════════════
# VIEW 1: Product List (Retrieve all)
# URL: /products/
# ══════════════════════════════════════════
def product_list(request):
    products = Product.objects.all()
    # Django ORM generates: SELECT * FROM catalog_product ORDER BY created_at DESC
    # Returns a QuerySet — lazy (doesn't hit DB until template iterates it)
    # Ordering from Meta class in model (newest first)

    return render(request, 'catalog/product_list.html', {'products': products})
    # render() arguments:
    #   1. request — the HTTP request object
    #   2. 'catalog/product_list.html' — template to load
    #   3. {'products': products} — context dict: keys become template variables


# ══════════════════════════════════════════
# VIEW 2: Product Detail (Retrieve one by ID)
# URL: /products/<pk>/  e.g. /products/3/
# ══════════════════════════════════════════
def product_detail(request, pk):
    # 'pk' is captured from the URL by <int:pk> in urls.py
    # /products/3/ → Django extracts 3, passes as pk=3

    product = get_object_or_404(Product, pk=pk)
    # Django ORM: SELECT * FROM catalog_product WHERE id = 3
    # If no row found → raises Http404 → Django shows 404 error page
    # If found → product is a Product instance (one row as Python object)

    return render(request, 'catalog/product_detail.html', {'product': product})
    # template accesses: {{ product.name }}, {{ product.price }}, etc.


# ══════════════════════════════════════════
# VIEW 3: Add Product (Insert new row)
# URL: GET  /products/add/  → show empty form
# URL: POST /products/add/  → save to DB
# ══════════════════════════════════════════
def add_product(request):
    if request.method == 'POST':
        # Form was submitted — data is in request.POST
        form = ProductForm(request.POST)
        # Bind submitted data to form (validates against model rules)

        if form.is_valid():
            # Validation passed:
            # - 'name' is not empty and ≤ 200 chars
            # - 'price' is a valid decimal number
            # - 'available_stock' is a positive integer

            form.save()
            # Django ORM INSERT:
            # INSERT INTO catalog_product (name, description, price, category,
            #                              available_stock, created_at)
            # VALUES ('iPhone 15', 'Latest iPhone', 79999.00, 'Electronics',
            #          50, '2025-04-29 16:30:00');
            # 'created_at' is auto-filled by Django (auto_now_add=True)

            messages.success(request, 'Product added successfully!')
            # Flash message — shows as a green alert on the next page

            return redirect('product-list')
            # Redirect to /products/ after successful save
            # POST → Redirect → GET pattern:
            #   Without redirect: refreshing page re-submits the form → duplicate products

    else:
        # GET request: user just opened /products/add/
        form = ProductForm()
        # Create an empty form with no data

    return render(request, 'catalog/product_form.html', {
        'form': form,
        'title': 'Add New Product'
    })
    # Rendered for both:
    # 1. Initial GET — shows blank form
    # 2. Invalid POST — shows form WITH error messages highlighted
```

---

## 📄 urls.py — Line by Line

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product-list'),
    # '' = no suffix → /products/ (after project prefix 'products/')
    # name='product-list' → used in templates: {% url 'product-list' %}
    #                     → used in views: redirect('product-list')

    path('add/', views.add_product, name='add-product'),
    # Matches /products/add/
    # Static segment — always matches this exact string

    path('<int:pk>/', views.product_detail, name='product-detail'),
    # <int:pk> = URL parameter converter
    # 'int:' → only matches integers (rejects non-numeric URLs)
    # 'pk'   → the captured value is passed as keyword argument 'pk'
    # /products/5/ → calls product_detail(request, pk=5)
    # /products/abc/ → does NOT match → 404
]
```

---

## 📄 Templates — Key Lines Explained

### `product_list.html`
```html
{% extends 'catalog/base.html' %}
<!-- Template inheritance: this file gets navbar + Bootstrap from base.html -->

{% block content %}
<!-- Fills the {% block content %} placeholder in base.html -->

{{ products|length }}
<!-- Template filter: like Python's len(). Shows total count of products -->

{% for product in products %}
<!-- Loops over every Product object in the QuerySet -->

{{ product.description|truncatewords:15 }}
<!-- |truncatewords:15 — shows first 15 words then adds "..." -->
<!-- Useful for card-style previews of long descriptions -->

{% url 'product-detail' product.pk %}
<!-- Reverse URL lookup: generates /products/3/ for product.pk=3 -->
<!-- NEVER hardcode URLs — use {% url %} so changes in urls.py auto-update -->

{% if product.available_stock > 0 %}
    <span class="text-success">{{ product.available_stock }} units</span>
{% else %}
    <span class="text-danger">Out of Stock</span>
{% endif %}
<!-- Conditional rendering based on stock level -->
```

### `product_detail.html`
```html
{{ product.created_at|date:"d M Y, h:i A" }}
<!-- |date filter formats DateTimeField to human-readable string -->
<!-- "d M Y" = day month year → "29 Apr 2025" -->
<!-- "h:i A" = 12hr:min AM/PM → "04:30 PM" -->
<!-- Output: "29 Apr 2025, 04:30 PM" -->
```

### `product_form.html`
```html
<form method="POST">
    {% csrf_token %}
    <!-- MANDATORY in every POST form -->
    <!-- Inserts hidden field: <input name="csrfmiddlewaretoken" value="..."> -->
    <!-- Django middleware validates this token on every POST -->
    <!-- Protects against CSRF attacks -->

    {% for field in form %}
    <!-- Loops over each form field: name, description, price, category, stock -->

        {{ field.label }}
        <!-- Auto-generated label: "Available Stock" from field name "available_stock" -->

        {{ field }}
        <!-- Renders the HTML input widget for this field -->
        <!-- Uses the widget defined in forms.py: TextInput, Textarea, NumberInput etc. -->

        {% for error in field.errors %}
            {{ error }}
        <!-- field.errors: list of validation messages for failed fields -->
        <!-- Example: "Ensure this value is greater than or equal to 0." -->
        {% endfor %}
    {% endfor %}
```

---

## 📁 Final File Structure

```
catalog/                           ← Django App
├── models.py                      — Product model
├── forms.py                       — ProductForm (ModelForm)
├── views.py                       — product_list, product_detail, add_product
├── urls.py                        — 3 URL patterns
├── admin.py                       — ProductAdmin
└── templates/catalog/
    ├── base.html                  — Navbar + Bootstrap layout
    ├── product_list.html          — Card grid of all products
    ├── product_detail.html        — Full info for one product
    └── product_form.html          — Add product form
```

---

## ✅ Checklist: What the Question Asks vs What's Implemented

| Requirement | Implemented | How |
|---|---|---|
| MVT Architecture | ✅ | Model, View, Template each in separate files |
| SQLite Database | ✅ | Default Django setting — no config needed |
| `name` field | ✅ | `CharField(max_length=200)` |
| `description` field | ✅ | `TextField()` |
| `price` field | ✅ | `DecimalField(max_digits=10, decimal_places=2)` |
| `category` field | ✅ | `CharField(max_length=100)` |
| `available_stock` field | ✅ | `PositiveIntegerField(default=0)` |
| `created_at` field | ✅ | `DateTimeField(auto_now_add=True)` |
| Add new products | ✅ | `add_product` view + `product_form.html` |
| List all products | ✅ | `product_list` view + `product_list.html` |
| View detail by ID | ✅ | `product_detail(pk)` view + `product_detail.html` |
| URL routing | ✅ | 3 URLs: `''`, `add/`, `<int:pk>/` |
| HTML Templates | ✅ | 4 templates with DTL |
| ORM for insert | ✅ | `form.save()` → INSERT |
| ORM for retrieve | ✅ | `.all()` and `get_object_or_404(pk)` → SELECT |

---

## 🔑 Key Differences from IA Questions

| | IA (Q1/Q2) | PYQ (End Sem) |
|---|---|---|
| Database | PostgreSQL | **SQLite** (default) |
| Install needed | `psycopg2-binary` | **Nothing extra** |
| Operations | Full CRUD | **Insert + Retrieve only** |
| Models | Student / Book+Member+IssueRecord | **Single Product model** |
| Special features | Search, unique email, issue/return | **Detail view by ID** |
