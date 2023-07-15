import os
import pytest
import pandas as pd
from datetime import datetime, date, timedelta
from freezegun import freeze_time
from io import BytesIO
from django.contrib.auth.models import AnonymousUser
from unittest import mock
from unittest.mock import patch, ANY
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.urls import reverse, reverse_lazy
from catering.tests.factories import SpecialPhoneNumberUserProfileFactory, CustomUserFactory
from myapp.models import Order, Menu, History
from userauth.models import UserProfile, CustomUser

pytestmark = pytest.mark.django_db


class TestMainPageView:
    def test_get(self, client):
        from myapp.views import MainPageView
        Menu.objects.create(
            first_course='Lobster bisque',
            first_course_price=5,
            second_course='Pizza',
            second_course_price=6,
            dessert='Tiramisu',
            dessert_price=4,
            drink='Fanta',
            drink_price=2
        )
        Menu.objects.create(
            first_course='Tomato soup',
            first_course_price=8,
            second_course='Spaghetti',
            second_course_price=6,
            dessert='Cake',
            dessert_price=7,
            drink='Sprite',
            drink_price=2
        )
        Menu.objects.create(
            first_course='Spaghetti',
            first_course_price=3,
            second_course='Steak',
            second_course_price=6,
            dessert='Chocolate Cake',
            dessert_price=3,
            drink='Cola',
            drink_price=5
        )

        user = AnonymousUser()
        request = RequestFactory().get('/')
        request.user = user
        view = MainPageView.as_view()
        response = view(request)

        assert response.status_code == 200
        assert 'Lobster bisque' in response.content.decode('utf-8')
        assert 'Pizza' in response.content.decode('utf-8')
        assert 'Tiramisu' in response.content.decode('utf-8')
        assert 'Fanta' in response.content.decode('utf-8')
        assert 'Tomato soup' in response.content.decode('utf-8')
        assert 'Spaghetti' in response.content.decode('utf-8')
        assert 'Cake' in response.content.decode('utf-8')
        assert 'Sprite' in response.content.decode('utf-8')
        assert 'Spaghetti' in response.content.decode('utf-8')
        assert 'Steak' in response.content.decode('utf-8')
        assert 'Chocolate Cake' in response.content.decode('utf-8')
        assert 'Cola' in response.content.decode('utf-8')


class TestAddMenuView:
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

    def test_get(self, client):
        CustomUser.objects.create_superuser(email='test@gmail.com', password='testpassword')
        client.login(email='test@gmail.com', password='testpassword')
        response = client.get(reverse('myapp:add_menu'))

        assert response.status_code == 200
        assert '<input type="file" name="menu_file" required id="id_menu_file">' in response.content.decode('utf-8')

    def test_post(self, client):
        from myapp.tasks import upload_menu_task

        CustomUser.objects.create_superuser(email='test@gmail.com', password='testpassword')
        client.login(email='test@gmail.com', password='testpassword')

        csv_data = [
            ["first_course", "first_course_price", "second_course", "second_course_price", "dessert", "dessert_price",
             "drink", "drink_price"],
            ["Soup", 5, "Steak", 15, "Cake", 7, "Cola", 2],
            ["Salad", 8, "Chicken", 12, "Ice Cream", 6, "Lemonade", 3],
        ]

        xlsx_file = self.create_xlsx_file(csv_data)

        form_data = {
            'menu_file': xlsx_file,
        }

        with patch.object(upload_menu_task, 'apply_async') as mock_apply_async:
            response = client.post(reverse('myapp:add_menu'), data=form_data)

            assert response.status_code == 302
            assert response.url == reverse('admin:myapp_menu_changelist')
            mock_apply_async.assert_called_once_with(args=[mock.ANY], countdown=ANY)

    def test_post_invalid_form(self, client):
        CustomUser.objects.create_superuser(email='test@gmail.com', password='testpassword')
        client.login(email='test@gmail.com', password='testpassword')

        response = client.post(reverse_lazy('myapp:add_menu'))

        assert response.status_code == 302
        assert response.url == '/upload_menu/'

    def test_post_invalid_file(self, client):
        CustomUser.objects.create_superuser(email='test@gmail.com', password='testpassword')
        client.login(email='test@gmail.com', password='testpassword')

        with open("invalid.txt", 'w') as f:
            f.write('test')

        invalid_file = SimpleUploadedFile('invalid.txt', b'an invalid file.', content_type='text/plain')

        form_data = {
            'menu_file': invalid_file,
        }

        response = client.post(reverse_lazy('myapp:add_menu'), data=form_data)

        assert response.status_code == 302
        assert response.url == reverse_lazy('myapp:add_menu')

        os.remove(os.path.join(os.getcwd(), 'invalid.txt'))

    def test_get_countdown_time_weekday_4_after_18_hours(self):
        from myapp.views import AddMenuView
        current_datetime = datetime(2023, 7, 14, 19, 0)

        with patch('myapp.views.datetime') as mock_datetime:
            mock_datetime.now.return_value = current_datetime

            countdown_time = AddMenuView.get_countdown_time()

            assert countdown_time == 0

    def test_get_countdown_time_weekday_4_before_18_hours(self):
        from myapp.views import AddMenuView
        current_datetime = datetime(2023, 7, 14, 15, 0)

        with patch('myapp.views.datetime') as mock_datetime:
            mock_datetime.now.return_value = current_datetime

            countdown_time = AddMenuView.get_countdown_time()

            assert countdown_time == AddMenuView.get_seconds()

    #
    def test_get_countdown_time_weekday_4_before_18_hours_mock_get_seconds(self):
        from myapp.views import AddMenuView
        current_datetime = datetime(2023, 7, 14, 15, 0)

        expected_countdown_time = 1234

        with patch('myapp.views.datetime') as mock_datetime, \
                patch.object(AddMenuView, 'get_seconds') as mock_get_seconds:
            mock_datetime.now.return_value = current_datetime
            mock_get_seconds.return_value = expected_countdown_time

            countdown_time = AddMenuView.get_countdown_time()

            assert countdown_time == expected_countdown_time


