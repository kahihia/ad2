from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from .models import *
from django.shortcuts import Http404
from django.http import HttpResponse
import json
from IrisOnline.decorators import admin_required
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from order_management.views import *


def admin_sign_out(request):
    logout(request)
    return redirect('/admin-sign-in/')


class AdministratorSignInView(View):
    @staticmethod
    def get(request):
        if request.user.is_superuser:
            return redirect(to='/entity-management/')
        return render(request, 'admin_sign_in.html')

    @staticmethod
    def post(request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is None:
            return render(request, 'admin_sign_in.html', {
                'error': 'Invalid Credentials'
            })
        elif not user.is_superuser:
            return render(request, 'admin_sign_in.html', {
                'error': 'Customer account entered'
            })
        else:
            login(request, user)
            return redirect('/entity-management/')


class EntityManagementView(View):
    @staticmethod
    @login_required(login_url='/admin-sign-in/')
    @admin_required
    def get(request):
        stalls = Stall.objects.all()
        return render(request, 'entity_management.html', {
            "stalls": stalls,
            "username": request.user.username
        })


class ProductView(View):
    @staticmethod
    def post(request, stall_id):

        if 'photo' not in request.FILES:
            return HttpResponse(status=400)

        dict = {
            "product_name": request.POST.get('name'),
            "description": request.POST.get('description'),
            "price": request.POST.get('price'),
            "quantity": request.POST.get('quantity')
        }

        errors = handle_errors(dict)
        print(not errors)

        if not errors:
            new_product = Product.objects.create(name=dict["product_name"],
                                                 description=dict["description"],
                                                 photo=request.FILES.get('photo'),
                                                 stall=Stall.objects.get(id=stall_id),
                                                 quantity=dict["quantity"])

            PriceHistory.objects.create(product=new_product, price=dict["price"])

            data = {
                "new_product": new_product.name
            }

            return HttpResponse(
                json.dumps(data),
                content_type="application/json"
            )

        return HttpResponse(
            json.dumps(errors),
            content_type="application/json",
            status=400
        )

    @staticmethod
    def delete(request, stall_id):
        dict = json.loads(request.body)
        product = Product.objects.get(id=dict["product_id"])
        data = {
            "name": product.name
        }
        product.is_active = False
        product.save()

        return HttpResponse(
            json.dumps(data),
            content_type="application/json",
            status=400
        )


class StallView(View):
    @staticmethod
    @login_required
    @admin_required
    def get(request, stall_id):
        try:
            stall = Stall.objects.get(id=stall_id)
            products = Product.objects.all().filter(stall=stall,is_active=True)
        except:
            raise Http404("Stall does not exist")

        stalls = Stall.objects.all()
        return render(request, 'entity_management.html', {
            "stalls": stalls,
            "active_stall": stall,
            "products": products,
        })

    @staticmethod
    @login_required
    @admin_required
    def post(request):
        dict = json.loads(request.body)
        new_stall = Stall()
        new_stall.name = dict["stall_name"]
        new_stall.save()

        data = {
            "new_stall": new_stall.name
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

    @staticmethod
    def put(request, stall_id):
        dict = json.loads(request.body)
        try:
            stall = Stall.objects.get(pk=stall_id)
            print(stall)
            old_name = stall.name  # old name stored for debugging purposes (sent in JSON response)
            stall.name = dict["modified_name"]
            stall.save()

        except:
            raise Http404("Stall does not exist")
        data = {
            "old_name": old_name,
            "new_name": stall.name
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

    @staticmethod
    def delete(self, stall_id):

        try:
            Stall.objects.get(pk=stall_id).delete()

        except:
            raise Http404("Stall does not exist")

        data = {

        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )


def handle_errors(dict):
    errors = []
    if is_invalid(dict["product_name"]):
        errors.append("Error Missing: Name field required")
    if is_invalid(dict["price"]):
        errors.append("Error Missing: Price field required")
    if is_invalid(dict["quantity"]):
        errors.append("Error Missing: Quantity field required")
    if is_invalid(dict["description"]):
        errors.append("Error Missing: Description field required")

    return errors


def is_invalid(item):
    return item is None or item == ""


def update_product(request, stall_id):
    request_data = {
        "product_name": request.POST.get('name'),
        "description": request.POST.get('description'),
        "price": request.POST.get('price'),
        "quantity": request.POST.get('quantity')
    }

    errors = handle_errors(request_data)
    print(errors)

    if not errors:
        product = Product.objects.get(id=request.POST.get("product_id"))
        product.name = request_data["product_name"]
        product.description = request_data["description"]
        product.price = request_data["price"]
        product.quantity = request_data["quantity"]
        if 'photo' in request.FILES:
            product.photo = request.FILES.get('photo')
        product.save()

        data = {
            "product": product.name
        }

        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

    return HttpResponse(
        json.dumps(errors),
        content_type="application/json",
        status=400
    )


def make_context(request):
    username = request.user.username
    return {
        "username": username
    }


# TODO: replenish shows low and out of stock, reports are self explanatory
class ReplenishView(View):
    @staticmethod
    @login_required
    @admin_required
    def get(request):
        return render(request, 'replenish_stocks.html', make_context(request))

    @staticmethod
    @login_required
    @admin_required
    def post(request):
        pass


class SalesReportView(View):
    @staticmethod
    @login_required
    @admin_required
    def get(request):
        return render(request, 'sales_report.html', make_context(request))


class OrderReportView(View):
    @staticmethod
    @login_required
    @admin_required
    def get(request):
        context = make_context(request)

        orders = Order.objects.all()

        pending_orders = orders.filter(status="P")
        approved_orders = orders.filter(status="A")
        shipped_orders = orders.filter(status="S")
        cancelled_orders = orders.filter(status="C")

        context.update({
            "orders": {
                "Pending": pending_orders,
                "Processing": approved_orders,
                "Shipped": shipped_orders,
                "Cancelled": cancelled_orders,
            },
            "selected_type": orders
        })

        return render(request, 'orders_report.html', context)


class OrderTypeView(View):
    @staticmethod
    @login_required
    @admin_required
    def get(request, order_type):
        context = make_context(request)
        orders = Order.objects.all()

        try:
            status = Order.ORDER_STATUSES
            for key, value in status:
                if order_type == value:
                    selected_type = orders.filter(status=key)
        except:
            raise Http404("Order type does not exist!")

        pending_orders = orders.filter(status="P")
        approved_orders = orders.filter(status="A")
        shipped_orders = orders.filter(status="S")
        cancelled_orders = orders.filter(status="C")

        context.update({
            "orders": {
                "Pending": pending_orders,
                "Processing": approved_orders,
                "Shipped": shipped_orders,
                "Cancelled": cancelled_orders,
            },
            "selected_type": selected_type
        })

        return render(request, 'orders_report.html', context)


class WishlistReportView(View):
    @staticmethod
    @login_required
    @admin_required
    def get(request):
        return render(request, 'wishlist_report.html', make_context(request))


# TODO: Confirm payments received from customers
class ConfirmPaymentsView(View):
    @staticmethod
    @login_required
    @admin_required
    def get(request):
        return render(request, 'confirm_payments.html', make_context(request))
