from django import forms
from django.contrib.auth.forms import UserCreationForm as SignupForm
from .models import CustomUser, Profile


class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    birthdate = forms.DateField(required=False, help_text='Optional')
    photo = forms.ImageField(required=False, help_text='Optional')

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
        birthdate = self.cleaned_data['birthdate']
        photo = self.cleaned_data['photo']

        if commit:
            user = CustomUser.objects.create_user(
                email=email,
                password=password
            )

            Profile.objects.create(
                user=user,
                username=username,
                first_name=first_name,
                last_name=last_name,
                birthdate=birthdate,
                photo=photo
            )

        return user