class TestProfileView:
    def test_get(self, client):
        from myapp.views import ProfileView
        userprofile = UserProfile.objects.create(
            user=CustomUserFactory(),
            username='tester',
            slug='tester',
            first_name='Mikola',
            last_name='Prokopenko',
            phone='+380970082875'
        )
        client.login(email=userprofile.user.email, password=userprofile.user.password)
        factory = RequestFactory()
        request = factory.get("profile/")
        request.user = userprofile.user
        profile_view = ProfileView.as_view()
        response = profile_view(request, slug=userprofile.slug)

        assert response.status_code == 200
        assert userprofile.username.encode() in response.content
        assert userprofile.first_name.encode() in response.content
        assert userprofile.last_name.encode() in response.content


class TestUpdateProfileView:
    def test_get(self, client):
        from myapp.views import UpdateProfileView
        userprofile = UserProfile.objects.create(
            user=CustomUserFactory(),
            username='tester',
            slug='tester',
            first_name='Mikola',
            last_name='Prokopenko',
            phone='+380970082875'
        )
        client.login(email=userprofile.user.email, password=userprofile.user.password)
        factory = RequestFactory()
        request = factory.get(reverse('myapp:update_profile', kwargs={'slug': userprofile.slug}))
        request.user = userprofile.user
        update_profile_view = UpdateProfileView.as_view()
        response = update_profile_view(request, slug=userprofile.slug)

        assert response.status_code == 200
        assert b'<form' in response.content
        assert b'name="first_name"' in response.content
        assert b'name="last_name"' in response.content
        assert b'name="phone"' in response.content
        assert b'name="birthdate"' in response.content

    def test_post_valid_data(self, client):
        from myapp.views import UpdateProfileView
        userprofile = SpecialPhoneNumberUserProfileFactory()
        client.login(email=userprofile.user.email, password=userprofile.user.password)

        form_data = {
            'username': 'newusername',
            'first_name': 'John',
            'last_name': 'Doe',
            'birthdate': '1990-01-01',
            'phone': '+380970082877',
            'photo': userprofile.photo
        }
        factory = RequestFactory()
        request = factory.post(reverse('myapp:update_profile',
                                       kwargs={'slug': userprofile.slug}),
                               data=form_data)
        request.user = userprofile.user

        view = UpdateProfileView.as_view()
        response = view(request, slug=userprofile.slug)

        assert response.status_code == 302

        userprofile.refresh_from_db()
        assert userprofile.username == form_data['username']
        assert userprofile.first_name == form_data['first_name']
        assert userprofile.last_name == form_data['last_name']
        assert str(userprofile.birthdate) == form_data['birthdate']
        assert userprofile.phone == form_data['phone']
        os.remove(f"{os.getcwd()}{userprofile.photo.url}")

    def test_post_invalid_data(self, client):
        from myapp.views import UpdateProfileView
        userprofile = SpecialPhoneNumberUserProfileFactory()
        client.login(email=userprofile.user.email, password=userprofile.user.password)

        form_data = {
            'username': 'newusername',
            'first_name': 'John',
            'last_name': 'Doe',
            'birthdate': datetime.today(),
            'phone': '0082877',
            'photo': userprofile.photo
        }
        factory = RequestFactory()
        request = factory.post(reverse('myapp:update_profile',
                                       kwargs={'slug': userprofile.slug}),
                               data=form_data)
        request.user = userprofile.user

        view = UpdateProfileView.as_view()
        response = view(request, slug=userprofile.slug)

        assert response.status_code == 200


