from django.shortcuts import render, Http404, redirect
from django.views import View
from entity_management.models import Stall, Product
from django.db.models import Q
from IrisOnline.decorators import customer_required
from .models import LineItem
from .contexts import make_context
from customer_profile.models import Customer
from django.http import HttpResponse


def available_stalls():
    return [stall
            for stall in Stall.objects.all()
            if len(stall.product_set.all()) > 0]


class ProductCatalogView(View):
    @staticmethod`
    @customer_required
    def get(request):
        context = make_context(request)
        return render(request, 'product_catalog.html', context)

    # Add to cart
    @staticmethod
    @customer_required
    def post(request):

        if "product" not in request.POST or "quantity" not in request.POST:
            raise Http404("Product or quantity not in POST data")

        product_id = request.POST["product"]
        quantity = int(request.POST["quantity"])

        try:
            product = Product.objects.get(id=product_id)
        except:
            raise Http404("Product ID not in database")

        # TODO: Error when item exceeds quantity count

        if product_id in request.session["cart"]:
            request.session["cart"][product_id] += quantity
        else:
            request.session["cart"][product_id] = quantity

        request.session.modified = True
        context = make_context(request=request)

        context.update({
            'added_to_cart': product,
            'quantity': quantity,
        })

        # TODO: Compute recommendations
        return render(request, 'product_catalog.html', context)


class CartView(View):
    @staticmethod
    def get(request):
        products = []

        for product_id, quantity in request.session["cart"].items():
            product = Product.objects.get(id=product_id)
            products.append(LineItem(product, quantity=quantity))

        context = {
            "line_items": products
        }

        return render(request, 'cart.html', context)


class WishList(View):
    @staticmethod
    @customer_required
    def post(request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except:
            Http404('Product not found')
            return

        try:
            customer = Customer.objects.get(user=request.user)
        except:
            Http404('Could not get Customer object')
            return

        customer.userwish_set.create(customer, product)
        return HttpResponse(200)


class StallView(View):
    @staticmethod
    @customer_required
    def get(request, stall_id):
        try:
            stall = Stall.objects.get(id=stall_id)
        except:
            raise Http404("Stall does not exist")

        context = make_context(request, active_stall=stall)
        return render(request, 'product_catalog.html', context)


def search(request):
    if request.method != 'GET':
        return redirect('/')

    key = request.GET["search-query"]
    products = Product.objects.filter(
        Q(name__icontains=key) |
        Q(description__icontains=key)
    ).order_by("pk").reverse()

    context = make_context(request)
    context["products"] = products
    context["search_term"] = key

    return render(request, 'product_catalog.html', context)
