from django.contrib.auth.models import User
from django.db.models import (
    Model,
    CharField,
    OneToOneField
)


class Customer(Model):
    user = OneToOneField(User)
    phone_number = CharField(max_length=64)
    city = CharField(max_length=64)
    address = CharField(max_length=1024)
    postal_code = CharField(max_length=32)

