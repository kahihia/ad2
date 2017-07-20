from entity_management.models import Stall, Product
from customer_profile.models import Customer


def available_stalls():
    return [stall for stall in Stall.objects.all()
            if len(stall.product_set.all()) > 0]


def make_context(request, active_stall=None, include_stalls_and_products=True):
    cart_count = get_cart_count(request)
    name = get_user_name(request)

    context = {
        'cart_count': cart_count,
        'name': name
    }

    if include_stalls_and_products:
        stalls = available_stalls()

        if active_stall:
            products = Product.objects.all().filter(stall=active_stall)
        else:
            active_stall = None
            products = Product.objects.all()

        context.update({
            'products': products,
            'stalls': stalls,
            'active_stall': active_stall,
        })

    return context


def get_user_name(request):
    if request.user.is_authenticated:
        user = request.user
        customer = Customer.objects.get(user=user)
        return customer.full_name
    else:
        return None


def get_cart_count(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}
        cart_count = 0
        request.session.modified = True
    else:
        cart_count = len(request.session['cart'])

    return cart_count
