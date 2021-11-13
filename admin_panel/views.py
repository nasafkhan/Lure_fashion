from django.shortcuts import redirect, render
from django.contrib import messages
from brands.models import Brand
from brands.forms import BrandForm
from category.models import Category
from category.forms import CategoryForm
from products.models import Product
from products.forms import ProductForm
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
    form = ProductForm()
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Product added successfully')
        else:

            messages.error(request, 'Form submission failed')
        return redirect("add_product")
    context = {
        'form': form
    }

    return render(request, 'adminpanel/products/add_product.html', context )




def all_brands(request):
    brands = Brand.objects.all()

    context = {
        'brands' : brands
    }
    return render(request, 'adminpanel/brands/all_brands.html', context)

def add_brand(request):
    form = BrandForm()

    if request.method == 'POST':
        brand_form = BrandForm(request.POST, request.FILES)

        if brand_form.is_valid():
            brand_form.save()
            messages.success(request, 'Brand added successfully')
        else:
            messages.error(request, 'Form submission failed')
        
        return redirect('add_brand')

    context = {
        'form' : form
    }
    return render(request, 'adminpanel/brands/add_brand.html', context)


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        category_form = CategoryForm(request.POST, request.FILES)

        if category_form.is_valid():
            category_form.save()
            messages.success(request, 'Category added successfully')
        else:
            messages.error(request, 'Form submission failed')

        return redirect('add_category')

    context = {
        'form': form
    }

    return render(request, 'adminpanel/categories/add_category.html', context)
        


def all_categories(request):
    categories = Category.objects.all()

    context = {
        'categories' : categories
    }
    return render(request, 'adminpanel/categories/all_categories.html', context)