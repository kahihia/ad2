from django.shortcuts import render, Http404, redirect
from django.views import View
from entity_management.models import Stall, Product
from customer_profile.models import Customer
from django.db.models import Q


class ProductCatalogView(View):
    @staticmethod
    def get(request):
        stalls = Stall.objects.all()
        products = Product.objects.all()

        context = {
            "stalls": stalls,
            "products": products,
        }

        if request.user.is_authenticated:
            user = request.user
            customer = Customer.objects.all().filter(user=user)[0]
            full_name = customer.full_name
            context["name"] = full_name

        return render(request, 'product_catalog.html', context)


class StallView(View):
    @staticmethod
    def get(request, stall_id):
        try:
            stall = Stall.objects.get(id=stall_id)
            products = Product.objects.all().filter(stall=stall)
        except:
            raise Http404("Stall does not exist")

        stalls = Stall.objects.all()
        return render(request, 'product_catalog.html', {
            "stalls": stalls,
            "active_stall": stall,
            "products": products,
        })


def search(request):
    if request.method != 'GET':
        return redirect('/product_catalog')

    key = request.GET["search-key"]
    print(key)
    products = Product.objects.filter(

        Q(name__icontains=key) |
        Q(description__icontains=key)

    ).order_by("pk").reverse()

    print(products)
    stalls = Stall.objects.all()
    return render(request, 'product_catalog.html', {
        "stalls": stalls,
        "products": products
    })
