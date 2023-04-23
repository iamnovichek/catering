import os

from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from PIL import Image
from django.conf import settings
from django.utils.text import slugify


class CustomUserManager(UserManager):
    def create_user(self,
                    email=None,
                    password=None,
                    **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         email=None,
                         password=None,
                         **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_admin = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='userprofile', on_delete=models.CASCADE)
    username = models.CharField(max_length=30, unique=True, blank=False)
    slug = models.SlugField(unique=True)
    first_name = models.CharField(max_length=30, unique=False, blank=False)
    last_name = models.CharField(max_length=30, unique=False, blank=False)
    birthdate = models.DateField(unique=False, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_pics')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            output_size = (200, 200)
            img = img.resize(output_size)
            img.save(self.photo.path)

