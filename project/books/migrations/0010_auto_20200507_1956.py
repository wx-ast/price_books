# Generated by Django 3.0.5 on 2020-05-07 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_orderitem_publisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='loader_type',
            field=models.CharField(choices=[('em', 'ЭКСМО'), ('l2', 'Азбука-КоЛибри-Махаон-Иностранка'), ('ak', 'Аквилегия'), ('pt', 'Питер'), ('kk', 'Книжный клуб'), ('am', 'ТД Амадеос'), ('zc', 'Загря center'), ('um', 'Умка')], max_length=2, verbose_name='Загрузчик'),
        ),
    ]
