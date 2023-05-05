from django import forms
from django.contrib.auth.forms import UserCreationForm as SignupForm
from .models import CustomUser, UserProfile


class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=9, min_length=9, required=True)

    class Meta:
        model = CustomUser
        fields = ['email',
                  'password1',
                  'password2'
                  ]

    def save(self, commit=True):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        phone = self.cleaned_data['phone']

        if commit:
            user = CustomUser.objects.create_user(
                email=email,
                password=password
            )

            UserProfile.objects.create(
                user=user,
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )

        return user
