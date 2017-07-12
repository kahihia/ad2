from django.shortcuts import render, Http404, redirect
from django.views import View
from entity_management.models import Stall, Product
from customer_profile.models import Customer
from django.db.models import Q
from IrisOnline.decorators import customer_required
from django.contrib.auth.decorators import login_required


def available_stalls():
    return [stall for stall in Stall.objects.all() if len(stall.product_set.all()) > 0]


class ProductCatalogView(View):
    @staticmethod
    @customer_required
    def get(request):
        stalls = available_stalls()
        products = Product.objects.all()

        if 'cart' not in request.session:
            request.session['cart'] = []
            cart_count = 0
        else:
            print(request.session["cart"])
            cart_count = len(request.session['cart'])

        context = {
            "stalls": stalls,
            "products": products,
            'cart_count': cart_count
        }

        if request.user.is_authenticated:
            user = request.user
            customer = Customer.objects.filter(user=user)[0]
            full_name = customer.full_name
            context["name"] = full_name

        return render(request, 'product_catalog.html', context)

    # Add to cart
    @staticmethod
    @customer_required
    def post(request):

        if "product" not in request.POST or "quantity" not in request.POST:
            raise Http404("Product or quantity not in POST data")

        product_id = request.POST["product"]
        quantity = request.POST["quantity"]

        try:
            product = Product.objects.get(id=product_id)
        except:
            raise Http404("Product ID not in database")

        request.session["cart"].append((product.pk, quantity))
        request.session.modified = True
        cart_count = len(request.session['cart'])
        print(request.session["cart"])

        stalls = available_stalls()
        products = Product.objects.all()

        context = {
            'added_to_cart': product,
            'cart_count': cart_count,
            'quantity': quantity,
            'stalls': stalls,
            'products': products
        }

        if request.user.is_authenticated:
            user = request.user
            customer = Customer.objects.filter(user=user)[0]
            full_name = customer.full_name
            context["name"] = full_name

        # TODO: Compute recommendations
        return render(request, 'product_catalog.html', context)


class StallView(View):
    @staticmethod
    @customer_required
    def get(request, stall_id):
        try:
            stall = Stall.objects.get(id=stall_id)
            products = Product.objects.all().filter(stall=stall)
        except:
            raise Http404("Stall does not exist")

        stalls = available_stalls()

        context = {
            "stalls": stalls,
            "active_stall": stall,
            "products": products,
        }

        if request.user.is_authenticated:
            user = request.user
            customer = Customer.objects.filter(user=user)[0]
            full_name = customer.full_name
            context["name"] = full_name

        return render(request, 'product_catalog.html', context)


def search(request):
    if request.method != 'GET':
        return redirect('/')

    key = request.GET["search-query"]
    products = Product.objects.filter(
        Q(name__icontains=key) |
        Q(description__icontains=key)
    ).order_by("pk").reverse()

    stalls = available_stalls()

    context = {
        "stalls": stalls,
        "products": products,
        "search_term": key
    }

    if request.user.is_authenticated:
        user = request.user
        customer = Customer.objects.filter(user=user)[0]
        full_name = customer.full_name
        context["name"] = full_name

    return render(request, 'product_catalog.html', context)
