from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from IrisOnline.decorators import customer_required

class LineItem():
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity


class CartView(View):
    @staticmethod
    def get(request):
        products = []

        for product_id, quantity in request.session["cart"]:
            product = Product.objects.get(id=product_id)
            products.append(LineItem(product, quantity=quantity))

        print(products)
        print(products[0].product.id)

        context = {
            "products": products
        }

        return render(request, 'cart.html', context)
