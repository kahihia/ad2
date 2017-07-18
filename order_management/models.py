from entity_management.models import Product
from customer_profile.models import Customer
from django.db.models import (
    Model,
    ForeignKey,
    PROTECT,
    CASCADE,
    PositiveIntegerField,
    DateTimeField,
    BooleanField,
    DecimalField
)


class Order(Model):
    date_ordered = DateTimeField(auto_now=True)
    approved = BooleanField(default=False)
    customer = ForeignKey(Customer, on_delete=CASCADE)

    def total_price(self):
        order_items = self.orderlineitems_set.all()
        total_price = 0
        for order_item in order_items:
            total_price += order_item.line_price()
        return total_price

    def has_products(self, *products):
        for product in products:
            if not self.has_product(product):
                return False
        return True

    def has_product(self, product):
        order_items = self.orderlineitems_set.all()
        for order_item in order_items:
            if order_item.product == product:
                return True
        return False


class OrderLineItems(Model):
    # TODO: Prevent product deletion when ordered
    product = ForeignKey(Product, on_delete=PROTECT)
    quantity = PositiveIntegerField(),
    parent_order = ForeignKey(Order, on_delete=CASCADE)

    def line_price(self):
        return self.product.price * self.quantity


class ProductAssociation(Model):
    root_product = ForeignKey(Product, on_delete=PROTECT)
    associated_product = ForeignKey(Product, on_delete=PROTECT)
    probability = DecimalField(decimal_places=2, max_digits=3)