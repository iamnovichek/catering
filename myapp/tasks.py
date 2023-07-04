import os

from celery import shared_task
from .models import Menu


@shared_task()
def upload_menu_task(rows):
    for row in rows:
        db_row = Menu.objects.create(
            first_course=row['first_course'],
            first_course_price=row['first_course_price'],
            second_course=row['second_course'],
            second_course_price=row['second_course_price'],
            dessert=row['dessert'],
            dessert_price=row['dessert_price'],
            drink=row['drink'],
            drink_price=row['drink_price']
        )

        db_row.save()

    return "Menu uploaded"
