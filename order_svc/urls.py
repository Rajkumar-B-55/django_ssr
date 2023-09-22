from django.urls import path
from . import views

urlpatterns = [
    path('api/orders_add/', views.OrderAddAPI.as_view(), name='order_api_add'),
    path('api/orders_get', views.OrderGetAPI.as_view(), name='order_api_detail'),
]