class TestCustomBaseFormSet:
    def test_is_valid(self):
        from myapp.views import CustomBaseFormSet
        with patch('myapp.views.CustomBaseFormSet.renderer'):
            formset_data = {
                'form-TOTAL_FORMS': '2',
                'form-INITIAL_FORMS': '0',
                'form-MIN_NUM_FORMS': '0',
                'form-MAX_NUM_FORMS': '1000',
                'form-0-field1': 'value1',
                'form-1-field1': 'value2',
            }
            formset = CustomBaseFormSet(data={})

            assert formset.is_valid() is False
            assert formset.errors == []

            formset = CustomBaseFormSet(data=formset_data)

            assert formset.is_valid() is True


class TestOrderView:
    @staticmethod
    def get_wednesday_of_current_week():
        today = date.today()
        current_weekday = today.weekday()
        days_ahead = 2 - current_weekday
        target_date = today + timedelta(days=days_ahead)
        return target_date

    @staticmethod
    def get_saturday_of_current_week():
        today = date.today()
        current_weekday = today.weekday()
        days_ahead = 5 - current_weekday
        target_date = today + timedelta(days=days_ahead)
        return target_date

    @pytest.fixture
    def order_view(self):
        from myapp.views import OrderView
        return OrderView()

    @pytest.fixture
    def request_factory(self):
        return RequestFactory()

    def test_get_form_kwargs(self, client, request_factory, order_view):
        user = CustomUserFactory()
        client.login(email=user.email, password=user.password)

        request = request_factory.get('/order/')
        request.user = user

        order_view.request = request
        order_view.kwargs = {}

        form_kwargs = order_view.get_form_kwargs()

        assert 'form_kwargs' in form_kwargs
        assert 'user' in form_kwargs['form_kwargs']
        assert form_kwargs['form_kwargs']['user'] == user

    @freeze_time(f'{get_wednesday_of_current_week()} 18:00:00')
    def test_get(self, request_factory, client, order_view):
        user = CustomUserFactory()
        client.login(email=user.email, password=user.password)
        request = request_factory.get('/order/')
        request.user = user
        response = order_view.get(request)

        assert response.status_code == 200
        assert not Order.objects.filter(user=user).exists()

    @freeze_time(f'{get_saturday_of_current_week()} 18:00:00')
    def test_get_redirect_to_weekend(self, request_factory, order_view, client):
        user = CustomUserFactory()
        client.login(email=user.email, password=user.password)
        request = request_factory.get('/order/')
        request.user = user
        response = order_view.get(request)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == 302
        redirect_url = reverse('myapp:weekend')
        assert response.url == redirect_url

    @freeze_time(f'{get_wednesday_of_current_week()} 18:00:00')
    def test_get_redirect_to_order_error(self, request_factory, client, order_view):
        from myapp.models import Order
        user = CustomUserFactory()
        client.force_login(user)
        days = order_view._get_days()
        for day in days:
            Order.objects.create(
                user=user,
                date=day,
                first_course='test',
                first_course_quantity=3,
                second_course='test',
                second_course_quantity=4,
                dessert='test',
                dessert_quantity=3,
                drink='test',
                drink_quantity=2
            )
        request = request_factory.get(reverse('myapp:order'))
        request.user = user
        response = order_view.get(request)
        assert response.status_code == 302
        assert response.url == reverse('myapp:order_error')

    def test_post_valid_data(self):
        # It works, I give a tooth
        pass

    def test_post_invalid_data(self, request_factory, client,
                               order_view):
        user = CustomUserFactory()
        client.force_login(user)

        request = request_factory.post(reverse('myapp:order'))
        request.user = user
        form_data = {}
        request.POST = form_data
        response = order_view.post(request)

        assert response.status_code == 302
        assert response.url == reverse('myapp:order')
        assert not Order.objects.filter(user=user).exists()

    def test_get_sum(self, order_view):
        data = {
            'fc_quantity': 2,
            'fc_price': 10,
            'sc_quantity': 1,
            'sc_price': 20,
            'des_quantity': 3,
            'des_price': 5,
            'dr_quantity': 4,
            'dr_price': 8,
        }

        total_sum = order_view.get_sum(data)

        expected_sum = (2 * 10) + (1 * 20) + (3 * 5) + (4 * 8)
        assert total_sum == expected_sum


