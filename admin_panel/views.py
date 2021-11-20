from django.shortcuts import redirect, render
from django.contrib import messages
from brands.models import Brand
from brands.forms import BrandForm, EditBrand
from category.models import Category
from category.forms import CategoryForm, EditCategory
from products.models import Product
from products.forms import EditProduct, ProductForm
from accounts.models import Account
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
@staff_member_required(login_url='admin_login')
def dashboard(request):
    return render(request, 'adminpanel/dashboard.html')

@staff_member_required(login_url='access_denied')
def active_users(request):
    users   = Account.objects.all()

    context = {
        'users' : users
    }
    return render(request, 'adminpanel/user_management/active_users.html', context)

@staff_member_required(login_url='access_denied')
def all_products(request):
    products  =  Product.objects.all()

    context = {
        'products': products
    }
    return render(request, 'adminpanel/products/all_products.html', context)


@staff_member_required(login_url='access_denied')
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

@staff_member_required(login_url='access_denied')
def edit_product(request,prod_id):
    edit_prod = Product.objects.get(id=prod_id)
    form = EditProduct(instance=edit_prod)
    print(form)
    if request.method == 'POST':
        form=EditProduct(request.POST, request.FILES, instance=edit_prod)
        if form.is_valid():
            try:
                form.save()
            except:
                context = {'form': form}
                return render(request,'adminpanel/products/edit_product.html', context)
            return redirect('all_products')
    
    context = {
        'form': form
    }
    return render(request,'adminpanel/products/edit_product.html', context)


@staff_member_required(login_url='access_denied')
def delete_product(request, prod_id):
    Product.objects.get(id=prod_id).delete()
    return redirect('all_products')




@staff_member_required(login_url='access_denied')
def all_brands(request):
    brands = Brand.objects.all()

    context = {
        'brands' : brands
    }
    return render(request, 'adminpanel/brands/all_brands.html', context)

@staff_member_required(login_url='access_denied')
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


@staff_member_required(login_url='access_denied')
def edit_brand(request,brand_id):
    edit_bran = Brand.objects.get(id=brand_id)
    form = EditBrand(instance=edit_bran)
    print(form)
    if request.method == 'POST':
        form=EditBrand(request.POST, request.FILES, instance=edit_bran)
        if form.is_valid():
            try:
                form.save()
            except:
                context = {'form': form}
                return render(request,'adminpanel/brands/edit_brands.html', context)
            return redirect('all_brands')
    
    context = {
        'form': form
    }
    return render(request,'adminpanel/brands/edit_brands.html', context)


@staff_member_required(login_url='access_denied')
def delete_brand(request, brand_id):
    Brand.objects.get(id=brand_id).delete()
    return redirect('all_brands')



@staff_member_required(login_url='access_denied')
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
        


@staff_member_required(login_url='access_denied')
def all_categories(request):
    categories = Category.objects.all()

    context = {
        'categories' : categories
    }
    return render(request, 'adminpanel/categories/all_categories.html', context)


@staff_member_required(login_url='access_denied')
def edit_category(request,category_id):
    edit_cate = Category.objects.get(id=category_id)
    form = EditCategory(instance=edit_cate)
    print(form)
    if request.method == 'POST':
        form=EditCategory(request.POST, request.FILES, instance=edit_cate)
        if form.is_valid():
            try:
                form.save()
            except:
                context = {'form': form}
                return render(request,'adminpanel/categories/edit_category.html', context)
            return redirect('all_categories')
    
    context = {
        'form': form
    }
    return render(request,'adminpanel/categories/edit_category.html', context)

@staff_member_required(login_url='access_denied')
def delete_category(request, category_id):
    Category.objects.filter(id=category_id).delete()
    return redirect('all_categories')

