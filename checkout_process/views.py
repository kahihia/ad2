from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from IrisOnline.decorators import customer_required


class CheckoutView(View):
    @staticmethod
    @customer_required
    def get(request):
        # TODO: Build context
        return render(request, 'checkout.html', None)

    @staticmethod
    @customer_required
    def post(request):
        # TODO
        pass
