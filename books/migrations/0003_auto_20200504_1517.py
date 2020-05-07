# Generated by Django 3.0.5 on 2020-05-04 12:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20200504_1032'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-date_create'], 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AddField(
            model_name='order',
            name='date_create',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 5, 4, 15, 17, 45, 640613), verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(default='default', max_length=127, verbose_name='Название'),
            preserve_default=False,
        ),
    ]
