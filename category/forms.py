from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name', 'slug', 'description', 'category_image', 'category_offer',)

class EditCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name', 'slug', 'description', 'category_image', 'category_offer',)
