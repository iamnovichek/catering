import os
from io import BytesIO
import pytest
import pandas as pd
import datetime
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from catering.tests.factories import UserProfileFactory, SpecialPhoneNumberUserProfileFactory, \
    CustomUserFactory
from userauth.models import UserProfile, CustomUserManager, CustomUser
from myapp.models import History, Menu, Order

pytestmark = pytest.mark.django_db


class TestProfileUpdateForm:

    def test__init__(self):
        user_profile = UserProfileFactory()
        os.remove(f"{os.getcwd()}{user_profile.photo.url}")

        form_data = {
            'username': 'newusername',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'birthdate': '1995-05-05',
            'phone': '+380970082875',
        }
        from myapp.forms import ProfileUpdateForm
        form = ProfileUpdateForm(data=form_data, instance=user_profile)

        assert form.is_valid()

        form.save(commit=True)

        updated_user_profile = UserProfile.objects.get(id=user_profile.id)

        assert updated_user_profile.username == 'newusername'
        assert updated_user_profile.first_name == 'Jane'
        assert updated_user_profile.last_name == 'Smith'
        assert str(updated_user_profile.birthdate) == '1995-05-05'
        assert updated_user_profile.phone == '+380970082875'

    def test_profile_update_form_valid_clean(self):
        userprofile = UserProfileFactory()

        form_data = {
            'username': 'newusername',
            'birthdate': '1990-01-01',
            'phone': '+380970082875',
            'first_name': userprofile.first_name,
            'last_name': userprofile.last_name
        }

        from myapp.forms import ProfileUpdateForm
        form = ProfileUpdateForm(data=form_data, instance=userprofile)

        assert form.is_valid()
        form.clean()

        assert form.cleaned_data['username'] == 'newusername'
        assert str(form.cleaned_data['birthdate']) == '1990-01-01'
        assert form.cleaned_data['phone'] == '+380970082875'
        os.remove(f"{os.getcwd()}{userprofile.photo.url}")

    def test_profile_update_form_invalid_clean(self):
        userprofile = UserProfileFactory()

        form_data = {
            'username': '',
            'birthdate': '1990-001',
            'phone': '097002875',
        }

        from myapp.forms import ProfileUpdateForm
        form = ProfileUpdateForm(data=form_data, instance=userprofile)

        assert not form.is_valid()
        os.remove(f"{os.getcwd()}{userprofile.photo.url}")

    def test_profile_update_form_invalid_unsername_clean(self):
        userprofile1 = UserProfileFactory()
        userprofile2 = UserProfileFactory()
        form_data = {
            'username': userprofile2.username,
            'birthdate': '1990-01-01',
            'phone': '+380970082875',
            'first_name': userprofile1.first_name,
            'last_name': userprofile1.last_name
        }

        from myapp.forms import ProfileUpdateForm
        form = ProfileUpdateForm(data=form_data, instance=userprofile1)

        assert form.is_valid() is False

        assert 'username' in form.errors
        assert form.errors['__all__'][0] == 'Current username is already taken!'
        os.remove(f"{os.getcwd()}{userprofile1.photo.url}")
        os.remove(f"{os.getcwd()}{userprofile2.photo.url}")

    def test_cleaned_birthday_valid_date(self):
        from myapp.forms import ProfileUpdateForm
        userprofile = UserProfileFactory()
        userprofile.photo = None
        form_data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'birthdate': '1990-01-01',
            'phone': '+380970082875',
            'photo': None
        }
        form = ProfileUpdateForm(data=form_data, instance=userprofile)
        form.is_valid()
        cleaned_birthday = form.cleaned_data.get('birthdate')

        assert cleaned_birthday == datetime.datetime.strptime('1990-01-01', "%Y-%m-%d").date()

    def test_cleaned_birthday_too_young(self):
        from myapp.forms import ProfileUpdateForm
        userprofile = UserProfileFactory()
        form_data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'birthdate': '2023-06-01',
            'phone': '+380970082875',
        }
        form = ProfileUpdateForm(data=form_data, instance=userprofile)

        form.is_valid()

        cleaned_birthday = form.cleaned_data.get('birthdate')

        assert not form._is_adult(cleaned_birthday)
        os.remove(f"{os.getcwd()}{userprofile.photo.url}")

    def test_cleaned_birthday_too_old(self):
        from myapp.forms import ProfileUpdateForm
        userprofile = UserProfileFactory()
        form_data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'birthdate': '1023-06-01',
            'phone': '+380970082875',
        }
        form = ProfileUpdateForm(data=form_data, instance=userprofile)

        form.is_valid()

        cleaned_birthday = form.cleaned_data.get('birthdate')

        assert form._is_too_old(cleaned_birthday)
        os.remove(f"{os.getcwd()}{userprofile.photo.url}")

    def test_cleaned_phone_exits(self):
        from myapp.forms import ProfileUpdateForm
        userprofile1 = SpecialPhoneNumberUserProfileFactory()
        userprofile2 = SpecialPhoneNumberUserProfileFactory()
        form_data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'birthdate': '1990-01-01',
            'phone': userprofile2.phone,
        }

        form = ProfileUpdateForm(data=form_data, instance=userprofile1)

        form.is_valid()

        assert form.errors['__all__'][0] == "Current phone number is already taken!"
        os.remove(f"{os.getcwd()}{userprofile1.photo.url}")
        os.remove(f"{os.getcwd()}{userprofile2.photo.url}")

    def test_profile_update_form_file_not_found(self):
        from myapp.forms import ProfileUpdateForm
        userprofile = UserProfileFactory()

        form_data = {
            'username': 'newusername',
            'birthdate': '1990-01-01',
            'phone': '+380970082875',
            'first_name': userprofile.first_name,
            'last_name': userprofile.last_name,
            'photo': 'test_img.png'
        }

        form = ProfileUpdateForm(data=form_data, instance=userprofile)

        assert form.is_valid()
        os.remove(f"{os.getcwd()}{userprofile.photo.url}")
        res = form.save()
        file_path = os.path.join(os.getcwd(),
                                 f'{userprofile.photo.url}')
        assert not os.path.exists(file_path)
        assert res


