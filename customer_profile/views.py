from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View

from IrisOnline.contexts import make_context
from IrisOnline.decorators import customer_required
from customer_profile.forms import UserForm
from customer_profile.models import Customer
from .models import Wishlist


class SignInView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated and not request.user.is_superuser:
            return redirect(to="/")
        return render(request, 'sign_in.html', None)

    @staticmethod
    def post(request):
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['cart'] = {}
            return redirect("/")
        else:
            return render(request, 'sign_in.html', {
                "error": "Invalid Credentials"
            })


class SignUpView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return redirect(to="/")

        return render(request, 'sign_up.html', None)

    @staticmethod
    def post(request):
        form = UserForm(request.POST)

        if not form.is_valid():
            return render(request, 'sign_up.html', {
                'form': form
            })

        username = request.POST["username"]
        password = request.POST["password"]
        full_name = request.POST["full_name"]
        address = request.POST["address"]
        city = request.POST["city"]
        postal_code = request.POST["postal_code"]
        phone_number = request.POST["phone_number"]

        conflicts = User.objects.filter(username=username)
        if conflicts:
            return render(request, 'sign_up.html', {
                'error': f'User \'{username}\' already exists.'
            })

        user = User.objects.create_user(username=username, password=password)

        Customer.objects.create(user=user, phone_number=phone_number,
                                full_name=full_name, city=city,
                                address=address, postal_code=postal_code)

        login(request, user)
        request.session['cart'] = {}
        return redirect('/user-profile/')


class UserProfileView(View):
    @staticmethod
    @login_required
    @customer_required
    def get(request):
        context = make_context(request, include_stalls_and_products=False)
        user = request.user
        customer = Customer.objects.get(user=user)

        context.update({
            "customer": customer
        })

        return render(request, 'customer_profile.html', context)


class UserWishlistView(View):
    @staticmethod
    @login_required
    @customer_required
    def get(request):
        context = make_context(request)
        user = request.user
        customer = Customer.objects.get(user=user)
        products_wished = Wishlist.wishlist_products_for_customer(customer)

        context.update({
            "customer": customer,
            "products": products_wished,
            "wishlist": products_wished
        })

        return render(request, 'customer_wishlist.html', context)


def sign_out(request):
    logout(request)
    return redirect('/')
