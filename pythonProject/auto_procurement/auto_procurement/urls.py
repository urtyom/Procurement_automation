"""
URL configuration for auto_procurement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from big_purchases.views import UploadYAMLView, RegisterView, ProductListView, CartView, CartItemDeleteView, ContactCreateView, ConfirmOrderView, OrderHistoryView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload-yaml/', UploadYAMLView.as_view(), name='upload_yaml'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/item/<int:pk>/', CartItemDeleteView.as_view(), name='cart-item-delete'),
    path('contacts/', ContactCreateView.as_view(), name='contact-create'),
    path('order/confirm/', ConfirmOrderView.as_view(), name='order-confirm'),
    path('orders/history/', OrderHistoryView.as_view(), name='order-history'),
]
