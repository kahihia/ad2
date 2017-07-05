from django.db.models import (
    Model,
    CharField,
    DecimalField,
    ForeignKey,
    PositiveIntegerField,
    CASCADE,
    FileField
)


class Stall(Model):
    name = CharField(max_length=64)

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=64)
    description = CharField(max_length=256)
    # photo = ImageField(default='/static/images/product.png')
    photo = FileField(null=True,blank=True, default="/static/images/product.png")
    price = DecimalField(decimal_places=2, max_digits=10)
    stall = ForeignKey(Stall, on_delete=CASCADE)
    quantity = PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.stall}"
