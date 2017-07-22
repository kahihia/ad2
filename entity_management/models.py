from datetime import datetime
from django.dispatch import receiver
from order_management.models import Waitlist
from django.db.models.signals import post_save
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

    def change_price(self, new_price):
        current_price_history = self.pricehistory_set.filter(effective_to=None)[0]
        current_price_history.effective_to = datetime.now()
        current_price_history.save()
        self.pricehistory_set.create(price=new_price)

    def price_for_date(self, date):
        self.pricehistory_set.filter(effective_from__gte=date).order_by()


        price_history = self.pricehistory_set.get(
            Q(effective_to__gte=date) | Q(effective_to=None),
            Q(effective_from__lte=date),
        )

        return price_history.price

    def __str__(self):
        return f"{self.name} - {self.stall}"


@receiver(post_save, sender=Product)
def on_product_save(sender, instance, created, **kwargs):
    if instance.quantity == 0:
        # Cannot fulfill waitlists with an empty inventory
        return

    waitlists = Waitlist.waitlist_for_product(product=instance)

    for waitlist in waitlists:
        if instance.quantity == 0:
            # Cannot fulfill the rest of the waitlists
            break

        waitlist.convert_to_order()
        instance.quantity -= 1

    instance.save()


class PriceHistory(Model):
    product = ForeignKey(Product)
    price = DecimalField(decimal_places=2, max_digits=10)
    effective_from = DateTimeField(auto_now_add=True)
    effective_to = DateTimeField(null=True, default=None)

    def __str__(self):
        return f"{self.price} - {self.effective_from} to {self.effective_to}"

