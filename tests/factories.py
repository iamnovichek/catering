import factory
from django.contrib.auth.hashers import make_password
from faker.providers import phone_number
from userauth.models import CustomUser, CustomUserManager, UserProfile
from myapp.models import Menu, History, Order

phone_nubmers = [
    '+32498311799',
    '+380970082875',
    '+380970082876',
    '+380671621626',
    '+380971688835'
]

class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Faker('email')
    password = make_password('password')
    is_active = True
    is_admin = False


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(CustomUserFactory)
    date = factory.Faker('date')
    first_course = factory.Faker('word')
    first_course_quantity = factory.Faker('random_int', min=0, max=10)
    second_course = factory.Faker('word')
    second_course_quantity = factory.Faker('random_int', min=0, max=10)
    dessert = factory.Faker('word')
    dessert_quantity = factory.Faker('random_int', min=0, max=10)
    drink = factory.Faker('word')
    drink_quantity = factory.Faker('random_int', min=0, max=10)


class MenuFactory(factory.django.DjangoModelFactory):
    first_course = factory.Faker('word')
    first_course_price = factory.Faker('pyint')
    second_course = factory.Faker('word')
    second_course_price = factory.Faker('pyint')
    dessert = factory.Faker('word')
    dessert_price = factory.Faker('pyint')
    drink = factory.Faker('word')
    drink_price = factory.Faker('pyint')

    class Meta:
        model = Menu


class HistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = History

    user = factory.SubFactory(CustomUserFactory)
    date = factory.Faker('date')
    first_course = factory.Faker('word')
    first_course_quantity = factory.Faker('random_int', min=0, max=10)
    second_course = factory.Faker('word')
    second_course_quantity = factory.Faker('random_int', min=0, max=10)
    dessert = factory.Faker('word')
    dessert_quantity = factory.Faker('random_int', min=0, max=10)
    drink = factory.Faker('word')
    drink_quantity = factory.Faker('random_int', min=0, max=10)


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(CustomUserFactory)
    username = factory.Faker('word')
    slug = factory.Faker('slug')
    first_name = factory.Faker('word')
    last_name = factory.Faker('word')
    birthdate = factory.Faker('date')
    photo = factory.django.ImageField()
    phone = factory.Faker('phone_number')


class SpecialPhoneNumberUserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(CustomUserFactory)
    username = factory.Faker('word')
    slug = factory.Faker('slug')
    first_name = factory.Faker('word')
    last_name = factory.Faker('word')
    birthdate = factory.Faker('date')
    photo = factory.django.ImageField(filename='default.png')
    phone = factory.LazyFunction(lambda: phone_nubmers.pop())

