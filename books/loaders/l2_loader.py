import re

from ..models import Product


class Loader:
    price_multiplier = 0.82
    started = False
    supplier = None
    i = 0
    bindings = []
    publisher = ''

    def __init__(self, supplier):
        self.supplier = supplier

    def process_line(self, row):
        if row[4] == 'Название':
            self.started = True
            return True
        if not self.started:
            return True

        if row[0] is None and row[1] is None and isinstance(row[2], str):
            if row[2].find('Книги издательства "') == 0:
                self.publisher = row[2].strip()[20:-1]
            return True
        name = row[4]
        author = row[3]
        if name is None:
            return True

        name = name.replace('(мягк/обл.)', '').replace('(нов/обл.)', '').\
            replace('(нов/обл.*)', '').replace('(нов/оф.)', '').\
            replace('(нов/обл)', '')
        if name.find(f'/{author}') > 0:
            name = name.replace(f'/{author}', '')

        name_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                         name.lower()))
        if author is not None:
            author_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                               author.lower()))
        else:
            author_search = ''

        binding_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                            row[10].lower()))

        if row[10] not in self.bindings:
            self.bindings.append(row[10])
        data = {
            'price': round(float(row[7]) * self.price_multiplier, 2),
            'name': name.strip(),
            'author': author.strip() if author is not None else '',
            'article': row[1].strip(),
            'binding': row[10].strip(),
            'publisher': self.publisher,
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
