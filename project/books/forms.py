from django.forms import Form, FileField, ChoiceField

from .models import Supplier


def get_all_suppliers():
    return [(a.pk, a.name) for a in Supplier.objects.all()]


class PriceForm(Form):
    supplier = ChoiceField(label='Поставщик', choices=get_all_suppliers)
    file = FileField(label='*.xls, *.xlsx')


class OrderForm(Form):
    loader = ChoiceField(label='Обработчик', choices=(
        ('df', 'По умолчанию'),
        ('nf', 'Нет в наличии'),
        ('oo', 'Нулевой')
    ))
    file = FileField(label='*.xls, *.xlsx')
