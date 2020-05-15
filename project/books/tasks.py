import os
import importlib
from time import time

import xlrd
from openpyxl import load_workbook

from core.celery import app
from .models import Supplier, Order, Product


@app.task(bind=True)
def load_price(self, file_extension, uploaded_file_path, supplier_id):
    print('#'*79)
    print('load_price')

    supplier = Supplier.objects.get(pk=supplier_id)
    supplier.task_id = self.request.id
    supplier.task_status = 'Удаление товаров поставщика'
    supplier.save()
    Product.objects.filter(supplier=supplier).delete()

    supplier.task_status = 'Загрузка...'
    supplier.save()
    try:
        loader_module = importlib.import_module(
            f'.loaders.{supplier.loader_type}_loader',
            package=__package__
        )
        loader = loader_module.Loader(supplier)
    except ModuleNotFoundError as e:
        print(e)
        supplier.task_status = 'Ошибка'
        supplier.save()
        return False

    i = load_file(file_extension, uploaded_file_path, loader, supplier)

    supplier.task_status = f'Готово ({i})'
    supplier.save()


@app.task(bind=True)
def load_order(self, file_extension, uploaded_file_path, order_loader,
               order_id):
    print('#'*79)
    print('load_order')

    order = Order.objects.get(pk=order_id)
    order.task_id = self.request.id
    order.task_status = 'Загрузка начата'
    order.save()
    try:
        loader_module = importlib.import_module(
            f'.loaders.{order_loader}_order_loader',
            package=__package__
        )
        loader = loader_module.OrderLoader(order)
    except ModuleNotFoundError as e:
        print(e)
        order.task_status = 'Ошибка'
        order.save()
        return False

    i = load_file(file_extension, uploaded_file_path, loader, order)

    order.task_status = f'Готово ({i})'
    order.save()


def load_file(file_extension, uploaded_file_path, loader, target):
    i = 0
    start = time()

    if file_extension == '.xls':
        workbook = xlrd.open_workbook(
            uploaded_file_path,
            formatting_info=False
        )
        sheet = workbook.sheet_by_index(0)
        for rownum in range(sheet.nrows):
            row = sheet.row_values(rownum)
            if not loader.process_line(row):
                break
            i += 1
            if time() - start > 1:
                start = time()
                target.task_status = f'Обработано записей: {i}'
                target.save()
    elif file_extension == '.xlsx':
        workbook = load_workbook(
            filename=uploaded_file_path,
            read_only=True
        )
        worksheet = workbook.active
        for row in worksheet.rows:
            row = [cell.value for cell in row]
            if not loader.process_line(row):
                break
            i += 1
            if time() - start > 1:
                start = time()
                target.task_status = f'Обработано записей: {i}'
                target.save()

    if hasattr(loader, 'bindings') and \
            loader.bindings is not None:
        print('bindings:', loader.bindings)

    os.remove(uploaded_file_path)

    return i
