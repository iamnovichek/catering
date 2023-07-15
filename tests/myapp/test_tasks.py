import pytest
import os
from django.conf import settings
from catering.tests.factories import UserProfileFactory
from myapp.tasks import agrigate_orders, upload_menu_task, send_orders_task
from myapp.models import Order, Menu

pytestmark = pytest.mark.django_db


def test_agrigate_orders():
    user1 = UserProfileFactory()
    user2 = UserProfileFactory()

    Order.objects.create(
        user=user1.user,
        date='2023-07-01',
        first_course='Dish 1',
        first_course_quantity=2,
        second_course='Dish 2',
        second_course_quantity=1,
        dessert='Dish 3',
        dessert_quantity=3,
        drink='Drink 1',
        drink_quantity=4
    )
    Order.objects.create(
        user=user2.user,
        date='2023-07-02',
        first_course='Dish 4',
        first_course_quantity=1,
        second_course='Dish 5',
        second_course_quantity=2,
        dessert='Dish 6',
        dessert_quantity=2,
        drink='Drink 2',
        drink_quantity=3
    )

    names = [
        user1.first_name + " " + user1.last_name,
        user2.first_name + " " + user2.last_name,
    ]

    expected_result = {
        "date": ['2023-07-01', '2023-07-02'],
        "first_course": ['Dish 1', 'Dish 4'],
        "first_course_quantity": [2, 1],
        "second_course": ['Dish 2', 'Dish 5'],
        "second_course_quantity": [1, 2],
        "dessert": ['Dish 3', 'Dish 6'],
        "dessert_quantity": [3, 2],
        "drink": ['Drink 1', 'Drink 2'],
        "drink_quantity": [4, 3],
        "name": names
    }

    assert agrigate_orders() == expected_result
    os.remove(f"{os.getcwd()}{user1.photo.url}")
    os.remove(f"{os.getcwd()}{user2.photo.url}")


def test_upload_menu_task():

    rows = [
        {
            'first_course': 'Soup',
            'first_course_price': 5.99,
            'second_course': 'Steak',
            'second_course_price': 15.99,
            'dessert': 'Cake',
            'dessert_price': 4.99,
            'drink': 'Soda',
            'drink_price': 1.99,
        }
    ]

    result = upload_menu_task(rows)

    assert result == "Menu uploaded"

    menu = Menu.objects.first()
    assert menu.first_course == 'Soup'
    assert menu.first_course_price == 5
    assert menu.second_course == 'Steak'
    assert menu.second_course_price == 15
    assert menu.dessert == 'Cake'
    assert menu.dessert_price == 4
    assert menu.drink == 'Soda'
    assert menu.drink_price == 1


def test_send_orders_task(mailoutbox):
    send_orders_task()

    assert len(mailoutbox) == 1
    email = mailoutbox[0]
    assert email.subject == "Orders"
    assert email.body == "Orders for current week:"
    assert email.from_email == settings.EMAIL_HOST_USER
    assert email.to == [settings.RECEIVER]

    assert len(email.attachments) == 1
    attachment = email.attachments[0]
    assert attachment[0] == "orders.xlsx"
    assert os.path.exists("media/orders.xlsx")
    assert Order.objects.count() == 0
