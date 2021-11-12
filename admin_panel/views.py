from django.shortcuts import redirect, render
from django.contrib import messages
from brands.models import Brand
from category.models import Category
from products.forms import ProductForm
from products.models import Product
from accounts.models import Account

# Create your views here.
def dashboard(request):
    return render(request, 'adminpanel/dashboard.html')

def active_users(request):
    users   = Account.objects.all()

    context = {
        'users' : users
    }
    return render(request, 'adminpanel/user_management/active_users.html', context)

def all_products(request):
    products  =  Product.objects.all()

    context = {
        'products': products
    }
    return render(request, 'adminpanel/products/all_products.html', context)

def add_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.files)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Product added successfully')
        else:
            messages.error(request, 'Form submission failed')
        return redirect("adminpanel:add_product")
    return render(request, 'adminpanel/products/add_product.html')


def all_brands(request):
    brands = Brand.objects.all()

    context = {
        'brands' : brands
    }
    return render(request, 'adminpanel/brands/all_brands.html', context)

def all_categories(request):
    categories = Category.objects.all()

    context = {
        'categories' : categories
    }
    return render(request, 'adminpanel/categories/all_categories.html', context)