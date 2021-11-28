from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model= Order
        fields = ['first_name', 'last_name', 'company_name', 'phone','email', 
                  'address_line1', 'address_line2', 'landmark', 'city', 'state', 'postcode', 'order_notes']


