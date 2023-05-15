import pandas as pd
import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput
from userauth.models import UserProfile
from .models import Order, Menu


def is_adult(birthdate):
    today_ = datetime.datetime.today()
    age = today_.year - birthdate.year - ((today_.month, today_.day) < (birthdate.month, birthdate.day))
    return age >= 18


def is_too_old(birthday):
    today_ = datetime.datetime.today()
    age = today_.year - birthday.year - ((today_.month, today_.day) < (birthday.month, birthday.day))
    return age >= 80


class CustomImageWidget(ClearableFileInput):
    initial_text = ""
    input_text = ""
    template_name = "myapp/custom_image_field.html"


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.userprofile = UserProfile.objects.get(user=self.instance.user)
        self.fields['username'].initial = self.userprofile.username
        self.fields['first_name'].initial = self.userprofile.first_name
        self.fields['last_name'].initial = self.userprofile.last_name
        self.fields['birthdate'].initial = self.userprofile.birthdate
        self.fields['phone'].initial = self.userprofile.phone

    photo = forms.ImageField(widget=CustomImageWidget)

    class Meta:
        model = UserProfile
        fields = [
            'username',
            'first_name',
            'last_name',
            'birthdate',
            'photo',
            'phone'
        ]

    def clean(self):
        cleaned_data = super(ProfileUpdateForm, self).clean()
        username = cleaned_data.get('username')
        birthday = cleaned_data.get('birthdate')
        phone = cleaned_data.get('phone')
        userprofile = UserProfile.objects.get(user=self.instance.user)
        cleaned_birthday = datetime.datetime.strptime(str(birthday), "%Y-%m-%d").date()

        if not is_adult(cleaned_birthday) or is_too_old(cleaned_birthday):
            raise ValidationError("Enter valid date!")

        if userprofile.username != username:
            if UserProfile.objects.filter(username=username).exists():
                raise ValidationError("Current username is already taken!")

        if userprofile.phone != phone:
            if UserProfile.objects.filter(phone=phone).exists():
                raise ValidationError("Current phone number is already taken!")

    def save(self, commit=True):
        form = super().save(commit=False)
        if commit:
            self.userprofile.username = self.cleaned_data['username']
            self.userprofile.first_name = self.cleaned_data['first_name']
            self.userprofile.last_name = self.cleaned_data['last_name']
            self.userprofile.birthdate = self.cleaned_data['birthdate']
            self.userprofile.phone = self.cleaned_data['phone']
            self.userprofile.photo = self.cleaned_data['photo']
            self.userprofile.save()
            form.save()

        return form


class OrderForm(forms.ModelForm):
    first_course = forms.ModelChoiceField(queryset=None)  # to complete
    first_course_quantity = forms.IntegerField(min_value=0)
    second_course = forms.ModelChoiceField(queryset=None)  # to complete
    second_course_quantity = forms.IntegerField(min_value=0)
    dessert = forms.ModelChoiceField(queryset=None)  # to complete
    dessert_quantity = forms.IntegerField(min_value=0)  # to complete
    drink = forms.ModelChoiceField(queryset=None)  # to complete
    drink_quantity = forms.IntegerField(min_value=0)

    class Meta:
        model = Order
        fields = [
            'date',
            'first_course',
            'first_course_quantity',
            'second_course',
            'second_course_quantity',
            'dessert',
            'dessert_quantity',
            'drink',
            'drink_quantity'
        ]

    def save(self, commit=True):
        if commit:
            order = Order.objects.create(
                date=self.cleaned_data['date'],
                first_course=self.cleaned_data['first_course'],
                first_course_quantity=self.cleaned_data['first_course_quantity'],
                second_course=self.cleaned_data['second_course'],
                second_course_quantity=self.cleaned_data['second_course_quantity'],
                dessert=self.cleaned_data['dessert'],
                dessert_quantity=self.cleaned_data['dessert_quantity'],
                drink=self.cleaned_data['drink'],
                drink_quantity=self.cleaned_data['drink_quantity']
            )

        return order


class AddMenuForm(forms.ModelForm):
    menu_file = forms.FileField()

    class Meta:
        model = Menu
        fields = []

    def save(self, commit=True):

        if commit:

            if Menu.objects.all():
                Menu.objects.all().delete()

            csv_file = self.cleaned_data['menu_file']
            excel_data = pd.read_excel(csv_file)
            db_frame = excel_data
            for row in db_frame.itertuples():
                line = Menu.objects.create(
                    first_course=row.first_course,
                    first_course_price=row.first_course_price,
                    second_course=row.second_course,
                    second_course_price=row.second_course_price,
                    dessert=row.dessert,
                    dessert_price=row.dessert_price,
                    drink=row.drink,
                    drink_price=row.drink_price
                )

                line.save()

        return db_frame


class MainPageForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = []

    first_courses = Menu.objects.values_list('first_course', flat=True)
    first_courses_number = Menu.objects.values_list('first_course', flat=True).count()
    second_courses = Menu.objects.values_list('second_course', flat=True)
    second_courses_number = Menu.objects.values_list('second_course', flat=True).count()
    desserts = Menu.objects.values_list('dessert', flat=True)
    desserts_number = Menu.objects.values_list('dessert', flat=True).count
    drinks = Menu.objects.values_list('drink', flat=True)
    drinks = Menu.objects.values_list('drink', flat=True).count()