from django.db.models import (
    Q,
    Model,
    CharField,
    DecimalField,
    ForeignKey,
    PositiveIntegerField,
    CASCADE,
    FileField,
    BooleanField,
    DateTimeField
)


class Stall(Model):
    name = CharField(max_length=64)

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=64)
    description = CharField(max_length=256)
    photo = FileField(null=True, blank=True, default="/static/images/product.png")
    stall = ForeignKey(Stall, on_delete=CASCADE)
    quantity = PositiveIntegerField(default=0)
    is_active = BooleanField(default=True)

    @property
    def current_price(self):
        price = self.pricehistory_set.filter(effective_to=None)[0]
        return price.price

    def price_for_date(self, date):
        priceHistory = self.pricehistory_set.get(
            Q(effective_to__gte=date) | Q(effective_to=None),
            Q(effective_from__lte=date),
        )[0]

        return priceHistory.price

    def __str__(self):
        return f"{self.name} - {self.stall}"


class PriceHistory(Model):
    product = ForeignKey(Product)
    price = DecimalField(decimal_places=2, max_digits=10)
    effective_from = DateTimeField(auto_now_add=True)
    effective_to = DateTimeField(null=True, default=None)

    def __str__(self):
        return f"{self.price} - {self.effective_from} to {self.effective_to}"
