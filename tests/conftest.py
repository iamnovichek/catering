from pytest_factoryboy import register
from catering.tests.factories import (OrderFactory, CustomUserFactory, MenuFactory,
                                      HistoryFactory, UserProfileFactory, SpecialPhoneNumberUserProfileFactory)

register(CustomUserFactory)
register(OrderFactory)
register(MenuFactory)
register(HistoryFactory)
register(UserProfileFactory)
register(SpecialPhoneNumberUserProfileFactory)
