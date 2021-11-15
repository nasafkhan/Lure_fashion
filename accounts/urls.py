from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('logout/', views.logout, name='logout'),
    path('OTP_signin/', views.sign_in_with_OTP, name='otp_login'),
    path('OTP_verify/', views.verify_otp, name='verify_otp'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    
    path('403_access_deneid/', views.access_denied, name='access_denied')
]