# Generated by Django 5.0.6 on 2024-06-11 14:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0048_alter_classassignment_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmarks',
            name='viva_marks_obtained',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='classassignment',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 11, 14, 50, 23, 1941, tzinfo=datetime.timezone.utc)),
        ),
    ]
