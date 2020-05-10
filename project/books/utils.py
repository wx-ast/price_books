import re

from .models import OrderItem, Product


def process_order_item(data, order):
    if data['author'].find('Пескова И.М., Дмитриева Т.Н., Смирнова С.В., Куксина Н.В., Зото') >= 0:
        print(data)
    name_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                     data['name'].lower()))
    author_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                       data['author'].lower()))
    binding_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                        data['binding'].lower()))

    bindings = {
        'твердый': ['7', '7бц', '7б', 'дпружинатвердый', 'переплет',
                    '7бцел', '7бс', 'п', 'тв', 'полутв'],
        'мягкий': ['3', 'дпружинамягкий', 'обложка', 'облц', 'обл',
                   'о', 'мяг'],
        'картон': ['картон', '5'],
        'интегральный': ['7инт', 'интегральныйпереплетуфлак', '10',
                         'интегр']
    }
    # автоимп

    if len(name_search) > 0:
        products = Product.objects.filter(name_search=name_search)
        if len(products) > 0:
            if len(author_search) > 0:
                if binding_search in bindings and len(binding_search) > 0:
                    products2 = products.filter(
                        author_search=author_search,
                        binding_search__in=bindings[binding_search]
                    )
                    if len(products2) > 0:
                        return True, {
                            'status': 1,
                            'product': products2[0],
                            'count': len(products2)
                        }

                products3 = products.filter(author_search=author_search)
                if len(products3) > 0:
                    return True, {
                        'status': 2,
                        'product': products3[0],
                        'count': len(products3)
                    }

            return True, {
                'status': 3,
                'product': products[0],
                'count': len(products)
            }

    return False, None