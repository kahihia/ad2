from django.shortcuts import render
from django.views import View
from entity_management.models import Product
from IrisOnline.decorators import customer_required
from product_catalog.contexts import make_context

class LineItem():
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity


class CartView(View):
    @staticmethod
    @customer_required
    def get(request):
        line_items = []

        total_price = 0.00

        for product_id, quantity in request.session["cart"]:
            product = Product.objects.get(id=product_id)
            line_items.append(LineItem(product, quantity=quantity))
            total_price += float(product.price) * float(quantity)

        context=make_context(request)
        context.update({
            "total_price": total_price,
            "line_items": line_items
        })

<<<<<<< HEAD
        context = {
            "products": products
        }

        return render(request, 'cart.html', context)


=======
        return render(request, 'cart.html', context)

# TODO: Checkout and Purchase -h
class CheckoutView(View):
    @staticmethod
    @customer_required
    def get(request):
        return render(request, 'checkout.html')


class PurchaseView(View):
    @staticmethod
    @customer_required
    def get(request):
        return render(request, 'purchase.html')
>>>>>>> 2460562e651ba9a3b1cea1f69a32b9b2d39d068f
