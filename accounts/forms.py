from django import forms
from .models import Account

class SignupForm(forms.ModelForm):
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(attrs = {'placeholder' : 'Enter Password', 'class' : 'form-control'}))
    confirm_password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(attrs = {'Placeholder' : 'Enter Password', 'class' : 'form-control'}))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone', 'email', 'password']

    def clean(self):
        cleaned_data = super(SignupForm,self).clean()
        password = cleaned_data.get('password')
        confirm_passwrod = cleaned_data.get('confirm_password')

        if password != confirm_passwrod:
            raise forms.ValidationError(
                "Passwords does'nt match!"
            )

    def __init__(self,*args, **kwargs):
        super(SignupForm,self,).__init__(*args, kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter the first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter the last name'
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter the mobile number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter the email address'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


   
