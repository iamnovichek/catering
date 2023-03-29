from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomSignupForm
from .models import CustomUser


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
            user = form.save(commit=True)
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.birthdate = form.cleaned_data['birthdate']
            user.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})
