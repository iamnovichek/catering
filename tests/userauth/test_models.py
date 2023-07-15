import pytest
import os
from userauth.models import CustomUser, CustomUserManager
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestCustomUserManager:
    def test_normalize_email(self):
        email = 'Test@Example.com'
        normalized_email = CustomUserManager.normalize_email(email)

        assert normalized_email.lower() == 'test@example.com'

    def test_create_user(self):
        manager = CustomUserManager()
        email = 'test1@example.com'
        password = 'testpassword'
        manager.model = CustomUser
        user = manager.create_user(email=email, password=password)

        assert user.email == email
        assert user.is_active is True
        assert user.check_password(password) is True

    def test_create_superuser(self):
        manager = CustomUserManager()
        email = 'test2@example.com'
        password = 'testpassword'
        manager.model = CustomUser
        user = manager.create_superuser(email=email, password=password)

        assert user.email == email
        assert user.is_active is True
        assert user.is_admin is True
        assert user.check_password(password) is True


class TestCustomUser:
    def test_str_return(self, custom_user_factory):
        user = custom_user_factory()

        assert user.__str__() == user.email

    def test_is_staff_return(self, custom_user_factory):
        user = custom_user_factory()

        assert user.is_staff == user.is_admin


class TestUserProfile:
    def test_str_return(self, user_profile_factory):
        profile = user_profile_factory()

        assert profile.__str__() == profile.username
        os.remove(f"{os.getcwd()}{profile.photo.url}")

    def test_get_absolute_url_return(self, user_profile_factory):
        profile = user_profile_factory()

        expected_url = reverse('myapp:update_profile', kwargs={'slug': profile.slug})

        assert profile.get_absolute_url() == expected_url
        os.remove(f"{os.getcwd()}{profile.photo.url}")

