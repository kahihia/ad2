from django.shortcuts import render
from django.views import View
from IrisOnline.decorators import customer_required
from product_catalog.contexts import make_context
import json
from django.shortcuts import redirect, Http404
from django.http import HttpResponse
from order_management.models import *
import datetime


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

        context = make_context(request)
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

        new_cart = [tuple for tuple in cart if tuple[0] != product.id]

        request.session["cart"] = new_cart

        return HttpResponse(
            json.dumps(data),
            content_type="application/json",
            status=400
        )


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

        if 'product_id' not in request.POST or \
                        'quantity' not in request.POST:
            return redirect('/checkout/cart')

        product_id = request.POST['product_id']
        quantity = request.POST['quantity']

        try:
            product = Product.objects.get(id=product_id)
        except:
            raise Http404('Product not found')

        try:
            quantity = int(quantity)
        except:
            raise Http404('Quantity is not an integer')

        #TODO: Update tuple
        cart = request.session["cart"]

        for product_id, quan in cart:
            if product.id == product_id:
                quan = quantity
                request.session.modified = True




class PurchaseView(View):
    @staticmethod
    @customer_required
    def get(request):
        cart = request.session["cart"]
        order = Order()
        order.date_ordered = datetime.datetime.now().strftime('%H:%M:%S')
        order.customer = Customer.objects.get(user=request.user)
        order.save()

        for product_id, quantity in cart:
            line_item = OrderLineItems()
            line_item.product = Product.objects.get(id=product_id)
            line_item.quantity = quantity
            line_item.parent_order = order
            line_item.save()

        request.session["cart"] = []
        request.session.modified = True

        context = make_context(request)

        return render(request, 'purchase.html', context)
