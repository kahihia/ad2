from django.shortcuts import render
from django.views import View
from .models import Stall, Product
from django.shortcuts import Http404, redirect
from .forms import StallForm


class EntityManagementView(View):
    @staticmethod
    def get(request):
        stalls = Stall.objects.all()
        return render(request, 'entity_management.html', {
            "stalls": stalls
        })


class StallView(View):
    # noinspection PyBroadException
    @staticmethod
    def get(request, stall_id):
        try:
            stall = Stall.objects.get(id=stall_id)
        except:
            raise Http404("Stall does not exist")

        stalls = Stall.objects.all()
        return render(request, 'entity_management.html', {
            "stalls": stalls,
            "active_stall": stall
        })

    @staticmethod
    def post(request):
        new_stall = StallForm(request.POST)
        print(request.POST)
        if new_stall.is_valid():
            print("Valid!")
            new_stall.save()
        else:
            print("NOT VALID")
        return redirect('/entity_management/')

    @staticmethod
    def put(request):
        pass
