# Generated by Django 3.0.6 on 2020-05-12 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0014_auto_20200511_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='name',
            field=models.CharField(max_length=511, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=511, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_search',
            field=models.CharField(blank=True, db_index=True, max_length=511, null=True, verbose_name='Название (поиск)'),
        ),
    ]
