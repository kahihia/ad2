from entity_management.models import Stall, Product
from customer_profile.models import Customer, Wishlist
from order_management.models import Waitlist
from product_catalog.cart import Cart


def available_stalls():
    return [stall for stall in Stall.objects.all()
            if len(stall.product_set.all()) > 0]


def make_context(request, active_stall=None, include_stalls_and_products=True):
    cart = Cart(request=request)
    name = get_user_name(request)

    context = {
        'cart': cart,
        'name': name
    }

    if include_stalls_and_products:
        stalls = available_stalls()

        if active_stall:
            products = Product.objects.filter(stall=active_stall, is_active=True)
        else:
            active_stall = None
            products = Product.objects.filter(is_active=True)

        out_of_stock = products.filter(quantity=0)

        if request.user.is_authenticated:
            user = request.user
            customer = Customer.objects.get(user=user)
            user_wishlist = Wishlist.wishlist_products_for_customer(customer=customer)
            user_waitlists = Waitlist.waitlist_products_for_customer(customer=customer)

            context.update({
                'wishlist': user_wishlist,
                'waitlist': user_waitlists
            })

        context.update({
            'products': products,
            'stalls': stalls,
            'active_stall': active_stall,
            'out_of_stock': out_of_stock
        })

    return context


def get_user_name(request):
    if request.user.is_authenticated:
        user = request.user
        customer = Customer.objects.get(user=user)
        return customer.full_name
    else:
        return None
