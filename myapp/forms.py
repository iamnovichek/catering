from django import forms
from userauth.models import UserProfile


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.userprofile = UserProfile.objects.get(user=self.instance.user)
        self.fields['username'].initial = self.userprofile.username
        self.fields['first_name'].initial = self.userprofile.first_name
        self.fields['last_name'].initial = self.userprofile.last_name
        self.fields['birthdate'].initial = self.userprofile.birthdate

    class Meta:
        model = UserProfile
        fields = [
            'username',
            'first_name',
            'last_name',
            'birthdate',
            'photo'
        ]

    def save(self, commit=True):
        form = super().save(commit=False)
        if commit:
            self.userprofile.username = self.cleaned_data['username']
            self.userprofile.first_name = self.cleaned_data['first_name']
            self.userprofile.last_name = self.cleaned_data['last_name']
            self.userprofile.birthdate = self.cleaned_data['birthdate']
            self.userprofile.photo = self.cleaned_data['photo']
            self.userprofile.save()
            form.save()

        return form
