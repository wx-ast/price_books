# Generated by Django 3.0.5 on 2020-05-05 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_orderitem_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['price'], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AddField(
            model_name='product',
            name='publisher',
            field=models.CharField(blank=True, max_length=63, null=True, verbose_name='Издатель'),
        ),
    ]
