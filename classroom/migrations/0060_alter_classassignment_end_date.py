# Generated by Django 5.0.6 on 2024-06-14 09:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0059_alter_classassignment_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classassignment',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 14, 9, 57, 21, 794596, tzinfo=datetime.timezone.utc)),
        ),
    ]