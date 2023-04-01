from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomSignupForm


class CustomLoginView(LoginView):
    template_name = 'userauth/login.html'
    success_url = reverse_lazy('home')


class CustomSignupView(CreateView):
    form_class = CustomSignupForm
    success_url = reverse_lazy('success')
    template_name = 'userauth/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})
