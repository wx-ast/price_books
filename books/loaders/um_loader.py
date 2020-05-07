import re

from ..models import Product


class Loader:
    price_multiplier = 0.75
    started = False
    supplier = None
    # i = 0
    bindings = []
    binding = ''

    def __init__(self, supplier):
        self.supplier = supplier

    def process_line(self, row):
        if row[3] == 'Наименование':
            self.started = True
            return True
        if not self.started:
            return True

        if row[1] is None:
            if row[0] is None:
                return True
            if row[0].lower().find('твердом') > 0:
                self.binding = '7'
            elif row[0].lower().find('картон') > 0:
                self.binding = 'картон'
            elif row[0].lower().find('мягк') > 0:
                self.binding = '3'
            else:
                self.binding = ''
            return True

        name = row[3]
        if name is None:
            return True
        name = name.strip()

        if isinstance(row[8], str):
            price = round(float(row[8].replace(',', '.')) * self.price_multiplier, 2)
        else:
            price = round(float(row[8]) * self.price_multiplier, 2)

        data = {
            'price': price,
            'name': name,
            'author': '',
            'article': str(row[1]).strip(),
            'binding': self.binding,
            'publisher': 'Умка'
        }

        name_search = ''.join(re.findall("[a-z0-9а-яё]+", name.lower()))
        author_search = ''
        binding_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                            data['binding'].lower()))

        data['name_search'] = name_search
        data['author_search'] = author_search
        data['binding_search'] = binding_search

        if data['binding'] not in self.bindings:
            self.bindings.append(data['binding'])
        product = Product(supplier=self.supplier, **data)
        product.save()

        # self.i += 1
        # if self.i > 20:
        #     return False

        return True
