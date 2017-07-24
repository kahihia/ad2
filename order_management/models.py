from django.dispatch import receiver
from entity_management.models import Product
from customer_profile.models import Customer
from django.db.models.signals import post_save, pre_save
from django.db.models import (
    Model,
    ForeignKey,
    CASCADE,
    FileField,
    PositiveIntegerField,
    DateTimeField,
    DateField,
    CharField,
    FloatField,
)


class Order(Model):
    ORDER_STATUSES = (
        ('P', 'Pending'),
        ('A', 'Processing'),
        ('S', 'Shipped'),
        ('C', 'Cancelled')
    )

    date_ordered = DateTimeField(auto_now=True)
    customer = ForeignKey(Customer, on_delete=CASCADE)
    status = CharField(max_length=2, choices=ORDER_STATUSES, default='P')
    # customer_deposit_photo = FileField(blank=True, null=True, default=None)
    # customer_payment_date = DateField(null=True, blank=True, default=None)

    @staticmethod
    def print_orders_containing_product(product):
        orders = [order for order in Order.objects.all() if order.has_product(product)]
        for order in orders:
            print(f"Order #{order.id}")
            for line_item in order.orderlineitems_set.all():
                print(line_item.product.name)
            print()

    @property
    def total_price(self):
        order_items = self.orderlineitems_set.all()
        total_price = 0.00
        for order_item in order_items:
            total_price += float(order_item.line_price)
        return total_price

    def get_status(self):
        return self.get_status_display()

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
    product = ForeignKey(Product, on_delete=CASCADE)
    quantity = PositiveIntegerField()
    parent_order = ForeignKey(Order, on_delete=CASCADE)

    @property
    def line_price(self):
        date_ordered = self.parent_order.date_ordered
        price = self.product.price_for_date(date=date_ordered)
        return float(price) * float(self.quantity)


class ProductAssociation(Model):
    root_product = ForeignKey(Product, on_delete=CASCADE, related_name="root_product")
    associated_product = ForeignKey(Product, on_delete=CASCADE, related_name="associated_product")
    probability = FloatField()

    def __str__(self):
        return f"{self.root_product.name} to {self.associated_product.name} - {self.probability}"


class Waitlist(Model):
    product = ForeignKey(Product)
    customer = ForeignKey(Customer)
    date_added = DateTimeField(auto_now_add=True)

    @staticmethod
    def total_current_waitlist_for_product(product):
        return len(Waitlist.objects.filter(product=product))

    def __str__(self):
        return f"{self.product.name} - {self.customer.user.username}"

    def convert_to_order(self):
        order = Order.objects.create(customer=self.customer)
        OrderLineItems.objects.create(order=order, product=self.product, quantity=1)
        self.delete()

    @staticmethod
    def waitlist_products_for_customer(customer):
        return [waitlist.product for waitlist in Waitlist.objects.filter(customer=customer)]

    @staticmethod
    def waitlist_count_for_product(product):
        return len(Waitlist.objects.filter(product=product))

    def to_order(self):
        order = Order.objects.create(customer=self.customer)
        OrderLineItems.objects.create(parent_order=order,
                                      quantity=1)
        self.delete()


class WaitlistCount(Model):
    product = ForeignKey(Product)
    count = PositiveIntegerField(default=0)

    @staticmethod
    def total_waitlist_count_for_product(product):
        waitlist_count, is_created = WaitlistCount.objects.get_or_create(product=product, defaults={
            "count": 0
        })

        return waitlist_count.count

    def __str__(self):
        return f"{self.product.name} - {self.count}"


@receiver(post_save, sender=Waitlist)
def on_waitlist_save(sender, instance, created, **kwargs):
    if not created:
        return

    product_wishlisted = instance.product
    waitlist_count, is_created = WaitlistCount.objects.get_or_create(product=product_wishlisted, defaults={
        "count": 0
    })

    waitlist_count.count += 1
    waitlist_count.save()


@receiver(pre_save, sender=Product)
def on_product_save(sender, instance, **kwargs):
    if instance.quantity == 0:
        # Cannot fulfill waitlists with an empty inventory
        return

    # Sort by earlier to later
    waitlists = Waitlist.waitlist_count_for_product(product=instance).order_by('date_added')

    for waitlist in waitlists:
        if instance.quantity == 0:
            # Cannot fulfill the rest of the waitlists
            break

        waitlist.convert_to_order()
        instance.quantity -= 1


class CustomerPaymentDetails(Model):
    customer = ForeignKey(Customer, on_delete=CASCADE)
    parent_order = ForeignKey(Order, on_delete=CASCADE)
    deposit_slip = FileField(null=True, blank=True)
    date = DateTimeField(null=True, default=None)
