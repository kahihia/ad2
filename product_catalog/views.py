from django.shortcuts import render, Http404, redirect
from django.views import View
from entity_management.models import Stall, Product
from customer_profile.models import Customer
from django.db.models import Q
from IrisOnline.decorators import require_customer


def available_stalls():
    return [stall for stall in Stall.objects.all() if len(stall.product_set.all()) > 0]


class ProductCatalogView(View):
    @staticmethod
    @require_customer
    def get(request):
        stalls = available_stalls()
        products = Product.objects.all()

        context = {
            "stalls": stalls,
            "products": products,
        }

        if request.user.is_authenticated:
            user = request.user
            customer = Customer.objects.filter(user=user)[0]
            full_name = customer.full_name
            context["name"] = full_name

        return render(request, 'product_catalog.html', context)


class StallView(View):
    @staticmethod
    @require_customer
    def get(request, stall_id):
        try:
            stall = Stall.objects.get(id=stall_id)
            products = Product.objects.all().filter(stall=stall)
        except:
            raise Http404("Stall does not exist")

        stalls = available_stalls()
        return render(request, 'product_catalog.html', {
            "stalls": stalls,
            "active_stall": stall,
            "products": products,
        })


def search(request):
    if request.method != 'GET':
        return redirect('/')

    key = request.GET["search-query"]
    products = Product.objects.filter(
        Q(name__icontains=key) |
        Q(description__icontains=key)
    ).order_by("pk").reverse()

    stalls = available_stalls()
    return render(request, 'product_catalog.html', {
        "stalls": stalls,
        "products": products,
        "search_term": key
    })
