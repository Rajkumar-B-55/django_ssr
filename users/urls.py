from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('api/login/', views.ObtainTokenView.as_view(), name='obtain_token'),
    path('api/register/', views.RegisterUser.as_view(), name='register_user'),
    path('api/update/', views.UpdateUser.as_view(), name='update_user'),
    path('api/profile/', views.GetUser.as_view(), name='user_profile'),
    path('api/list_user/', views.ListUsers.as_view(), name='list_user'),
    path('api/week_count/', views.GetCountUserByWeek.as_view(), name='user_weekly_count'),
    path('api/month_count/', views.GetCountUserByMonth.as_view(), name='user_monthly_count'),
    path('api/total_count/', views.GetTotalCount.as_view(), name='total_user_count'),
]
