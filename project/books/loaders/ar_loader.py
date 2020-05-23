import re

from ..models import Product


class Loader:
    price_multiplier = 0.7
    started = False
    supplier = None
    bindings = []

    def __init__(self, supplier):
        self.supplier = supplier

    def process_line(self, row):
        if row[1] == 'Название книги':
            self.started = True
            return True
        if not self.started:
            return True

        if row[1] is None or len(row[1]) <= 0 or\
                row[12] is None or\
                (isinstance(row[5], float) and row[5] <= 0)\
                or (isinstance(row[5], str) and len(row[5]) <= 0):
            return True
        name = row[1].strip()
        author = row[2].strip() if row[2] is not None else ''
        name = name.replace(author, '').strip()
        price = row[5].replace(',', '.') if isinstance(row[5], str) else row[5]
        price = round(float(price) * self.price_multiplier, 2)

        data = {
            'price': price,
            'name': name,
            'author': author,
            'article': row[12].strip(),
            'binding': row[10].strip() if isinstance(row[10], str) else str(
                row[10]),
            'publisher': row[7].strip()
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
