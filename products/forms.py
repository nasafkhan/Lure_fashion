from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name', 'description', 'price', 'image1', 'image2', 'image3', 'image4', 'stock', 'brand', 'category',)