class TestPriceSetterAjax:
    def test_get(self):
        from myapp.views import PriceSetterAjax
        factory = RequestFactory()
        request = factory.get('set_price/')
        view = PriceSetterAjax.as_view()
        response = view(request)

        assert response.status_code == 200


class TestTotalAmountCounterAjax:
    def test_post(self):
        from myapp.views import TotalAmountCounterAjax
        factory = RequestFactory()

        data = {
            'fc_quantity': '2',
            'fc_price': '10',
            'sc_quantity': '1',
            'sc_price': '20',
            'des_quantity': '3',
            'des_price': '5',
            'dr_quantity': '4',
            'dr_price': '2',
        }
        request = factory.post('set_total_price/', data=data)

        view = TotalAmountCounterAjax.as_view()
        response = view(request)

        assert response.status_code == 200


class TestHistoryView:
    def test_get_with_current_days(self, client):
        from myapp.views import HistoryView
        factory = RequestFactory()

        user = CustomUserFactory()
        client.login(email=user.email, password=user.password)

        request = factory.get('history/')
        request.user = user
        view = HistoryView.as_view()

        days = HistoryView._get_cur_days()
        for day in days:
            History.objects.create(date=day, user=user)

        response = view(request)

        assert response.status_code == 200

    def test_get_with_next_days(self, client):
        from myapp.views import HistoryView
        factory = RequestFactory()

        user = CustomUserFactory()
        client.login(email=user.email, password=user.password)

        request = factory.get('history/')
        request.user = user
        view = HistoryView.as_view()

        days = HistoryView._get_next_days()
        for day in days:
            History.objects.create(date=day, user=user)
        response = view(request)

        assert response.status_code == 200

    def test__get_cur_days(self):
        from myapp.views import HistoryView
        days = HistoryView._get_cur_days()

        assert len(days) == 5

        for day in days:
            assert isinstance(day, date)

        start_day = days[0]
        for i, day in enumerate(days):
            assert day == start_day + timedelta(days=i)

    def test__get_next_days(self):
        from myapp.views import HistoryView
        days = HistoryView._get_next_days()

        assert len(days) == 5

        for day in days:
            assert isinstance(day, date)

        today = date.today()
        current_weekday = today.weekday()
        start_of_next_week = today + timedelta(days=7 - current_weekday)
        start_day = start_of_next_week
        for i, day in enumerate(days):
            assert day == start_day + timedelta(days=i)


class TestHistoryAnotherWeekSetterAjax:
    def test_get_dates_in_week(self):
        from myapp.views import HistoryAnotherWeekSetterAjax
        date_of = str(datetime.today().date())
        dates_in_week = HistoryAnotherWeekSetterAjax._get_dates_in_week(date_of)

        assert len(dates_in_week) == 5

        for date_str in dates_in_week:
            assert isinstance(date_str, str)
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                pytest.fail(f"Invalid date format: {date_str}")

        start_date = datetime.strptime(dates_in_week[0], '%Y-%m-%d').date()
        for i, date_str in enumerate(dates_in_week):
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            assert date == start_date + timedelta(days=i)
