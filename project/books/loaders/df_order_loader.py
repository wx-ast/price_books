from ..models import OrderItem
from ..utils import process_order_item


class OrderLoader:
    started = False
    order = None

    def __init__(self, order):
        self.order = order

    def process_line(self, row):
        row = [a for a in row if a != '' and a]
        data = {'quantity': 0}

        if len(row) == 5:
            data['name'] = str(row[1]) if isinstance(row[1], int) else\
                row[1].strip()
            data['author'] = ''
            data['binding'] = row[2].strip()
            data['publisher'] = row[3].strip()
            data['quantity'] = row[4]
        elif len(row) > 5:
            data['name'] = str(row[1]) if isinstance(row[1], int) else\
                row[1].strip()
            data['author'] = row[2].strip()
            data['name'] = data['name'].replace(data['author'], '').strip()
            data['binding'] = row[3].strip()
            data['publisher'] = row[4].strip() if isinstance(row[4], str) else\
                str(row[4])
            data['quantity'] = row[5]

        try:
            if data.get('quantity') is not None:
                data['quantity'] = int(data['quantity'])
            else:
                data['quantity'] = 0
        except ValueError:
            return True

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
