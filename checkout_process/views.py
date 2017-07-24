import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import Http404, redirect
from django.shortcuts import render
from django.views import View
from product_catalog.cart import Cart

from IrisOnline.contexts import make_context
from IrisOnline.decorators import customer_required
from order_management.models import *
from IrisOnline.tasks import expire
from celery.schedules import datetime, timedelta


class CartView(View):
    @staticmethod
    @login_required
    @customer_required
    def get(request):
        cart = Cart(request=request)

        context = make_context(request)
        context.update({
            "cart": cart
        })
        return render(request, 'cart.html', context)

    @staticmethod
    @login_required
    @customer_required
    def delete(request):
        json_data = json.loads(request.body)
        try:
            product_id = json_data['product_id']
        except:
            return HttpResponseBadRequest()  # Product ID Not Found

        Cart(request=request).remove_product(product_id)

        request.session.modified = True
        return HttpResponse(200)

    @staticmethod
    @login_required
    @customer_required
    def post(request):

        try:
            json_data = json.loads(request.body)
            product_id = json_data['product_id']
            quantity = int(json_data['quantity'])
        except:
            raise Http404('Invalid JSON')

        try:
            Product.objects.get(id=product_id)
        except:
            raise Http404('Product not found')

        if quantity <= 0:
            if str(product_id) in request.session["cart"]:
                del request.session["cart"][str(product_id)]
        else:
            request.session["cart"][product_id] = quantity

        request.session.modified = True
        return HttpResponse(200)


def has_quantity_errors(line_items):
    for line_item in line_items:
        if line_item.product.quantity < line_item.quantity:
            return True

    return False


def has_dead_product_errors(line_items):
    for line_item in line_items:
        if not line_item.product.is_active:
            return True

    return False


class CheckoutView(View):
    @staticmethod
    @login_required
    @customer_required
    def get(request):
        user = request.user
        customer = Customer.objects.get(user=user)
        cart = Cart(request=request)
        line_items = cart.line_items

        if len(line_items) == 0:
            return redirect("/")

        quantity_errors = []
        out_of_stock_errors = []
        dead_products = []

        for line_item in line_items:

            product_id = line_item.product.id
            stock_count = line_item.product.quantity

            # Check if product is activated
            if not line_item.product.is_active:
                dead_products.append(line_item.product)
                cart.remove_product(product_id)
                line_items.remove(line_item)
                continue

            # Check if product is in stock
            if stock_count == 0:
                out_of_stock_errors.append(line_item.product)
                cart.remove_product(product_id)
                line_items.remove(line_item)
                continue

            # Check if inventory can support cart quantity
            if stock_count < line_item.quantity:
                quantity_errors.append(line_item.product)
                cart.update_quantity(product_id, quantity=stock_count)
                line_item.quantity = stock_count

        context = make_context(request)

        context.update({
            "total_price": cart.total_price,
            "line_items": line_items,
            "customer": customer,
            "out_of_stock_errors": out_of_stock_errors,
            "quantity_errors": quantity_errors,
            "dead_products": dead_products
        })

        return render(request, 'checkout.html', context)

    @staticmethod
    @login_required
    @customer_required
    def post(request):
        cart = Cart(request=request)
        line_items = cart.line_items
        if has_quantity_errors(line_items) or has_dead_product_errors(line_items):
            return redirect("/checkout/review/")

        cart.is_approved = True
        return redirect("/checkout/purchase-complete/")


class PurchaseView(View):
    @staticmethod
    @login_required
    @customer_required
    def get(request):
        cart = Cart(request=request)

        if not cart.is_approved:
            print("Cart is not approved")
            return redirect("/checkout/cart/")

        customer = Customer.objects.get(user=request.user)
        order = cart.convert_to_order(customer=customer)
        cart.reset_cart()
        print(order.status)
        expire.apply_async(args=(order.id,), eta=datetime.utcnow() + timedelta(days=3))

        context = make_context(request)
        context["total_price"] = order.total_price

        return render(request, 'purchase.html', context)
