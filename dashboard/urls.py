from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard_index'),
    path('users/', views.users, name='dashboard_users'),
    path('product/', views.product, name='dashboard_product'),
    path('order/', views.order, name='dashboard_order'),
]
