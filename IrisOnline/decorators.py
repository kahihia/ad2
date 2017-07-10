from django.shortcuts import render


def admin_required(func):
    def handle_request(*args, **kwargs):
        request = args[0]
        if request.user.is_superuser:
            return func(*args, **kwargs)
        else:
            return render(request, 'lost_customer.html')
    return handle_request


def customer_required(func):
    def handle_request(*args, **kwargs):
        request = args[0]
        if request.user.is_superuser:
            return render(request, 'lost_admin.html')
        else:
            return func(*args, **kwargs)
    return handle_request