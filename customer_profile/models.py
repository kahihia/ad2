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


class Wishlist(Model):
    customer = ForeignKey(Customer, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)

    @staticmethod
    def wishlist_products_for_customer(customer):
        user_wishes = Wishlist.objects.filter(customer=customer)
        return [user_wish.product for user_wish in user_wishes]

