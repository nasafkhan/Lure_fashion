from django.shortcuts import redirect, render
from django.contrib import messages
from brands.models import Brand
from brands.forms import BrandForm, EditBrand
from category.models import Category
from category.forms import CategoryForm, EditCategory
from products.models import Product, Variation
from products.forms import EditProduct, EditVariant, ProductForm, VariantForm
from accounts.models import Account
from orders.models import OrderProduct, STATUS
from offer.forms import CategoryOfferForm, ProductOfferForm, BrandOfferForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse


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
def all_variants(request):
    variants = Variation.objects.all()

    context = {
        'variants' : variants 
    }

    return render(request, 'adminpanel/variants/all_variants.html', context)


@staff_member_required(login_url='access_denied')
def add_variant(request):
    form = VariantForm()

    if request.method == 'POST':
        variant_form = VariantForm(request.POST, request.FILES)

        if variant_form.is_valid():
            variant_form.save()
            messages.success(request, 'Variant added successfully')
        else:
            messages.error(request, 'Form submission failed')
        
        return redirect('add_variant')

    context = {
        'form' : form
    }
    return render(request, 'adminpanel/variants/add_variant.html', context)


@staff_member_required(login_url='access_denied')
def edit_variant(request, variant_id):
    edit_varian=Variation.object.get(id=variant_id)
    form = EditVariant(instance=edit_varian)
    if request.method == 'POST':
        form=EditVariant(request.POST, instance=edit_varian)
        if form.is_valid():
            try:
                form.save()
            except:
                context = {'form': form}
                return render(request,'adminpanel/variants/edit_variant.html', context)
            return redirect('all_variants')
    
    context = {
        'form': form
    }
    return render(request,'adminpanel/variants/edit_variant.html', context)

@staff_member_required(login_url='access_denied')
def delete_variant(request, varian_id):
    Variation.objects.get(id=varian_id).delete()
    return redirect('all_variants')

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


@staff_member_required(login_url='access_denied')
def add_product_offer(request):
    form = ProductOfferForm()
    if request.method == 'POST':
        form = ProductOfferForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Offer added for product successfully')
            return redirect('add_product_offer')
    
    context = {
        'form' : form
    }

    return render(request, 'adminpanel/offers/add_product_offer.html', context)


@staff_member_required(login_url='access_denied')
def add_brand_offer(request):
    form = BrandOfferForm()
    if request.method == 'POST':
        form = BrandOfferForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Offer added for brand successfully')
            return redirect('add_brand_offer')
    context = {
        'form' : form
    }

    return render(request, 'adminpanel/offers/add_brand_offer.html', context)


@staff_member_required(login_url='access_denied')
def add_category_offer(request):
    form = CategoryOfferForm()
    if request.method == 'POST':
        form = CategoryOfferForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Offer added for category successfully')
            return redirect('add_category_offer')
    context = {
        'form' : form
    }
    
    return render(request, 'adminpanel/offers/add_category_offer.html', context)
    

@staff_member_required(login_url='access_denied')
def active_orders(request):
    list_exclude = ['Delivered', 'Canceled']
    active_orders = OrderProduct.objects.all().exclude(status__in=list_exclude)
    status = STATUS
    context = {
        'active_orders': active_orders,
        'status': status,
    }
    return render(request, 'adminpanel/orders/active_orders.html', context)



@staff_member_required(login_url='access_denied')
def update_order_status(request, pk):
    if request.method == 'POST':
        status = request.POST.get('status')
        order_product = OrderProduct.objects.get(pk=pk)

        if status == 'Canceled':
            variant = order_product.variant
            variant.stock += order_product.quantity
            variant.save()

        order_product.status = status
        order_product.save()
        return JsonResponse({'message': status})