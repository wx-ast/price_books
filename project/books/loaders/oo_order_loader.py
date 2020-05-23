from ..models import OrderItem
from ..utils import process_order_item


class OrderLoader:
    order = None

    def __init__(self, order):
        self.order = order

    def process_line(self, row):
        data = {
            'name': row[1],
            'author': row[2],
            'binding': row[3],
            'quantity': int(row[5]),
            'publisher': row[4],
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
