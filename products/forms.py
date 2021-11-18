from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name','slug', 'description', 'price', 'image1', 'image2', 'image3', 'image4', 'stock', 'brand', 'category',)

        def __init__(self, *args,**kwargs):
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'

    
class EditProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name','slug', 'description', 'price', 'image1', 'image2', 'image3', 'image4', 'stock', 'brand', 'category',)
