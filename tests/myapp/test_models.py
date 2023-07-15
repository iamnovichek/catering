import pytest

from catering.tests.factories import CustomUserFactory

pytestmark = pytest.mark.django_db


class TestOrderModel:
    def test_str_return(self, order_factory):
        user = CustomUserFactory()
        order = order_factory(user=user)

        assert order.__str__() == f"Date of order: {order.date}"


class TestMenuModel:

    def test_str_return(self, menu_factory):
        menu = menu_factory()

        assert menu.__str__() == "Dishes"


class TestHistoryModel:
    def test_str_return(self, history_factory):
        user = CustomUserFactory()
        history = history_factory(user=user)

        assert history.__str__() == f'''Date of order: {history.date}(History)'''
