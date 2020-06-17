import re

from ..models import OrderItem
from ..utils import process_order_item


class OrderLoader:
    started = False
    order = None

    def __init__(self, order):
        self.order = order

    def process_line(self, row):
        if row[1] == 'Название':
            self.started = True
            return True
        if not self.started:
            return True
        if row[1] == 'Итого':
            return

        name = row[1].strip()
        author = ''

        groups = re.findall('(?P<author>^([А-ЯЁ]{1}[А-ЯЁа-яё]+\s{1}[А-ЯЁ]{1}\.{1}([А-ЯЁ]{1}\.{1})?(\s{1}и др\.)?))', name)
        if len(groups) > 0:
            author = groups[0][0]
            name = name.replace(author, '').strip()
            author = author.strip()

        data = {
            'name': name,
            'author': author,
            'binding': 'none',
            'quantity': int(row[4]),
            'article': '',
            'publisher': '',
        }

        if data['quantity'] <= 0:
            print(row)
            return True

        ret, ret_data = process_order_item(data, self.order)
        if ret:
            item = OrderItem(
                order=self.order,
                product=ret_data['product'],
                status=ret_data['status'],
                count=ret_data['count'],
                **data
            )
        else:
            item = OrderItem(order=self.order, **data)
        item.save()

        return True
