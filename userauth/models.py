from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from PIL import Image


class CustomUserManager(UserManager):
    def create_user(self,
                    username,
                    password=None,
                    **extra_fields):
        user = self.model(
            username=username,
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # тут якщо я не буду повторюватися,
    # я не зможу зайти бо писатиме що неправильний логін або пароль
    # хоча для звичайного користувавча все працює добре
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
    # а якщо тут я заберу поле пошти то видасть помилку,
    # що так як USERNAME_FIELD я виставив ел. пошту,
    # то воно має бути unique і я намагався у менеджері
    # зроюити щось типу user.email.unique = True,
    # але не вийшло
    email = models.EmailField(max_length=254, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        # change after to username
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

