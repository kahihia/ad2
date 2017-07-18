from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.EntityManagementView.as_view()),
    url(r'^stalls/(?P<stall_id>(\d+))/$', views.StallView.as_view()),
    url(r'^stalls/$', views.StallView.as_view()),
    url(r'^stalls/(?P<stall_id>(\d+))/products/$', views.ProductView.as_view()),
    url(r'^stalls/(?P<stall_id>(\d+))/products/(?P<product_id>(\d+))/$', views.ProductView.as_view()),
    url(r'^stalls/(?P<stall_id>(\d+))/products/update/$', views.update_product),
    url(r'^replenish/$', views.ReplenishView.as_view()),
    url(r'^sales-report/$', views.SalesReportView.as_view()),
    url(r'^orders-report/$', views.OrderReportView.as_view()),
    url(r'^waitlist-report/$', views.WaitlistReportView.as_view())
]

