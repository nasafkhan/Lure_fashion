from django.db import models
import uuid

# Create your models here.

class Brand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)
    slug       = models.SlugField(max_length=100, unique=True)
    description= models.TextField(max_length=500, blank=True)
    brand_logo = models.ImageField(upload_to='photos/brands')

    def __str__(self):
        return self.brand_name
