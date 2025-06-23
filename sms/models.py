from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extrafields):
        if not email:
            raise ValueError(_("the Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extrafields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))
        return self.create_user(email, password, **extra_fields)
    

class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    # last_login = models.DateField(auto_now=True, null=True)
    first_name = models.CharField(max_length=25, null=True)
    middle_name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=25, null=True)
    username = None           # removing user field
    email = models.EmailField(_("email address"), unique=True)  #setting it as username 
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    user_profile = models.ManyToManyField(Role,db_table='user_role', related_name='role')  

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # def full_name(self):
    #     return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email 
    

class Director(models.Model):
    id = models.AutoField(primary_key=True)
    phone_no = models.CharField(max_length=20)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='director')


