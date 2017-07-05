from django.shortcuts import render
from django.views import View


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
        pass
