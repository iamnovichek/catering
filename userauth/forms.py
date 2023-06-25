import django.core.exceptions
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm as SignupForm
from .models import CustomUser, UserProfile
from django.core.exceptions import ValidationError


class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = PhoneNumberField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email',
                  'password1',
                  'password2'
                  ]

    def clean(self):
        cleaned_data = super(CustomSignupForm, self).clean()
        username = cleaned_data.get('username')
        phone = cleaned_data.get('phone')

        if UserProfile.objects.filter(username=username).exists():
            raise ValidationError("Current username is already taken!")

        if UserProfile.objects.filter(phone=phone).exists():
            raise ValidationError("Current phone number is already taken!")

    def save(self, commit=True):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name'][0].capitalize() + self.cleaned_data['first_name'][1:]
        last_name = self.cleaned_data['last_name'][0].capitalize() + self.cleaned_data['last_name'][1:]
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
