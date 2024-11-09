from django.forms import ModelForm
from .models import Rating, Comment, Order
from django import forms
from users.models import Address

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]


PAYMENT =  [
    (1, ("Zapłać teraz")),
    #(2, ("Płatnośc przy odbiorze")),
]



class OrderCreationForm(forms.Form):
    comments = forms.CharField(label="Uwagi",widget=forms.Textarea, required=False)
    choice = forms.IntegerField(widget=forms.RadioSelect(choices=PAYMENT), label = "")


class AddressOrderForm(forms.ModelForm):
    phone_number = forms.CharField(label='Numer telefonu')
    class Meta:
        model = Address
        fields =  ['user_first_last_name','phone_number','city','house_number','flat_number','street','postal_code']

