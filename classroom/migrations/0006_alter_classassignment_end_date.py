# Generated by Django 5.0.6 on 2024-06-10 09:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0005_studentmarks_semester_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classassignment',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 10, 9, 21, 58, 959842, tzinfo=datetime.timezone.utc)),
        ),
    ]
