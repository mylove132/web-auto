# Generated by Django 2.2 on 2019-04-19 21:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teacherspace', '0002_auto_20190419_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2019, 4, 19, 21, 38, 23, 230687, tzinfo=utc)),
            preserve_default=False,
        ),
    ]