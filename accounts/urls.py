from django.urls import path
from . import views

urlpatterns = [
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('logout/', views.logout, name='logout'),
    path('OTP_signin/', views.sign_in_with_OTP, name='otp_login'),
    path('OTP_verify/', views.verify_otp, name='verify_otp'),
    path('verify_account/', views.verify_account, name='verify_account'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),

    path('my_profile/', views.dashboard, name='my_profile'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    
    path('403_access_deneid/', views.access_denied, name='access_denied')
]