from django import forms
from .models import Account, Address, UserProfile

class SignupForm(forms.ModelForm):
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(attrs = {'placeholder' : 'Enter Password', 'class' : 'form-control'}))
    confirm_password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(attrs = {'Placeholder' : 'Enter Password', 'class' : 'form-control'}))

    class Meta:
        model = Account
        fields = ['username', 'phone', 'email', 'password']

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
        self.fields['username'].widget.attrs['placeholder'] = 'Enter the user name'
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter the mobile number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter the email address'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('username', 'phone')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class AddressForm(forms.ModelForm):
    class Meta:
        model= Address
        fields = ['first_name', 'last_name', 'company_name', 'phone','email',
                  'address_line1', 'address_line2', 'landmark', 'city', 'state', 'postcode', 'type']