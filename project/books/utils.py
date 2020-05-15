import re
import json

from django.http import HttpResponse

from .models import Product


def process_order_item(data, order):
    name_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                     data['name'].lower()))
    author_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                       data['author'].lower()))
    binding_search = ''.join(re.findall("[a-z0-9а-яё]+",
                                        data['binding'].lower()))

    bindings = {
        'твердый': ['7', '7бц', '7б', 'дпружинатвердый', 'переплет',
                    '7бцел', '7бс', 'п', 'тв', 'полутв',
                    'твердыйпереплетвироспираль', 'твердыйпереплетфутляр',
                    'твердыйпереплеткожа', 'твердыйпереплетткань',
                    'твердыйпереплет'],
        'мягкий': ['3', 'дпружинамягкий', 'обложка', 'облц', 'обл',
                   'о', 'мяг', 'мягкаяобложка'],
        'картон': ['картон', '5'],
        'интегральный': ['7инт', 'интегральныйпереплетуфлак', '10',
                         'интегр', 'интегральныйпереплет'],
    }
    for a in ('7бц', '7б', '7', '7бц', 'переплет'):
        bindings[a] = bindings['твердый']
    for a in ('покет', 'обл', 'обложка'):
        bindings[a] = bindings['мягкий']

    # автоимп
    # коробка
    # папка
    # резина

    if len(data.get('article', '')) > 0:
        products = Product.objects.filter(article=data.get('article', ''))
        if len(products) > 0:
            return True, {
                'status': 4,
                'product': products[0],
                'count': len(products)
            }

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


def json_response(data):
    mimetype = 'application/javascript'
    data = json.dumps(data)
    return HttpResponse(data, mimetype)
