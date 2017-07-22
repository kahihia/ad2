from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', UserOrdersView.as_view()),
    url(r'^(?P<order_id>(\d+))/$', OrderView.as_view()),
    url(r'^waitlist/(?P<product_id>(\d+))/$', WaitlistView.as_view()),
]
