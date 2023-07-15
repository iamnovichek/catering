import pytest

from myapp.templatetags.custom_filters import enumerate_items, get_index, \
    distribute_dishes

pytestmark = pytest.mark.django_db


def test_enumerate_items():
    data = [f"{i}" for i in range(10)]

    assert list(enumerate_items(data)) == list(enumerate(data))


def test_get_index_valid_data():
    data = [f"{i}" for i in range(10)]

    assert data[4] == get_index(data, 4)


def test_distribute_dishes_divisible_by_3():
    data = ['Dish 1', 'Dish 2', 'Dish 3',
            'Dish 4', 'Dish 5', 'Dish 6']
    expected_result = [['Dish 1', 'Dish 2', 'Dish 3'],
                       ['Dish 4', 'Dish 5', 'Dish 6']]

    assert distribute_dishes(data) == expected_result


def test_distribute_dishes_not_divisible_by_3():
    data = ['Dish 1', 'Dish 2', 'Dish 3',
            'Dish 4', 'Dish 5', 'Dish 6', 'Dish 7']

    expected_result = [['Dish 1', 'Dish 2', 'Dish 3'],
                       ['Dish 4', 'Dish 5', 'Dish 6'], ['Dish 7']]

    assert distribute_dishes(data) == expected_result


def test_distribute_dishes_empty_list():

    assert distribute_dishes([]) == []


def test_get_index_invalid_data():
    data = [f"{i}" for i in range(10)]

    assert get_index(data, 15) == ""
