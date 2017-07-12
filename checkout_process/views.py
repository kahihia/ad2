from django.shortcuts import render

# Create your views here.

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
