import re

from ..models import Product


class Loader:
    price_multiplier = 0.74
    started = False
    supplier = None
    i = 0
    bindings = []

    def __init__(self, supplier):
        self.supplier = supplier

    def process_line(self, row):
        if row[4] == 'Стоимость':
            self.started = True
            return True
        if not self.started:
            return True

        name_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                         row[5].lower()))
        author_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                           row[6].lower()))
        binding_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                            row[29].lower()))

        if row[29] not in self.bindings:
            self.bindings.append(row[29])
        data = {
            'price': round(float(row[4]) * self.price_multiplier, 2),
            'name': row[5].strip(),
            'author': row[6].strip(),
            'article': row[18].strip(),
            'binding': row[29].strip(),
            'publisher': row[16].strip(),
            'name_search': name_search,
            'author_search': author_search,
            'binding_search': binding_search,
        }
        product = Product(supplier=self.supplier, **data)
        product.save()

        # self.i += 1
        # if self.i > 20:
        #     return False

        return True
