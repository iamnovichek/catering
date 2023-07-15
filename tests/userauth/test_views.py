import pytest
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse
from userauth.views import CustomLoginView, CustomSignupView
from catering.tests.factories import CustomUserFactory

pytestmark = pytest.mark.django_db


class TestCustomLoginView:
    def test_form_invalid(self, rf):
        view = CustomLoginView()
        request = rf.post('/login/')
        setattr(view, 'request', request)
        request.session = 'dummy'
        storage = FallbackStorage(request)
        setattr(request, '_messages', storage)
        form = view.get_form()
        response = view.form_invalid(form)

        assert response.status_code == 200
        messages = list(get_messages(request))
        assert messages
        assert messages[0].message == "Invalid values! Try again or sign up!"


class TestCustomSignupView:
    def test_get(self):
        view = CustomSignupView()
        factory = RequestFactory()
        request = factory.get(reverse("signup"))
        request.user = CustomUserFactory()

        response = view.get(request)
        assert response.status_code == 200
        assert response['Content-Type'] == 'text/html; charset=utf-8'
        assert view.template_name == 'userauth/signup.html'
        assert 'form' in response.content.decode()

    def test_valid_form_post(self, client):
        url = reverse('signup')
        data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'phone': '+380970082876',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

        response = client.post(url, data=data)

        assert response.status_code == 302
        assert response.url == reverse('success')
        assert response.wsgi_request.user.is_authenticated
        assert isinstance(response, HttpResponseRedirect)

    def test_invalid_form_post(self, client):
        url = reverse('signup')
        data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'phone': '+380970082876',
            'password1': 'password',
            'password2': 'testpassword',
        }

        response = client.post(url, data=data)

        assert response.status_code == 200
        assert response.templates[0].name == 'userauth/signup.html'

