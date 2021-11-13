from django import forms

from brands.models import Brand

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('brand_name', 'description', 'brand_logo',)
