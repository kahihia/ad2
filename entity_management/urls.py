from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.EntityManagementView.as_view()),
    url(r'^stalls/(?P<stall_id>(\d+))/$', views.StallView.as_view()),
    url(r'^stalls/$', views.StallView.as_view())

]

