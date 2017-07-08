from django.shortcuts import render
from django.views import View
from customer_profile.forms import UserForm


class SignInView(View):
    @staticmethod
    def get(request):
        return render(request, 'sign_in.html', None)

    @staticmethod
    def post(request):
        pass


class SignUpView(View):
    @staticmethod
    def get(request):
        return render(request, 'sign_up.html', None)

    @staticmethod
    def post(request):
        form = UserForm(request.POST)

        if form.is_valid():
            print("valid")
        else:
            return render(request, form.errors)



