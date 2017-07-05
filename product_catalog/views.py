from django.shortcuts import render, Http404
from django.views import View
from entity_management.models import Stall, Product


class ProductCatalogView(View):
    @staticmethod
    def get(request):
        stalls = Stall.objects.all()
        products = Product.objects.all()
        return render(request, 'iris-online-home.html', {
            "stalls": stalls,
            "products": products
        })

class StallView(View):
    @staticmethod
    def get(request, stall_id):
        try:
            stall = Stall.objects.get(id=stall_id)
            products = Product.objects.all().filter(stall=stall)
        except:
            raise Http404("Stall does not exist")

        stalls = Stall.objects.all()
        return render(request, 'iris-online-home.html', {
            "stalls": stalls,
            "active_stall": stall,
            "products": products,
        })