class TestDisabledOptionWidget:
    def test_rendder(self):
        from myapp.forms import DisabledOptionWidget
        choice_field = forms.ChoiceField(choices=[("", 'Select a dish')], widget=DisabledOptionWidget)
        rendered_html = choice_field.widget.render('my_field', '', attrs={'id': 'choice_field'})

        expected_html = ('<select name="my_field" id="choice_field">\n'
                         '  <option value="" disabled selected>Select a dish</option>\n'
                         '\n'
                         '</select>')

        assert expected_html == rendered_html


class TestOrderForm:
    def test__init__(self):
        from myapp.forms import OrderForm
        user = CustomUserFactory
        form = OrderForm(user=user)

        assert form.user == user

    def test_save_method(self):
        from myapp.forms import OrderForm
        menu = Menu.objects.create(
            first_course='Lobster bisque',
            first_course_price=5,
            second_course='Pizza',
            second_course_price=6,
            dessert='Tiramisu',
            dessert_price=4,
            drink='Fanta',
            drink_price=2
        )

        user = CustomUserFactory()
        form_data = {
            'user': user,
            'date': '2023-07-12',
            'first_course': str(menu.first_course),
            'first_course_quantity': 2,
            'second_course': str(menu.second_course),
            'second_course_quantity': 1,
            'dessert': str(menu.dessert),
            'dessert_quantity': 3,
            'drink': str(menu.drink),
            'drink_quantity': 2,
        }

        choices = {
            'first_course': [(str(item.first_course), item.first_course) for item in Menu.objects.all()],
            'second_course': [(str(item.second_course), item.second_course) for item in Menu.objects.all()],
            'dessert': [(str(item.dessert), item.dessert) for item in Menu.objects.all()],
            'drink': [(str(item.drink), item.drink) for item in Menu.objects.all()],
        }

        form = OrderForm(data=form_data, user=user)
        form.fields['first_course'].choices = choices['first_course']
        form.fields['second_course'].choices = choices['second_course']
        form.fields['dessert'].choices = choices['dessert']
        form.fields['drink'].choices = choices['drink']

        assert form.is_valid()

        order = form.save()
        assert order.user == user
        assert str(order.date) == '2023-07-12'
        assert order.first_course == menu.first_course
        assert order.first_course_quantity == 2
        assert order.second_course == menu.second_course
        assert order.second_course_quantity == 1
        assert order.dessert == menu.dessert
        assert order.dessert_quantity == 3
        assert order.drink == menu.drink
        assert order.drink_quantity == 2


class TestAddMenuForm:
    @staticmethod
    def create_xlsx_file(csv_data):
        df = pd.DataFrame(csv_data)

        excel_file = BytesIO()

        with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, header=False)

        excel_file.seek(0)

        file_data = excel_file.read()
        content = SimpleUploadedFile("menu.xlsx", file_data,
                                     content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        return content

    def test_add_menu_form_parse_file(self):
        from myapp.forms import AddMenuForm
        csv_data = [
            ["first_course", "first_course_price", "second_course", "second_course_price", "dessert", "dessert_price",
             "drink", "drink_price"],
            ["Soup", 5, "Steak", 15, "Cake", 7, "Cola", 2],
            ["Salad", 8, "Chicken", 12, "Ice Cream", 6, "Lemonade", 3],
        ]

        xlsx_file = self.create_xlsx_file(csv_data)

        form = AddMenuForm(files={'menu_file': xlsx_file})

        assert form.is_valid()

        parsed_data = form.parse_file()

        assert not Menu.objects.all()

        expected_data = [
            {"first_course": "Soup", "first_course_price": 5, "second_course": "Steak", "second_course_price": 15,
             "dessert": "Cake", "dessert_price": 7, "drink": "Cola", "drink_price": 2},
            {"first_course": "Salad", "first_course_price": 8, "second_course": "Chicken", "second_course_price": 12,
             "dessert": "Ice Cream", "dessert_price": 6, "drink": "Lemonade", "drink_price": 3}
        ]

        assert parsed_data == expected_data

    def test_parse_file_deletes_existing_menus(self):
        from myapp.forms import AddMenuForm
        menu = Menu.objects.create(
            first_course='Soup',
            first_course_price=5,
            second_course='Steak',
            second_course_price=15,
            dessert='Cake',
            dessert_price=7,
            drink='Cola',
            drink_price=2
        )

        csv_data = [
            ["first_course", "first_course_price", "second_course", "second_course_price", "dessert", "dessert_price",
             "drink", "drink_price"],
            ["Soup", 5, "Steak", 15, "Cake", 7, "Cola", 2],
            ["Salad", 8, "Chicken", 12, "Ice Cream", 6, "Lemonade", 3],
        ]

        xlsx_file = self.create_xlsx_file(csv_data)

        form = AddMenuForm()
        form.cleaned_data = {'menu_file': xlsx_file}

        form.parse_file()

        assert not Menu.objects.filter(pk=menu.pk).exists()
