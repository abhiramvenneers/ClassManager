# Generated by Django 5.0.6 on 2024-06-11 14:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0045_studentmarks_viva_marks_obtained_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentmarks',
            name='viva_marks_obtained',
        ),
        migrations.AlterField(
            model_name='classassignment',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 11, 14, 38, 17, 468480, tzinfo=datetime.timezone.utc)),
        ),
    ]