import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput
from userauth.models import UserProfile
from .models import Order, Menu, History


class CustomImageWidget(ClearableFileInput):
    initial_text = ""
    input_text = ""
    clear_checkbox_label = ""
    template_name = "myapp/custom_image_field.html"


class ProfileUpdateForm(forms.ModelForm):
    photo = forms.ImageField(widget=CustomImageWidget)

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.userprofile = UserProfile.objects.get(user=self.instance.user)
        self.fields['username'].initial = self.userprofile.username
        self.fields['first_name'].initial = self.userprofile.first_name
        self.fields['last_name'].initial = self.userprofile.last_name
        self.fields['birthdate'].initial = self.userprofile.birthdate
        self.fields['phone'].initial = self.userprofile.phone

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

        if not self._is_adult(cleaned_birthday) or self._is_too_old(cleaned_birthday):
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

    @staticmethod
    def _is_adult(birthdate):
        today_ = datetime.datetime.today()
        age = today_.year - birthdate.year - ((today_.month, today_.day) < (birthdate.month, birthdate.day))
        return age >= 18

    @staticmethod
    def _is_too_old(birthday):
        today_ = datetime.datetime.today()
        age = today_.year - birthday.year - ((today_.month, today_.day) < (birthday.month, birthday.day))
        return age >= 80


class DisabledOptionWidget(forms.Select):
    def render(self, name, value, attrs=None, renderer=None):
        html_code = super(DisabledOptionWidget, self).render(name, value, attrs, renderer)
        html_code = html_code.replace(f'<option value=""', f'<option value="" disabled')
        return html_code


class OrderForm(forms.ModelForm):
    first_course = forms.ChoiceField(choices=[("", 'Select a dish')] + [(f"{item}", item) for item in list(
        Menu.objects.values_list("first_course", flat=True))], widget=DisabledOptionWidget, required=False)
    first_course_quantity = forms.IntegerField(min_value=0, required=False)
    second_course = forms.ChoiceField(choices=[("", 'Select a dish')] + [(f"{item}", item) for item in list(
        Menu.objects.values_list("second_course", flat=True))], widget=DisabledOptionWidget, required=False)
    second_course_quantity = forms.IntegerField(min_value=0, required=False)
    dessert = forms.ChoiceField(choices=[("", 'Select a dish')] + [(f"{item}", item) for item in list(
        Menu.objects.values_list("dessert", flat=True))], widget=DisabledOptionWidget, required=False)
    dessert_quantity = forms.IntegerField(min_value=0, required=False)
    drink = forms.ChoiceField(choices=[("", 'Select a dish')] + [(f"{item}", item) for item in list(
       Menu.objects.values_list("drink", flat=True))], widget=DisabledOptionWidget, required=False)
    drink_quantity = forms.IntegerField(min_value=0, required=False)
    date = forms.DateField(required=False)
    user = forms.Field(required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Order
        fields = "__all__"

    def save(self, commit=True):
        if commit:
            order = super(OrderForm, self).save(commit=False)
            order.user = self.user

            history = History.objects.create(
                date=order.date,
                user=order.user,
                first_course=order.first_course,
                first_course_quantity=order.first_course_quantity,
                second_course=order.second_course,
                second_course_quantity=order.second_course_quantity,
                dessert=order.dessert,
                dessert_quantity=order.dessert_quantity,
                drink=order.drink,
                drink_quantity=order.drink_quantity
            )
            history.save()
            order.save()

            return order


class AddMenuForm(forms.ModelForm):
    menu_file = forms.FileField()

    class Meta:
        model = Menu
        fields = []

    def save(self, commit=True):

        if commit:

            if not self.cleaned_data['menu_file']:
                return None

            if Menu.objects.all():
                Menu.objects.all().delete()

            import pandas as pd

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
