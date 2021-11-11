from django.shortcuts import render
from brands.models import Brand
from category.models import Category
from products.models import Product
from accounts.models import Account

# Create your views here.
def dashboard(request):
    products   = Product.objects.all()
    brands     = Brand.objects.all()
    categories = Category.objects.all()
    users      = Account.objects.all()

    context = {
        'products'   : products,
        'brands'     : brands,
        'categories' : categories,
        'users'      : users
    }
    return render(request, 'adminpanel/dashboard.html', context)