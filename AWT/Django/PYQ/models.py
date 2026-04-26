from django.db import models

class Product(models.Model):
    # Django auto-adds: id = AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    # TextField: stores unlimited-length text (no max_length needed)
    # DB type: TEXT — for long descriptions

    price = models.DecimalField(max_digits=10, decimal_places=2)
    # DecimalField: stores exact decimal numbers (important for money!)
    # max_digits=10: total digits (e.g., 99999999.99)
    # decimal_places=2: digits after decimal point (paise/cents)
    # Use DecimalField (not FloatField) for prices — floats have rounding errors

    category = models.CharField(max_length=100)
    # Product category: "Electronics", "Clothing", "Books", etc.

    available_stock = models.PositiveIntegerField(default=0)
    # How many units are in stock
    # PositiveIntegerField: only 0 or positive integers allowed
    # default=0: new products start with 0 stock

    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True: automatically set to NOW when product is created
    # Stores both date AND time: 2025-04-29 16:30:00
    # NOT editable — Django sets it automatically

    def __str__(self):
        return f"{self.name} (₹{self.price})"
        # Used in admin panel and shell for readable display
