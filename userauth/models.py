from django.core.validators import validate_email
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from PIL import Image
from django.urls import reverse
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self,
                    email=None,
                    password=None):
        normalized_email = self.normalize_email(email)
        user = self.model(
            email=normalized_email,
            password=password,
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         email=None,
                         password=None):
        normalized_email = self.normalize_email(email)
        user = self.model(
            email=normalized_email,
            password=password,
        )

        user.is_admin = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, validators=[validate_email])
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        app_label = 'userauth'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.is_admin


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='userprofile', on_delete=models.CASCADE)
    username = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True)
    first_name = models.CharField(max_length=30, unique=False)
    last_name = models.CharField(max_length=30, unique=False)
    birthdate = models.DateField(unique=False, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    phone = PhoneNumberField(max_length=30, unique=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("myapp:update_profile", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)
        if self.photo:
            try:
                img = Image.open(self.photo.path)
            except FileNotFoundError:
                return
            output_size = (200, 200)
            img = img.resize(output_size)
            img.save(self.photo.path)

