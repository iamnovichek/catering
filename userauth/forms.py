from django import forms
from django.contrib.auth.forms import UserCreationForm as SignupForm
from .models import CustomUser


class CustomSignupForm(SignupForm):

    class Meta:
        model = CustomUser
        fields = ['username',  'email',
                  'password1', 'password2'
                  ]

    def save(self, commit=True):
        user = super(CustomSignupForm, self).save(commit=False)
        if commit:
            user.save()

        return user

