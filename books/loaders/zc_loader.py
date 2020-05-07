import re

from ..models import Product


class Loader:
    price_multiplier = 0.7
    started = False
    supplier = None
    # i = 0
    bindings = []

    def __init__(self, supplier):
        self.supplier = supplier

    def process_line(self, row):
        name = row[4]
        if name == 'Название':
            self.started = True
            return True
        if not self.started:
            return True

        if isinstance(name, int):
            name = str(name)

        if name is None or len(name) <= 0 or\
                row[9] is None or\
                (isinstance(row[6], float) and row[6] <= 0)\
                or (isinstance(row[6], str) and len(row[6]) <= 0):
            return True
        name = name.strip()
        author = row[3].strip() if row[3] is not None else ''
        name = name.replace(author, '').strip()

        data = {
            'price': round(float(row[6]) * self.price_multiplier, 2),
            'name': name,
            'author': author,
            'article': row[9].strip() if isinstance(row[9], str) else str(
                row[9]),
            'binding': row[11].strip() if isinstance(row[11], str) else str(
                row[11]),
            'publisher': 'ЦЕНТРПОЛИГРАФ'
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
