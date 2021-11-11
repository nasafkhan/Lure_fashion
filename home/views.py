from django.shortcuts import render
from products.models import Product

# Create your views here.

def home(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products' : products
    }
    return render(request, 'user/index.html', context)