from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, CustomUser, Address
from django import forms

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','email','phone_number','password1','password2']

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Nazwa użytkownika'})
        self.fields['email'].widget.attrs.update({'placeholder': 'E-Mail'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Numer telefonu'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Hasło'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Powtórz hasło', 'cols': ''})


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','email', 'phone_number']
    
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class UpdateAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['user_first_last_name','city', 'house_number', 'flat_number', 'street', 'postal_code']
