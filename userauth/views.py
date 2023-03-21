from django.contrib.auth.views import LoginView
from django.views.generic import CreateView as SignupView
from django.urls import reverse_lazy
from .forms import CustomSignupForm


class CustomLoginView(LoginView):
    template_name = 'userauth/login.html'


class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    success_url = reverse_lazy('success')
    template_name = 'userauth/signup.html'

