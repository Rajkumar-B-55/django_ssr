from django.urls import path
from . import views

urlpatterns = [
    path('api/orders_get', views.order_list, name='order_api_detail'),
    path('place_order', views.place_order, name='place_order_api'),
    path('update_order_status/<str:uuid>', views.order_update_status, name='order_update_status_api'),
]
