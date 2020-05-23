import re

from ..models import Product


class Loader:
    price_multiplier = 0.55
    started = False
    supplier = None
    bindings = []

    def __init__(self, supplier):
        self.supplier = supplier

    def process_line(self, row):
        if row[4] == 'Название':
            self.started = True
            return True
        if not self.started:
            return True

        if row[4] is None or len(row[4]) <= 0 or\
                row[17] is None or\
                (isinstance(row[15], float) and row[15] <= 0)\
                or (isinstance(row[15], str) and len(row[15]) <= 0):
            return True
        name = row[4].strip()
        author = row[6].strip() if row[6] is not None else ''
        name = name.replace(author, '').strip()

        data = {
            'price': round(float(row[15]) * self.price_multiplier, 2),
            'name': name,
            'author': author,
            'article': row[17].strip(),
            'binding': row[13].strip() if isinstance(row[13], str) else str(
                row[13]),
            'publisher': row[9].strip()
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
