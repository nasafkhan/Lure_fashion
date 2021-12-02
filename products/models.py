import uuid
from django.db import models
from category.models import Category
from brands.models import Brand
from django.utils.text import slugify
from django.urls import reverse
from accounts.models import Account

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField(null=True)
    image1 = models.ImageField(upload_to='photos/products', )
    image2 = models.ImageField(upload_to='photos/products', blank=True)
    image3 = models.ImageField(upload_to='photos/products', blank=True)
    image4 = models.ImageField(upload_to='photos/products', blank=True)
    stock = models.IntegerField()
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args = [self.category.slug, self.slug])

    def get_price(self):
        try:
            if self.productoffer.is_active:
                offer_price = round((self.price / 100) * self.productoffer.discount_offer)
                price = round(self.price - offer_price)
                return {'price': price, 'discount': self.productoffer.discount_offer}
            raise
        except:
            try:
                if self.category.categoryoffer.is_active:
                    offer_price = round((self.price / 100) * self.category.categoryoffer.discount_offer)
                    price = round(self.price - offer_price)
                    return {'price': price, 'discount': self.category.categoryoffer.discount_offer}
                raise
            except:
                try:
                    if self.brand.brandoffer.is_active:
                        offer_price = round((self.price / 100) * self.brand.brandoffer.discount_offer)
                        price =  round(self.price - offer_price)
                        return {'price': price, 'discount': self.brand.brandoffer.discount_offer}
                    raise
                except:
                    pass
                return {'price': self.price}

    def __str__(self):
        return self.product_name

variation_category_choice = (
    ('color', 'color' ),
    ('size', 'size')
)

class VariationManager(models.Manager):
    def color(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def size(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)


    objects = VariationManager()


    def __str__(self):
        return self.variation_value



class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject