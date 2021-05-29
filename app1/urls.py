from django.urls import path
from app1 import views

urlpatterns = [

    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('otp', views.otp, name='otp'),
]