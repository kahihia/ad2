from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.EntityManagementView.as_view()),

    # Entity Management
    url(r'^stalls/(?P<stall_id>(\d+))/$', views.StallView.as_view()),
    url(r'^stalls/$', views.StallView.as_view()),
    url(r'^stalls/(?P<stall_id>(\d+))/products/$', views.ProductView.as_view()),
    url(r'^stalls/(?P<stall_id>(\d+))/products/(?P<product_id>(\d+))/$', views.ProductView.as_view()),
    url(r'^stalls/(?P<stall_id>(\d+))/products/update/$', views.update_product),

    # Replenish and Waitlists
    url(r'^replenish/$', views.ReplenishView.as_view()),
    url(r'^replenish/(?P<product_id>(\d+))/$', views.ReplenishProductView.as_view()),
    url(r'^waitlists/$', views.WaitlistReportView.as_view()),

    # Reports
    url(r'^sales-report/$', views.SalesReportView.as_view()),
    url(r'^orders-report/$', views.OrderReportView.as_view()),
    url(r'^orders-report/(?P<order_type>[\w\-]+)/$', views.OrderTypeView.as_view()),

    # Confirm payments
    url(r'^confirm-payments/$', views.ConfirmPaymentsView.as_view()),
    url(r'^confirm-payments/(?P<order_id>(\d+))/approve/$', views.ApproveOrderView.as_view()),
    url(r'^confirm-payments/(?P<order_id>(\d+))/reject/$', views.RejectOrderView.as_view()),

    # Order statuses
    url(r'orders/(?P<order_id>(\d+))/set-shipped/$', views.OrderSetShipping.as_view()),
    url(r'orders/(?P<order_id>(\d+))/set-cancelled/$', views.OrderSetCancelled.as_view()),
]
