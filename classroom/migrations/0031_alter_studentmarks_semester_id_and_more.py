# Generated by Django 5.0.6 on 2024-06-10 17:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0030_rename_semester_semester_semester_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentmarks',
            name='semester_id',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='classassignment',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 10, 17, 36, 3, 833637, tzinfo=datetime.timezone.utc)),
        ),
        migrations.DeleteModel(
            name='Semester',
        ),
    ]