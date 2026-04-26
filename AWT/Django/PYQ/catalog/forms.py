from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'available_stock']
        # 'created_at' is excluded — auto_now_add handles it automatically

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Product description'
            }),
            # Textarea: renders <textarea> for long text input
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',     # allows decimal input like 499.99
                'placeholder': '0.00'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Electronics, Clothing'
            }),
            'available_stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
        }
