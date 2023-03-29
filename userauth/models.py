from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from PIL import Image


class CustomUserManager(UserManager):
    def create_user(self,
                    username,
                    email=None,
                    password=None,
                    **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         username,
                         email=None,
                         password=None,
                         **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password
        )

        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthdate = models.DateField(blank=True,
                                 null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
