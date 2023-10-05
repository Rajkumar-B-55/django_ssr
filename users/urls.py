from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('register/', views.register_view, name='register_user'),

    path('update/', views.update_user, name='update_user'),

    path('update/<str:email>', views.update_user_view, name='update_user_admin'),

    path('delete/<str:email>', views.delete_user, name='delete_user_admin'),

    path('profile/', views.get_user_profile, name='user_profile'),

]
