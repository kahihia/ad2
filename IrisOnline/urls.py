"""IrisOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from customer_profile.views import (
    SignInView,
    SignUpView,
    sign_out,
    UserProfileView,
    UserOrdersView,
    OrderView,
    UserWishlistView
)
from product_catalog.views import ProductCatalogView
from entity_management.views import AdministratorSignInView, admin_sign_out

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^entity-management/', include('entity_management.urls')),
    url(r'^product-catalog/', include('product_catalog.urls')),
    url(r'^checkout/', include('checkout_process.urls')),
    url(r'^$', ProductCatalogView.as_view()),
    url(r'^customer-sign-in/', SignInView.as_view()),
    url(r'^customer-sign-up/', SignUpView.as_view()),
    url(r'^sign-out', sign_out),
    url(r'^admin-sign-in', AdministratorSignInView.as_view()),
    url(r'^admin-sign-out', admin_sign_out),
    url(r'^user-profile/$', UserProfileView.as_view()),
    url(r'^orders/$', UserOrdersView.as_view()),
    url(r'^orders/(?P<order_id>(\d+))/$', OrderView.as_view()),
    url(r'^wishlist/$', UserWishlistView.as_view())
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
