from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('active_users/', views.active_users, name='active_users'),
    path('all_products/', views.all_products, name='all_products'),
    path('add_product/', views.add_product, name='add_product'),
    path('all_brands/', views.all_brands, name='all_brands'),
    path('all_categories/', views.all_categories, name='all_categories'),
]