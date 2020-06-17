import re

from ..models import Product


class Loader:  # pylint: disable=too-few-public-methods
    price_multiplier = 1
    started = False
    supplier = None
    bindings = []

    def __init__(self, supplier):
        self.supplier = supplier

    def process_line(self, row):
        if row[3] == 'Наименование':
            self.started = True
            return True
        if not self.started:
            return True

        if row[3] is None or len(row[3]) <= 0:
            return True

        price = row[6] if row[7] == 'шт' else row[7]

        if row[2] is None or (isinstance(price, float) and price <= 0)\
                or (isinstance(price, str) and len(price) <= 0)\
                or price is None:
            return True

        name = row[3].strip()
        author = ''
        binding = 'none'

        groups = re.findall('(?P<author>(\s*[А-ЯЁ]{1}[А-ЯЁа-яё]+\s{1}[А-ЯЁ]{1}\.{1}([А-ЯЁ]{1}\.?)?(\s{1}и др\.)?))', name)
        if len(groups) > 0:
            author = groups[0][0]
            name = name.replace(author, '').strip()
            author = author.strip()

        data = {
            'price': round(float(price) * self.price_multiplier, 2),
            'name': name,
            'author': author,
            'article': row[2].strip(),
            'binding': binding,
            'publisher': 'Китол'
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
