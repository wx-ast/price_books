from django.forms import Form, FileField, ChoiceField

from .models import Supplier


def get_all_suppliers():
    return [(a.pk, a.name) for a in Supplier.objects.all()]


class PriceForm(Form):
    supplier = ChoiceField(label='Поставщик', choices=get_all_suppliers)
    file = FileField(label='*.xls, *.xlsx')


class OrderForm(Form):
    file = FileField(label='*.xls, *.xlsx')
