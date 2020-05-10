# Generated by Django 3.0.6 on 2020-05-10 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0013_auto_20200511_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='article',
            field=models.CharField(db_index=True, max_length=127, verbose_name='Артикул'),
        ),
        migrations.AlterField(
            model_name='product',
            name='author_search',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Автор (поиск)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='binding_search',
            field=models.CharField(blank=True, db_index=True, max_length=31, null=True, verbose_name='Переплет (поиск)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_search',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Название (поиск)'),
        ),
    ]
