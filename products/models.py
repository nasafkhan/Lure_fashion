import uuid
from django.db import models
from category.models import Category
from brands.models import Brand
from django.utils.text import slugify

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


def __str__(self):
     return self.product_name