from django.shortcuts import render
from brands.models import Brand
from category.models import Category
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
    return render(request, 'adminpanel/all_users_table.html', context)