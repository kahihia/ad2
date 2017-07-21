from django.shortcuts import render, Http404
from django.views import View
from django.contrib.auth.decorators import login_required
from IrisOnline.decorators import customer_required
from product_catalog.contexts import make_context
from .models import *
from customer_profile.models import Customer
from django.http import HttpResponse


class ConfirmPaymentView(View):
    @staticmethod
    @login_required()
    @customer_required
    def post(request):
        if 'deposit_slip' not in request.FILES or "date" not in request.POST:
            return HttpResponse(status=400)

        try:
            customer = Customer.objects.get(user=request.user)
        except:
            Http404('Could not get Customer object')
            return

        try:
            order_id = request.POST.get('order-id')
            order = Order.objects.get(id=order_id)
        except:
            Http404('Could not find order')
            return

        date_paid = request.POST.get('date'),
        deposit_slip = request.FILES.get('deposit-slip')

        print(date_paid)


        customer.customerpaymentdetails_set.create(customer=customer,
                                                   parent_order=order,
                                                   deposit_slip=deposit_slip,
                                                   date=date_paid)
        return HttpResponse(200)

