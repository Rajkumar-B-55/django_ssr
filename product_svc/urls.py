from django.urls import path
from . import views

''
urlpatterns = [
    path('products_create', views.product_create, name='product_create_api'),
    path('products_get/<int:pk>', views.products_get, name='product_detail_api'),
    path('products_put/<int:pk>', views.products_put, name='product_update_api'),
    path('products_del/<int:pk>', views.products_del, name='product_delete_api'),
]
