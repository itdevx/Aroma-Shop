from codecs import namereplace_errors
from django.urls import path
from account import views

app_name = 'account'


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('dashboard/profile/', views.DashboardProfile.as_view(), name='profile'),
    path('dashboard/all-users/', views.AllUser.as_view(), name='all-users')
]