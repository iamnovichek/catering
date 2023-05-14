from django.db import models


class Order(models.Model):
    date = models.DateField(unique=False, blank=False, null=False)
    first_course = models.CharField(null=False, blank=False, unique=False, max_length=30)
    first_course_quantity = models.IntegerField()
    second_course = models.CharField(null=False, blank=False, unique=False, max_length=30)
    second_course_quantity = models.IntegerField()
    dessert = models.CharField(null=False, blank=False, unique=False, max_length=30)
    dessert_quantity = models.IntegerField()
    drink = models.CharField(null=False, blank=False, unique=False, max_length=30)
    drink_quantity = models.IntegerField()

    def __str__(self):
        return f"Date of order: {self.date}"


class Menu(models.Model):
    first_course = models.CharField(max_length=30, blank=False, unique=True, null=False)
    first_course_price = models.IntegerField()
    second_course = models.CharField(max_length=30, blank=False, unique=True, null=False)
    second_course_price = models.IntegerField()
    dessert = models.CharField(max_length=30, blank=False, unique=True, null=False)
    dessert_price = models.IntegerField()
    drink = models.CharField(max_length=30, blank=False, unique=True, null=False)
    drink_price = models.IntegerField()

    def __str__(self):
        return 'Dishes'


class OrderHistory:
    pass
