# Generated by Django 5.0.6 on 2024-06-14 06:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0054_alter_classassignment_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classassignment',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 14, 6, 9, 14, 836448, tzinfo=datetime.timezone.utc)),
        ),
    ]