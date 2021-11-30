from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('active_users/', views.active_users, name='active_users'),

    path('all_products/', views.all_products, name='all_products'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<prod_id>', views.edit_product, name='edit_product'),
    path('delete_product/<prod_id>', views.delete_product, name='delete_product'),

    path('all_variants', views.all_variants, name='all_variants'),
    path('add_variant/', views.add_variant, name='add_variant'),
    path('edit_variant/<varian_id>', views.edit_variant, name='edit_variant'),
    path('delete_variant/varian_id>', views.delete_variant, name='delete_variant'),

    path('all_brands/', views.all_brands, name='all_brands'),
    path('add_brand/', views.add_brand, name='add_brand'),
    path('edit_brand/<brand_id>', views.edit_brand, name='edit_brand'),
    path('delete_brand/<brand_id>', views.delete_brand, name='delete_brand'),

    path('all_categories/', views.all_categories, name='all_categories'),
    path('add_category/', views.add_category, name='add_category'),
    path('delete_category/<category_id>', views.delete_category, name='delete_category'),
    path('edit_category/<category_id>', views.edit_category, name='edit_category'),

    path('add_product_offer/', views.add_product_offer, name='add_product_offer'),
    path('add_brand_offer/', views.add_brand_offer, name='add_brand_offer'),
    path('add_category_offer/', views.add_category_offer, name='add_category_offer'),
]