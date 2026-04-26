from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'available_stock', 'created_at']
    search_fields = ['name', 'category', 'description']
    list_filter = ['category']
    ordering = ['-created_at']
