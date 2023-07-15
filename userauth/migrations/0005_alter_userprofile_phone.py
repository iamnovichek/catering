# Generated by Django 4.1.7 on 2023-07-10 13:38

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0004_remove_customuser_date_joined_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default='default.png', max_length=30, region=None, unique=True),
        ),
    ]
