from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
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
    profile_pic= models.ImageField(upload_to='photos/users/pofile_pics', default="")

#required
    date_joined    = models.DateTimeField(auto_now_add=True)
    last_login     = models.DateTimeField(auto_now_add=True)
    is_admin       = models.BooleanField(default=False)
    is_staff       = models.BooleanField(default=False)
    is_active      = models.BooleanField(default=True)
    is_superuser   = models.BooleanField(default=True)
    is_superadmin  = models.BooleanField(default=True)

 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
 
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True