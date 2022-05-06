from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, name, username, email, password=None):
        if not email:
            raise ValidationError('User must have email address')
        if not username:
            raise ValidationError('User must have username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
        )
        user.set_password(password)
        user.is_active = True
        user.is_student = True
        user.save()
        return user

    def create_superuser(self, name, username, password=None):
        user = self.model(
            username=username,
            name=name,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_admin = True
        user.is_warden = True
        user.is_active = True
        user.is_superadmin = True
        user.save()
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=30)
    phone_number = models.CharField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_warden = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
