from codecs import namereplace_errors
from django.urls import path
from account import views

app_name = 'account'


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    # path('register/', views.register_view, name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]