from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser


# Create your models here.

class User(AbstractUser):
    """ Database model for users in the system """
    email = models.EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        """ Return string representation of our user """
        return self.email
