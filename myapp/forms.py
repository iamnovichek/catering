from django import forms

class UserLogin(forms.Form):

    email_input = forms.EmailInput()
    password_input = forms.PasswordInput()
