from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('loginBOUTOUN/', views.login_view, name='login'),
    path('registerBOUTOUN/', views.register_view, name='register'),
    path("login/", views.login_page),
    path("home/",views.home_page),
    
]