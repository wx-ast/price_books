import re

from ..models import Product


class Loader:
    price_multiplier = 0.93
    started = False
    supplier = None
    # i = 0
    bindings = []

    def __init__(self, supplier):
        self.supplier = supplier

    def process_line(self, row):
        if row[6] == 'Наименование':
            self.started = True
            return True
        if not self.started:
            return True

        if row[6] is None or len(row[6]) <= 0 or\
                row[4] is None or\
                (isinstance(row[10], float) and row[10] <= 0)\
                or (isinstance(row[10], str) and len(row[10]) <= 0):
            return True
        name = row[6].strip()
        author = row[5].strip() if row[5] is not None else ''

        data = {
            'price': round(float(row[10]) * self.price_multiplier, 2),
            'name': name,
            'author': author,
            'article': row[4].strip(),
            'binding': row[14].strip() if isinstance(row[14], str) else str(
                row[14]),
            'publisher': 'Питер'
        }

        name_search = ''.join(re.findall("[a-z0-9а-яё]+", name.lower()))
        author_search = ''.join(re.findall("[a-z0-9а-яё]+", author.lower()))
        binding_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                            data['binding'].lower()))

        data['name_search'] = name_search
        data['author_search'] = author_search
        data['binding_search'] = binding_search

        if data['binding'] not in self.bindings:
            self.bindings.append(data['binding'])
        product = Product(supplier=self.supplier, **data)
        product.save()
        # print(data)

        # self.i += 1
        # if self.i > 20:
        #     return False

        return True
