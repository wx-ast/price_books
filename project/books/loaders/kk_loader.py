import re

from ..models import Product


class Loader:  # pylint: disable=too-few-public-methods
    price_multiplier = 0.8
    started = False
    supplier = None
    bindings = []

    def __init__(self, supplier):
        self.supplier = supplier

    def process_line(self, row):
        if row[3] == 'Название':
            self.started = True
            return True
        if not self.started:
            return True

        if row[3] is None or len(row[3]) <= 0:
            return True
        if row[7] is None or (isinstance(row[6], float) and row[6] <= 0)\
                or (isinstance(row[6], str) and len(row[6]) <= 0):
            return True
        name = row[3].replace('(новая обложка)', '').replace(
            '( новая обложка)', '').strip()
        author = row[2].strip() if row[2] is not None else ''
        binding = row[12].strip() if isinstance(row[12], str) else str(row[12])

        data = {
            'price': round(float(row[6]) * self.price_multiplier, 2),
            'name': name,
            'author': author,
            'article': row[7].strip(),
            'binding': binding,
            'publisher': row[4].strip()
        }

        name_search = ''.join(re.findall("[a-z0-9а-яё]+", name.lower()))
        author_search = ''.join(re.findall("[a-z0-9а-яё]+", author.lower()))
        binding_search = ''.join(re.findall(
            "[a-z0-9а-яё]+", data['binding'].lower()))

        data['name_search'] = name_search
        data['author_search'] = author_search
        data['binding_search'] = binding_search

        if data['binding'] not in self.bindings:
            self.bindings.append(data['binding'])
        product = Product(supplier=self.supplier, **data)
        product.save()

        return True
