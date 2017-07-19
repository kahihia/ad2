from django.shortcuts import render
from django.views import View
from IrisOnline.decorators import customer_required
from product_catalog.contexts import make_context
import json
from django.shortcuts import Http404
from order_management.models import *
import datetime
from django.http import HttpResponse


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

        for product_id, quantity in request.session["cart"].items():
            product = Product.objects.get(id=product_id)
            line_items.append(LineItem(product, quantity=quantity))
            total_price += float(product.price) * float(quantity)

        context = make_context(request)
        context.update({
            "total_price": total_price,
            "line_items": line_items
        })
        return render(request, 'cart.html', context)

    @staticmethod
    @customer_required
    def delete(request):
        json_data = json.loads(request.body)
        try:
            product_id = json_data['product_id']
            del request.session['cart'][str(product_id)]
        except:
            raise Http404('Product ID Not found')

        request.session.modified = True
        return HttpResponse(200)


    @staticmethod
    @customer_required
    def post(request):

        try:
            json_data = json.loads(request.body)
            product_id = json_data['product_id']
            quantity = int(json_data['quantity'])
        except:
            raise Http404('Invalid JSON')

        try:
            product = Product.objects.get(id=product_id)
        except:
            raise Http404('Product not found')

        # TODO: Update tuple
        cart = request.session["cart"]

        print(product_id)
        print(quantity)


class CheckoutView(View):
    @staticmethod
    @customer_required
    def get(request):
        line_items = []
        user = request.user
        customer = Customer.objects.get(user=user)

        total_price = 0.00
        total_quantity = 0

        for product_id, quantity in request.session["cart"].items():
            product = Product.objects.get(id=product_id)
            line_items.append(LineItem(product, quantity=quantity))
            total_price += float(product.price) * float(quantity)
            total_quantity += quantity

        context = make_context(request)
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
        pass


class PurchaseView(View):
    @staticmethod
    @customer_required
    def get(request):
        cart = request.session["cart"]
        order = Order()
        order.date_ordered = datetime.datetime.now().strftime('%H:%M:%S')
        order.customer = Customer.objects.get(user=request.user)
        order.save()

        for product_id, quantity in cart.items():
            line_item = OrderLineItems()
            line_item.product = Product.objects.get(id=product_id)
            line_item.quantity = quantity
            line_item.parent_order = order
            line_item.save()

        request.session["cart"] = []
        request.session.modified = True

        context = make_context(request)

        return render(request, 'purchase.html', context)
