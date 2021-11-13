from django import froms
from django.forms import fields
from .models import Category

class CategoryForm(froms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name', 'description', 'category_image', 'category_offer',)

