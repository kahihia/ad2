from django.shortcuts import render, Http404
from django.views import View
from customer_profile.forms import UserForm
from django.contrib.auth.models import User
from customer_profile.models import Customer
from order_management.models import Order, OrderLineItems
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from IrisOnline.decorators import customer_required
from product_catalog.contexts import make_context


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
                'error': f'User with e-mail {username} already exists.'
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
        context = make_context(request)
        user = request.user
        customer = Customer.objects.get(user=user)

        context.update({
            "customer": customer
        })

        return render(request, 'customer_profile.html', context)


class UserOrdersView(View):
    @staticmethod
    @login_required
    @customer_required
    def get(request):
        context = make_context(request)
        user = request.user
        customer = Customer.objects.get(user=user)


        orders = Order.objects.all().filter(customer=customer)

        context.update({
            "customer": customer,
            "orders": orders
        })
        return render(request, 'customer_orders.html', context)

class OrderView(View):
    @staticmethod
    @login_required
    @customer_required
    def get(request, order_id):
        context = make_context(request)
        user = request.user
        customer = Customer.objects.get(user=user)
        try:
            order = Order.objects.get(id=order_id)
            products_ordered = OrderLineItems.objects.all().filter(parent_order=order_id)
        except:
            raise Http404("Something went wrong")

        orders = Order.objects.all().filter(customer=customer)

        # total_price = order.total_price()

        context.update({
            "products_ordered": products_ordered,
            "active_order": order,
            "orders": orders,
            "customer": customer
            # "total_price": total_price
        })
        return render(request, 'customer_orders.html', context)




# TODO: Wishlist
class UserWishlistView(View):
    @staticmethod
    @login_required
    @customer_required
    def get(request):
        context = make_context(request)
        user = request.user
        customer = Customer.objects.get(user=user)

        context.update({
            "customer": customer
        })

        return render(request, 'customer_wishlist.html', context)


def sign_out(request):
    logout(request)
    return redirect('/')


















