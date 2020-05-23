import re

from ..models import Product


class Loader:
    price_multiplier = 0.9
    started = False
    supplier = None
    bindings = []

    def __init__(self, supplier):
        self.supplier = supplier

    def process_line(self, row):
        name = row[1]
        if name == 'Наименование':
            self.started = True
            return True
        if not self.started:
            return True

        if isinstance(name, int):
            name = str(name)

        if name is None or len(name) <= 0 or\
                row[3] is None or\
                (isinstance(row[11], float) and row[11] <= 0)\
                or (isinstance(row[11], str) and len(row[11]) <= 0):
            return True
        name = name.strip()
        groups = re.findall('(?P<year>([\(]{1}[\d]*[\)]{1}$))', name)
        if len(groups) > 0:
            name = name[:-len(groups[0][0])].strip()

        author = row[4].strip() if row[4] is not None else ''

        data = {
            'price': round(float(row[11]) * self.price_multiplier, 2),
            'name': name,
            'author': author,
            'article': row[3].strip() if isinstance(row[3], str) else str(
                row[3]),
            'binding': row[7].strip() if isinstance(row[7], str) else str(
                row[7]),
            'publisher': row[5].strip()
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

        return True
