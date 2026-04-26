from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product-list'),
    # Matches /products/
    # name='product-list' used in templates: {% url 'product-list' %}

    path('add/', views.add_product, name='add-product'),
    # Matches /products/add/

    path('<int:pk>/', views.product_detail, name='product-detail'),
    # Matches /products/3/
    # <int:pk> captures the integer ID from URL → passed to view as 'pk'
]

# In project urls.py add:
# path('products/', include('catalog.urls')),
