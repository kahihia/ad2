from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404
from django.views import View
from IrisOnline.contexts import make_context
from IrisOnline.decorators import customer_required
from .models import *


class UserOrdersView(View):
    @staticmethod
    @login_required
    @customer_required
    def get(request):
        context = make_context(request, include_stalls_and_products=False)
        user = request.user
        customer = Customer.objects.get(user=user)

        orders = Order.objects.all().filter(customer=customer)

        pending_orders = orders.filter(status="P")
        approved_orders = orders.filter(status="A")
        shipped_orders = orders.filter(status="S")
        cancelled_orders = orders.filter(status="C")

        context.update({
            "customer": customer,
            "expand": "pending",
            "orders": {
                "pending": pending_orders,
                "processing": approved_orders,
                "shipped": shipped_orders,
                "cancelled": cancelled_orders,
            }
        })
        return render(request, 'customer_orders.html', context)


class UserWaitlistView(View):
    @staticmethod
    @login_required
    @customer_required
    def get(request):
        context = make_context(request, include_stalls_and_products=False)
        user = request.user
        customer = Customer.objects.get(user=user)

        context["waitlists"] = Waitlist.objects.filter(customer=customer)

        return render(request, 'customer_waitlist.html', context)


class OrderView(View):
    @staticmethod
    @login_required
    @customer_required
    def get(request, order_id):
        context = make_context(request, include_stalls_and_products=False)
        user = request.user
        customer = Customer.objects.get(user=user)

        try:
            order = Order.objects.get(id=order_id)
            line_items = OrderLineItems.objects.all().filter(parent_order=order_id)
        except:
            raise Http404("Something went wrong")

        orders = Order.objects.all().filter(customer=customer)

        pending_orders = orders.filter(status="P")
        approved_orders = orders.filter(status="A")
        shipped_orders = orders.filter(status="S")
        cancelled_orders = orders.filter(status="C")

        expand = order.get_status_display().lower()

        context.update({
            "line_items": line_items,
            "active_order": order,
            "customer": customer,
            "total_price": order.total_price,
            "orders": {
                "pending": pending_orders,
                "processing": approved_orders,
                "shipped": shipped_orders,
                "cancelled": cancelled_orders,
            },
            "expand": expand
        })

        return render(request, 'customer_orders.html', context)


# Create your views here.
class WaitlistView(View):
    @staticmethod
    @login_required
    @customer_required
    def get(request, product_id):
        # This is the delete function for waitlists
        delete = request.GET.get('delete')

        context = make_context(request, include_stalls_and_products=False)
        customer = Customer.objects.get(user=request.user)
        waitlists = list(Waitlist.objects.filter(customer=customer))
        context["waitlists"] = waitlists

        if not delete:
            return render(request, 'customer_waitlist.html', context)

        for waitlist in waitlists:
            if waitlist.product.id == int(product_id):
                waitlists.remove(waitlist)
                waitlist.delete()

        return render(request, 'customer_waitlist.html', context)

    @staticmethod
    @login_required
    @customer_required
    def post(request, product_id):
        user = request.user
        customer = Customer.objects.get(user=user)

        try:
            product = Product.objects.get(id=product_id)
        except:
            raise Http404

        # Waitlist only products that are out of stock
        if product.quantity == 0:
            Waitlist.objects.get_or_create(customer=customer, product=product)

            context = make_context(request)

            context.update({
                'waitlisted': product
            })

        return render(request, 'product_catalog.html', context)


class ConfirmPaymentView(View):
    @staticmethod
    @login_required()
    @customer_required
    def post(request):
        try:
            Customer.objects.get(user=request.user)
        except:
            Http404('Could not get Customer object')
        has_error = False

        context = make_context(request)



        if('photo' not in request.FILES):
            has_error = True
            context["photo_error"] = True
        if ('date' not in request.POST):
            has_error = True
            context["date_error"] = True


        if(not has_error):
            order_id = request.POST.get('order-id')
            date_paid = request.POST.get('date')
            photo = request.FILES.get('deposit-slip')

            order = Order.objects.get(id=order_id)
            context["order"] = order
            order.submit_customer_payment(deposit_photo=photo, payment_date=date_paid)

            return redirect(f"/orders/{order_id}/")

        return render(request,'customer_orders.html',context)


class CancelOrderView(View):
    @staticmethod
    @login_required
    @customer_required
    def get(request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except:
            raise Http404('Order does not exist')

        customer = Customer.objects.get(user=request.user)
        if order.customer.id != customer.id:
            raise Http404("Order not found in current user's list of orders")

        if order.status == 'P':
            # Only pending orders should be cancellable
            order.cancel()

        return redirect(f"/orders/{order_id}")
