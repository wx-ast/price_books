from django.db import models


class Supplier(models.Model):
    LOADER_TYPES = (
        ('em', 'ЭКСМО'),
        ('l2', 'Азбука-КоЛибри-Махаон-Иностранка'),
        ('ak', 'Аквилегия'),
        ('pt', 'Питер'),
        ('kk', 'Книжный клуб'),
        ('am', 'ТД Амадеос'),
        ('zc', 'Загря center'),
        ('um', 'Умка'),
    )
    name = models.CharField('Название', max_length=127)
    slug = models.SlugField('Символьный код', max_length=127)
    loader_type = models.CharField('Загрузчик', max_length=2,
                                   choices=LOADER_TYPES)

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Название', max_length=127)
    author = models.CharField('Автор', max_length=63, null=True, blank=True)
    binding = models.CharField('Переплет', max_length=31, null=True,
                               blank=True)
    article = models.CharField('Артикул', max_length=127)
    price = models.FloatField('Цена')
    publisher = models.CharField('Издатель', max_length=63, null=True,
                                 blank=True)
    supplier = models.ForeignKey(Supplier, verbose_name='Поставщик',
                                 on_delete=models.CASCADE)
    name_search = models.CharField('Название (поиск)', max_length=127,
                                   null=True, blank=True)
    author_search = models.CharField('Автор (поиск)', max_length=63,
                                     null=True, blank=True)
    binding_search = models.CharField('Переплет (поиск)', max_length=31,
                                      null=True, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['price']

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField('Название', max_length=127)
    date_create = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-date_create']

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ',
                              on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=127)
    author = models.CharField('Автор', max_length=63)
    binding = models.CharField('Переплет', max_length=31, null=True,
                               blank=True)
    quantity = models.IntegerField('Количество', null=True, blank=True)
    publisher = models.CharField('Издатель', max_length=63,
                                 null=True, blank=True)
    product = models.ForeignKey(Product, verbose_name='Товар',
                                on_delete=models.SET_NULL, null=True)
    status = models.IntegerField('Статус', default=0)
    count = models.IntegerField('Найденное количество товаров', default=0)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
