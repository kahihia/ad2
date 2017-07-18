from django.shortcuts import render
from django.views import View
from entity_management.models import Product
from IrisOnline.decorators import customer_required
from product_catalog.contexts import make_context
import json
from django.http import HttpResponse
from customer_profile.models import Customer
from order_management.models import Order,OrderLineItems

class LineItem():
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity


class CartView(View):
    @staticmethod
    @customer_required
    def get(request):
        line_items = []

        total_price = 0.00

        for product_id, quantity in request.session["cart"]:
            product = Product.objects.get(id=product_id)
            line_items.append(LineItem(product, quantity=quantity))
            total_price += float(product.price) * float(quantity)

        context=make_context(request)
        context.update({
            "total_price": total_price,
            "line_items": line_items
        })
        return render(request, 'cart.html', context)

    @staticmethod
    @customer_required
    def delete(request):
        dict = json.loads(request.body)
        product = Product.objects.get(id=dict["product_id"])
        data = {
            "name": product.name
        }

        cart = request.session["cart"]

        # The solution in non-lambda
        # new_cart = []
        # for product_id, quantity in cart:
        #     if product.id != product_id:
        #         new_cart.append((product_id,quantity))

        #solution in lambda
        # new_cart = list(filter(lambda x: x[0] != product.id, cart))

        new_cart = [tuple for tuple in cart if tuple[0] != product.id]

        request.session["cart"] = new_cart

        return HttpResponse(
            json.dumps(data),
            content_type="application/json",
            status=400
        )

# TODO: Checkout and Purchase -h
class CheckoutView(View):
    @staticmethod
    @customer_required
    def get(request):
        line_items = []
        user = request.user
        customer = Customer.objects.get(user=user)

        total_price = 0.00
        total_quantity = 0

        for product_id, quantity in request.session["cart"]:
            product = Product.objects.get(id=product_id)
            line_items.append(LineItem(product, quantity=quantity))
            total_price += float(product.price) * float(quantity)
            total_quantity += quantity


        context=make_context(request)
        context.update({
            "total_price": total_price,
            "total_quantity": total_quantity,
            "line_items": line_items,
            "customer": customer
        })
        return render(request, 'checkout.html', context)

    @staticmethod
    @customer_required
    def post(request):
        dict = json.loads(request.body)





class PurchaseView(View):
    @staticmethod
    @customer_required
    def get(request):
        return render(request, 'purchase.html')