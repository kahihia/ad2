from django.shortcuts import render
from django.views import View
from .models import Stall
from django.shortcuts import Http404
from django.http import HttpResponse
import json


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
        dict = json.loads(request.body)
        new_stall = Stall()
        new_stall.name = dict["stall_name"]
        new_stall.save()

        data = {
            "new_stall": new_stall.name
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

    @staticmethod
    def put(request, stall_id):
        dict = json.loads(request.body)
        try:
            stall = Stall.objects.get(pk=stall_id)
            print(stall)
            old_name = stall.name # old name stored for debugging purposes (sent in JSON response)
            stall.name = dict["modified_name"]
            stall.save()

        except:
            raise Http404("Stall does not exist")
        data = {
            "old_name": old_name,
            "new_name": stall.name
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )


    @staticmethod
    def delete(self, stall_id):

        try:
            Stall.objects.get(pk=stall_id).delete()

        except:
            raise Http404("Stall does not exist")

        data = {

        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )
