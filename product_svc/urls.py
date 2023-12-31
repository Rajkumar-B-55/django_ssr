from django.urls import path
from . import views

''
urlpatterns = [
    path('api/products_create', views.ProductAddAPI.as_view(), name='product_create_api'),
    path('api/products_get/<int:pk>', views.ProductGetAPI.as_view(), name='product_detail_api'),
    path('api/products_put/<int:pk>', views.ProductPutAPI.as_view(), name='product_update_api'),
    path('api/products_del/<int:pk>', views.ProductDeleteAPI.as_view(), name='product_delete_api'),
]
