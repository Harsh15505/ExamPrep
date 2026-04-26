# PYQ — E-Commerce Product Catalog

> **Exam:** Practical End Semester — April-May 2025 | PDEU, Gandhinagar
> **Subject:** Advanced Web Technology (20cp308p) | B.Tech CSE, Sem 6

---

## 🚀 Setup & Run

```bash
pip install django
django-admin startproject ecommerce_project .
python manage.py startapp catalog
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## ⚙️ settings.py Changes

```python
INSTALLED_APPS = [ ..., 'catalog' ]

# No DB changes needed — SQLite is the default!
```

**project/urls.py:**
```python
path('products/', include('catalog.urls')),
```

---

## 📁 File Structure

```
catalog/
├── models.py              — Product model (name, description, price, category, available_stock, created_at)
├── forms.py               — ProductForm (ModelForm)
├── views.py               — product_list, product_detail, add_product
├── urls.py                — 3 URL patterns
├── admin.py               — ProductAdmin
└── templates/catalog/
    ├── base.html
    ├── product_list.html  — Card grid of all products
    ├── product_detail.html — Full detail view by ID
    └── product_form.html  — Add product form
```

---

## ✅ Features

| Requirement | Status |
|---|---|
| MVT Architecture | ✅ |
| SQLite (default) | ✅ No extra config |
| Product model (all 6 fields) | ✅ |
| Add product (INSERT via ORM) | ✅ |
| List all products (SELECT via ORM) | ✅ |
| Detail view by ID | ✅ `get_object_or_404(pk)` |
| URL routing (3 URLs) | ✅ |
| HTML Templates | ✅ 4 templates |
