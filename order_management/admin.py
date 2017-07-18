from django.contrib import admin
from .models import *


admin.site.register(Order)
admin.site.register(OrderLineItems)
admin.site.register(ProductAssociation)