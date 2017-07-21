from django.contrib.auth.decorators import login_required
from IrisOnline.decorators import customer_required
from customer_profile.models import Customer
from django.shortcuts import render, Http404
from entity_management.models import Product
from django.http import HttpResponse
from django.views import View
from .models import Waitlist

# Create your views here.
class WaitlistView(View):
    @staticmethod
    @login_required
    @customer_required
    def get(request):
        # TODO: Render
        pass

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

        Waitlist.objects.get_or_create(customer=customer, product=product)
        return HttpResponse(200)
