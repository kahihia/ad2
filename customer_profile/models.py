from django.contrib.auth.models import User
from entity_management.models import Product
from django.db.models import (
    Model,
    CASCADE,
    CharField,
    ForeignKey,
    OneToOneField
)


class Customer(Model):
    user = OneToOneField(User)
    phone_number = CharField(max_length=64)
    full_name = CharField(max_length=256)
    city = CharField(max_length=64)
    address = CharField(max_length=1024)
    postal_code = CharField(max_length=32)


class UserWish(Model):
    user = ForeignKey(User, on_delete=CASCADE),
    product = ForeignKey(Product, on_delete=CASCADE)
