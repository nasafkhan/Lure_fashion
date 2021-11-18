from django import forms

from brands.models import Brand
class BrandForm(forms.ModelForm):

    # brand_logo = reciept=forms.ImageField( widget = forms.Select(attrs = {'onchange' : "myFunction();"}))

    class Meta:
        model = Brand
        fields = ('brand_name', 'slug', 'description', 'brand_logo',)

class EditBrand(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('brand_name', 'slug', 'description', 'brand_logo',)