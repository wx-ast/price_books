import re

from ..models import Product


class Loader:
    price_multiplier = 0.74
    started = False
    supplier = None
    bindings = []
    pattern = re.compile(r'(\(#\d+\)$)')
    pattern2 = re.compile(r'(\(ил\.[.А-ЯЁа-яё\s]+\)$)')

    def __init__(self, supplier):
        self.supplier = supplier

    def process_line(self, row):
        if row[4] == 'Стоимость':
            self.started = True
            return True
        if not self.started:
            return True

        name = row[5].strip()
        groups = self.pattern.findall(name)
        if len(groups) > 0:
            name = name.replace(groups[0], '').strip()
        # groups = self.pattern2.findall(name)
        # if len(groups) > 0:
        #     print(groups)
        #     name = name.replace(groups[0], '').strip()

        name_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                         name.lower()))
        author_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                           row[6].lower()))
        binding_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                            row[29].lower()))

        if row[29] not in self.bindings:
            self.bindings.append(row[29])
        data = {
            'price': round(float(row[4]) * self.price_multiplier, 2),
            'name': name.strip(),
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

        return True
