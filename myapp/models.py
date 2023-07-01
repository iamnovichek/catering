from django.db import models
from userauth.models import CustomUser


class Order(models.Model):
    user = models.ForeignKey(CustomUser, related_name="order", on_delete=models.CASCADE, unique=False)
    date = models.DateField()
    first_course = models.CharField(null=True, blank=True, unique=False, max_length=30)
    first_course_quantity = models.IntegerField(blank=True, null=True, unique=False, default=0)
    second_course = models.CharField(null=True, blank=True, unique=False, max_length=30)
    second_course_quantity = models.IntegerField(blank=True, null=True, unique=False, default=0)
    dessert = models.CharField(null=True, blank=True, unique=False, max_length=30)
    dessert_quantity = models.IntegerField(blank=True, null=True, unique=False, default=0)
    drink = models.CharField(null=True, blank=True, unique=False, max_length=30)
    drink_quantity = models.IntegerField(blank=True, null=True, unique=False, default=0)

    def __str__(self):
        return f"Date of order: {self.date}"


class Menu(models.Model):
    first_course = models.CharField(max_length=100, blank=False, unique=True, null=False)
    first_course_price = models.IntegerField()
    second_course = models.CharField(max_length=100, blank=False, unique=True, null=False)
    second_course_price = models.IntegerField()
    dessert = models.CharField(max_length=100, blank=False, unique=True, null=False)
    dessert_price = models.IntegerField()
    drink = models.CharField(max_length=100, blank=False, unique=True, null=False)
    drink_price = models.IntegerField()

    def __str__(self):
        return 'Dishes'


class History(models.Model):
    user = models.ForeignKey(CustomUser, related_name="history", on_delete=models.CASCADE, unique=False)
    date = models.DateField()
    first_course = models.CharField(null=True, blank=True, unique=False, max_length=30)
    first_course_quantity = models.IntegerField(blank=True, null=True, unique=False, default=0)
    second_course = models.CharField(null=True, blank=True, unique=False, max_length=30)
    second_course_quantity = models.IntegerField(blank=True, null=True, unique=False, default=0)
    dessert = models.CharField(null=True, blank=True, unique=False, max_length=30)
    dessert_quantity = models.IntegerField(blank=True, null=True, unique=False, default=0)
    drink = models.CharField(null=True, blank=True, unique=False, max_length=30)
    drink_quantity = models.IntegerField(blank=True, null=True, unique=False, default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Date of order: {self.date}(History)"
