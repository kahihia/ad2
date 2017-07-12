from django.forms import ModelForm

from .models import Stall


class StallForm(ModelForm):
    class Meta:
        model = Stall
        fields = ['name']
