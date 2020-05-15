from ..models import OrderItem
from ..utils import process_order_item


class OrderLoader:
    started = False
    order = None
    # i = 0
    bindings = []

    def __init__(self, order):
        self.order = order

    def process_line(self, row):
        if row[2] == 4 and row[3] == 5 and row[4] == 6:
            self.started = True
            return True
        if not self.started:
            return True

        if row[3] is None:
            return True

        data = {
            'name': str(row[3]) if not isinstance(row[3], str) else row[3].strip(),
            'author': row[4].strip() if isinstance(row[4], str) else '',
            'binding': row[14].strip() if isinstance(row[14], str) else str(
                row[14]),
            'quantity': int(row[2]),
            'article': '',
            'publisher': '',
        }

        if data['quantity'] <= 0:
            print(row)
            return True

        if data['binding'] not in self.bindings:
            self.bindings.append(data['binding'])

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

        # self.i += 1
        # print(self.i, len(row), data)
        # if 5 < len(row) > 6:
        #     print(self.i, len(row), row)
        # if self.i > 20:
        #     return False

        return True
