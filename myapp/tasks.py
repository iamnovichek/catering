import pandas as pd

from celery import shared_task
from userauth.models import CustomUser
from .models import Menu, Order
from django.core.mail import EmailMessage
from django.conf import settings

data_frame = pd.DataFrame

output_file = "media/orders.xlsx"


def agrigate_orders():
    ids = list(Order.objects.values_list("user_id", flat=True))
    names = []

    for i in ids:
        names.append(
            f"{CustomUser.objects.get(id=i).userprofile.first_name} " +
            f"{CustomUser.objects.get(id=i).userprofile.last_name}"
        )

    return {
        "date": [str(date) for date in Order.objects.values_list("date", flat=True)],
        "first_course": list(Order.objects.values_list("first_course", flat=True)),
        "first_course_quantity": list(Order.objects.values_list("first_course_quantity", flat=True)),
        "second_course": list(Order.objects.values_list("second_course", flat=True)),
        "second_course_quantity": list(Order.objects.values_list("second_course_quantity", flat=True)),
        "dessert": list(Order.objects.values_list("dessert", flat=True)),
        "dessert_quantity": list(Order.objects.values_list("dessert_quantity", flat=True)),
        "drink": list(Order.objects.values_list("drink", flat=True)),
        "drink_quantity": list(Order.objects.values_list("drink_quantity", flat=True)),
        "name": names
    }


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


@shared_task()
def send_orders_task():
    data_frame(agrigate_orders()).to_excel(output_file, index=False)

    email = EmailMessage(
        subject="Orders",
        body="Orders for current week:",
        from_email=settings.EMAIL_HOST_USER,
        to=[settings.RECEIVER]
    )

    email.attach_file(output_file)
    email.send(fail_silently=False)

    Order.objects.all().delete()

    return "Email sent"


