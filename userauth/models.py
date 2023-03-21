from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from PIL import Image
from datetime import datetime

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    #email = models.EmailField(max_length=254)
    birthdate = models.DateField(default=datetime.today, )
    photo = models.ImageField(default='default.png',
                              upload_to="profile_pics",
                              )
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)