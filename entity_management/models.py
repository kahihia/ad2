from django.db.models import (
    Model,
    CharField,
    DecimalField,
    ForeignKey,
    CASCADE
)


class Stall(Model):
    name = CharField(max_length = 64)

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length = 64)
    price = DecimalField(decimal_places = 2, max_digits = 10)
    stall = ForeignKey(Stall, on_delete = CASCADE)
    description = CharField(max_length = 256)

    def __str__(self):
        return f"{self.name} - {self.stall}"


class ProductTag(Model):
    product = ForeignKey(Product, on_delete = CASCADE)
    content = CharField(max_length = 64)
