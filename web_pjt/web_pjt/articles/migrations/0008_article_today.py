# Generated by Django 2.1.15 on 2020-06-15 08:32

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_auto_20200612_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='today',
            field=models.DateField(default=django.utils.timezone.now, verbose_name=datetime.datetime(2020, 6, 15, 17, 32, 20, 560656)),
            preserve_default=False,
        ),
    ]