from django import forms
from django.contrib.auth.forms import UserCreationForm as SignupForm
from .models import CustomUser


class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=255, required=True)
    birthdate = forms.DateField(required=False, help_text='''Optional (Sets current date by default)''')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name',
                  'last_name', 'email',
                  'birthdate', 'password1',
                  'password2']
