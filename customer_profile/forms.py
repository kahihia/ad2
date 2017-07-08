from customer_profile.models import Customer
from django.forms.models import ModelForm
from django.forms import (
    CharField,
    PasswordInput
)


class UserForm(ModelForm):
    password = CharField(widget=PasswordInput)
    username = CharField()

    class Meta:
        model = Customer
        fields = ['username', 'password', 'phone_number', 'city', 'address', 'postal_code']
