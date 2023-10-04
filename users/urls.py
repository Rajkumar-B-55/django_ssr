from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.ObtainTokenView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register_user'),
    path('update/', views.update_user, name='update_user'),
    path('update/<str:email>', views.UpdateUser.as_view(), name='update_user_admin'),
    path('profile/', views.get_user_profile, name='user_profile'),
    path('list_user/', views.ListUsers.as_view(), name='list_user'),
    path('week_count/', views.GetCountUserByWeek.as_view(), name='user_weekly_count'),
    path('month_count/', views.GetCountUserByMonth.as_view(), name='user_monthly_count'),
    path('total_count/', views.GetTotalCount.as_view(), name='total_user_count'),
]
