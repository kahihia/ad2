from entity_management.models import Product
from order_management.models import Order, OrderLineItems

class Cart:
    class LineItem:
        def __init__(self, product_id, quantity):
            self.product = Product.objects.get(id=product_id)
            self.quantity = quantity

        @property
        def total_price(self):
            return float(self.product.current_price) * float(self.quantity)

        def convert_to_order_line_item(self, order):
            self.product.quantity -= self.quantity
            self.product.save()

            OrderLineItems.objects.create(
                product=self.product,
                quantity=self.quantity,
                parent_order=order
            )

    def __init__(self, request):
        self.request = request

        if 'cart' not in request.session:
            request.session['cart'] = {}
            request.session.modified = True

    @property
    def cart(self):
        return self.request.session['cart'].items()

    @cart.setter
    def cart(self, value):
        self.request.session['cart'] = value

    @property
    def line_items(self):
        return [Cart.LineItem(product_id, quantity) for product_id, quantity in self.cart]

    @property
    def total_price(self):
        price = 0.00
        for line_item in self.line_items:
            price += line_item.total_price
        return price

    @property
    def products(self):
        return [Product.objects.get(id=product_id) for product_id, quantity in self.line_items]

    @property
    def is_approved(self):
        return self.request.session['approved'] if 'approved' in self.request.session else False

    @is_approved.setter
    def is_approved(self, value):
        self.request.session['approved'] = value
        self.mark_modified()

    def remove_product(self, product_id):
        product_id = str(product_id)
        if product_id in self.request.session['cart']:
            del self.request.session['cart'][product_id]
            self.mark_modified()

    def mark_modified(self):
        self.request.session.modified = True

    def cart_count(self):
        return len(self.cart)

    def update_quantity(self, product_id, quantity):
        self.request.session['cart'][product_id] = quantity
        self.mark_modified()

    def reset_cart(self):
        self.cart = {}
        self.is_approved = False
        self.mark_modified()

    def convert_to_order(self, customer):
        order = Order.objects.create(customer=customer)

        for line_item in self.line_items:
            line_item.convert_to_order_line_item(order=order)

        return order
