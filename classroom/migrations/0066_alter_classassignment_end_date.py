# Generated by Django 5.0.6 on 2024-06-14 10:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0065_alter_classassignment_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classassignment',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 14, 10, 34, 14, 2556, tzinfo=datetime.timezone.utc)),
        ),
    ]
