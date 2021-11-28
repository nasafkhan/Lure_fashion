from django.shortcuts import get_object_or_404, render
from products.models import Product
from category.models import Category

# Create your views here.

def home(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category=categories)
        # products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)

    context = {
            'products' : products,
            # 'products_count' : products_count
    }
    return render(request, 'user/index.html', context)
    

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug = category_slug, slug = product_slug)
        
    except Product.DoesNotExist:
        product=None
    
    context = {
        'product' : product
    }
    return render(request, 'user/product_detail.html', context)
    