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
        fields = ('username', 'password', 'phone_number', 'city', 'address', 'postal_code', 'full_name')
        labels = {
            "phone_number": "Phone number",
            "full_name": "Full Name",
            "city": "City",
            "address": "Address",
            "postal_code": "Postal Code"
        }
