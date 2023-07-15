import pytest
import os
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from catering.tests.factories import UserProfileFactory
from userauth.forms import CustomSignupForm

pytestmark = pytest.mark.django_db


class TestCustomSignupForm:

    def test_clean_method_valid_data(self):
        form = CustomSignupForm(data={
            "username": "test",
            "first_name": "Hello",
            "last_name": "World",
            "phone": "+380970082876",
            "email": "test@gmail.com",
            "password1": "testpassword",
            "password2": "testpassword"
        })

        assert form.is_valid()

    def test_clean_method_invalid_data(self):
        form = CustomSignupForm(data={
            "username": "",
            "first_name": "",
            "last_name": "",
            "phone": "+38097006",
            "email": "@gmail.com",
            "password1": "password",
            "password2": "password"
        })

        assert not form.is_valid()

    def test_clean_existing_username(self):
        prof = UserProfileFactory()

        form = CustomSignupForm(data={
            "username": prof.username,
            "first_name": "Hello",
            "last_name": "World",
            "phone": "+380970082876",
            "email": "test@gmail.com",
            "password1": "testpassword",
            "password2": "testpassword"
        })

        form.is_valid()

        with pytest.raises(ValidationError) as e:
            form.clean()

        assert str(e.value) == "['Current username is already taken!']"
        os.remove(f"{os.getcwd()}{prof.photo.url}")

    def test_clean_existing_phone_number(self):
        prof = UserProfileFactory()

        form = CustomSignupForm(data={
            "username": "testuser",
            "first_name": "Hello",
            "last_name": "World",
            "phone": prof.phone,
            "email": "test@gmail.com",
            "password1": "testpassword",
            "password2": "testpassword"
        })

        form.is_valid()
        form.cleaned_data.update({"phone": prof.phone})
        with pytest.raises(ValidationError) as e:
            form.clean()
        assert str(e.value) == "['Current phone number is already taken!']"
        os.remove(f"{os.getcwd()}{prof.photo.url}")

    def test_save_colected_data(self):
        form = CustomSignupForm(data={
            "username": "test",
            "first_name": "Hello",
            "last_name": "World",
            "phone": "+380970082876",
            "email": "test@gmail.com",
            "password1": "testpassword",
            "password2": "testpassword"
        })

        form.is_valid()

        user = form.save()

        assert user.email == form.cleaned_data['email']
        assert check_password(
            'testpassword',
            'pbkdf2_sha256$390000$HjV17O1NjtXDklhPVTHlV8$p4Bti'
            '1aJLUDgTAR6ECy9rw4ufKOctCJ6fYw0ORbVBdI='
        )
        assert user.userprofile.username == form.cleaned_data['username']
        assert user.userprofile.first_name == form.cleaned_data['first_name']
        assert user.userprofile.last_name == form.cleaned_data['last_name']
        assert user.userprofile.phone == form.cleaned_data['phone']
