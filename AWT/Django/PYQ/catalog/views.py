from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product
from .forms import ProductForm


def product_list(request):
    """
    View 1: Display a list of ALL products
    URL: GET /products/
    ORM: SELECT * FROM catalog_product ORDER BY created_at DESC
    """
    products = Product.objects.all()
    # .all() returns a QuerySet of every Product row in the DB
    # Ordered by '-created_at' because of Meta.ordering in model
    return render(request, 'catalog/product_list.html', {'products': products})


def product_detail(request, pk):
    """
    View 2: View detailed information for ONE product using its ID
    URL: GET /products/<pk>/
    ORM: SELECT * FROM catalog_product WHERE id = pk
    """
    product = get_object_or_404(Product, pk=pk)
    # pk comes from the URL: /products/3/ → pk=3
    # get_object_or_404: if product with this pk doesn't exist → 404 page
    # Better than .get() which causes an unhandled 500 error
    return render(request, 'catalog/product_detail.html', {'product': product})


def add_product(request):
    """
    View 3: Add a new product
    URL: GET  /products/add/  → show empty form
    URL: POST /products/add/  → process and save
    ORM: INSERT INTO catalog_product (...) VALUES (...)
    """
    if request.method == 'POST':
        # User submitted the add product form
        form = ProductForm(request.POST)
        # Bind submitted data to form for validation

        if form.is_valid():
            # All fields pass validation:
            # - name not empty, max 200 chars
            # - price is a valid decimal
            # - available_stock is a positive integer
            form.save()
            # Django ORM: INSERT INTO catalog_product (name, description, price,
            #             category, available_stock, created_at)
            #             VALUES ('Laptop', 'Fast laptop', 49999.00, 'Electronics', 10, NOW())

            messages.success(request, 'Product added successfully!')
            return redirect('product-list')
            # POST-Redirect-GET: redirect to list page
            # Prevents duplicate insert on browser refresh

    else:
        # GET request: show blank form
        form = ProductForm()

    return render(request, 'catalog/product_form.html', {
        'form': form,
        'title': 'Add New Product'
    })
