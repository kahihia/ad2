from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^stalls/(?P<stall_id>(\d+))/$', views.StallView.as_view()),
    url(r'^search/$', views.search),
]