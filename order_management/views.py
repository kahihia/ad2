from django.shortcuts import render, Http404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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
        print(context["waitlists"])

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

        context = make_context(request)

        # Waitlist only products that are out of stock
        if product.quantity == 0:
            Waitlist.objects.get_or_create(customer=customer, product=product)

            context.update({
                'waitlisted': product
            })

        return render(request, 'product_catalog.html', context)


class ConfirmPaymentView(View):
    @staticmethod
    @login_required()
    @customer_required
    def post(request):
        if 'deposit_slip' not in request.FILES or "date" not in request.POST:
            return HttpResponse(status=400)

        try:
            Customer.objects.get(user=request.user)
        except:
            Http404('Could not get Customer object')
            return

        try:
            order_id = request.POST.get('order-id')
            Order.objects.get(id=order_id)
        except:
            Http404('Could not find order')
            return

        date_paid = request.POST.get('date'),
        deposit_slip = request.FILES.get('deposit-slip')
        print(date_paid)


# kams code
# if 'deposit_slip' not in request.FILES or "date" not in request.POST:
#     return HttpResponse(status=400)
#
# try:
#     customer = Customer.objects.get(user=request.user)
# except:
#     Http404('Could not get Customer object')
#     return
#
# try:
#     order_id = request.POST.get('order-id')
#     order = Order.objects.get(id=order_id)
# except:
#     Http404('Could not find order')
#     return
#
# date_paid = request.POST.get('date'),
# deposit_slip = request.FILES.get('deposit-slip')
#
# print(date_paid)

# customer = Customer.objects.get(user=request.user)
#
# customer.customerpaymentdetails_set.create(customer=customer,
#                                            parent_order=order,
#                                            deposit_slip=deposit_slip,
#                                            date=date_paid)
#
# return redirect('/orders')


#   Amount  Measure       Ingredient -- Preparation Method
#  --------  ------------  --------------------------------
#     3      kg            dog meat -- * see note
#     1 1/2  cups          vinegar
#    60                    peppercorns -- crushed
#     6      tablespoons   salt
#    12      cloves        garlic -- crushed
#       1/2  cup           cooking oil
#     6      cups          onion -- sliced
#     3      cups          tomato sauce
#    10      cups          boiling water
#     6      cups          red pepper -- cut into strips
#     6      pieces        bay leaf
#     1      teaspoon      tabasco sauce
#     1 1/2  cups          liver spread -- ** see note
#     1      whole         fresh pineapple -- cut 1/2 inch thick
#
#  1. First, kill a medium sized dog, then burn off the fur over a hot fire.
#  2. Carefully remove the skin while still warm and set aside for later (may be
# used in other recpies)
#  3. Cut meat into 1″ cubes. Marinade meat in mixture of vinegar, peppercorn, salt
# and garlic for 2 hours.
#  4. Fry meat in oil using a large wok over an open fire, then add onions and
# chopped pineapple and suate until tender.
#  5. Pour in tomato sauce and boiling water, add green peper, bay leaf and tobasco.
#  6. Cover and simmer over warm coals until meat is tender. Blend in liver spread
# and cook for additional 5-7 minutes.
#
#  * you can substiture lamb for dog. The taste is similar, but not as pungent.
#  ** smooth liver pate will do as well.