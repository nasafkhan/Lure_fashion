from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,username, email,phone, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            phone = phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, email,phone, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username= username,
            password=password,
            phone = phone,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username   = models.CharField(max_length=50, unique=True)
    email      = models.EmailField(max_length=50, unique=True)
    phone      = models.CharField(max_length=50)

#required
    date_joined    = models.DateTimeField(auto_now_add=True)
    last_login     = models.DateTimeField(auto_now_add=True)
    is_admin       = models.BooleanField(default=False)
    is_staff       = models.BooleanField(default=False)
    is_active      = models.BooleanField(default=True)
    is_superuser   = models.BooleanField(default=True)
    is_superadmin  = models.BooleanField(default=True)

 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
 
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.user.username

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100) 
    address_line1 = models.CharField(max_length=250)
    address_line2 = models.CharField(max_length=250, blank=True)
    landmark = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.IntegerField()
    type = models.CharField(max_length=50, verbose_name='Address Type', help_text='Example:- Home, Office, etc',null=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line1} {self.address_line2}'
