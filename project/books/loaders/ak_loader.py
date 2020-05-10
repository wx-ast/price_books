import re

from ..models import Product


class Loader:
    price_multiplier = 0.7
    started = False
    supplier = None
    # i = 0
    bindings = []

    predefined_authors = [
        'Лада Кутузова',
        'Надея Ясминска',
        'Майя Лазаренская',
        'Алека Вольских',
        'Пальмира Керлис',
        'Катерина Фрок',
        'Эльвира Смелик',
        'Аделия Амраева',
        'Леон Костевич',
        'Ая Эн'
    ]

    def __init__(self, supplier):
        self.supplier = supplier

    def process_line(self, row):
        if row[1] == 'Автор, наименование':
            self.started = True
            return True
        if not self.started:
            return True

        if len(row[1]) <= 0 or (isinstance(row[8], float) and row[8] <= 0) or \
                (isinstance(row[8], str) and len(row[8]) <= 0):
            return True
        name = row[1].replace('NEW', '').replace('НОВОЕ ОФОРМЛЕНИЕ', '').\
            replace('цветные иллюстрации, новый формат', '').strip()
        author = ''

        groups = re.findall('(?P<author>(^[А-ЯЁ]{1}\.\s*[А-ЯЁа-яё]+(\.?|,+)\s+)|(^[А-ЯЁ]{1}\s+[А-ЯЁа-яё]+(\.{1}|,+)\s+))', name)
        if len(groups) > 0:
            author = groups[0][0]
            name = name.replace(author, '').strip()
            author = author.strip().rstrip('.').rstrip(',').\
                replace('.', '. ').replace('  ', ' ')

            groups = re.findall('(?P<author>(^[А-ЯЁ]{1}\.\s*[А-ЯЁа-яё]+(\.?|,+)\s+)|(^[А-ЯЁ]{1}\s+[А-ЯЁа-яё]+(\.{1}|,+)\s+))', name)
            if len(groups) > 0:
                author2 = groups[0][0]
                name = name.replace(author2, '').strip()
                author2 = author2.strip().rstrip('.').rstrip(',').\
                    replace('.', '. ').replace('  ', ' ')
                if author2.find('.') < 0:
                    author2 = author2.replace(' ', '. ')
                author = f'{author}, {author2}'
        else:
            for item in self.predefined_authors:
                if name.find(item) >= 0:
                    name = name.replace(item, '').strip()
                    author = item
                    break

        data = {
            'price': round(float(row[8]) * self.price_multiplier, 2),
            'name': name,
            'author': author,
            'article': row[3].strip(),
            'binding': row[5].split(', ')[1].strip(),
            'publisher': 'АКВИЛЕГИЯ-М'
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

        # self.i += 1
        # if self.i > 20:
        #     return False

        return True
