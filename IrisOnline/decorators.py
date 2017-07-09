from django.shortcuts import render


def require_admin(func):
    def handle_request(request):
        if request.user.is_superuser:
            return func(request)
        else:
            return render(request, 'lost_customer.html')
    return handle_request


def require_customer(func):
    def handle_request(request):
        if request.user.is_superuser:
            return render(request, 'lost_admin.html')
        else:
            return func(request)
    return handle_request