from django.forms import ModelForm
from .models import ContactModel
from django import forms

class CreateConctactForm(forms.ModelForm):
    
    class Meta:
        model = ContactModel
        fields = ['name','email','title','content']

    def __init__(self, *args, **kwargs):
        super(CreateConctactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-field', 'placeholder': 'Imię i nazwisko*'})
        self.fields['email'].widget.attrs.update({'class': 'form-field', 'placeholder': 'E-Mail*'})
        self.fields['title'].widget.attrs.update({'class': 'form-field', 'placeholder': 'Temat*'})
        self.fields['content'].widget.attrs.update({'class': 'form-field', 'placeholder': 'Treść wiadomości*', 'cols': ''})