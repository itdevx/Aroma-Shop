from django.urls import path
from blog import views


app_name = 'blog'


urlpatterns = [
    path('blog', views.BlogView.as_view(), name='blog'),
    path('single-blog', views.SingleBlog.as_view(), name='single-blog')
]