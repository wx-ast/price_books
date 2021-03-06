import os
import csv

import xlwt
from server_timing.middleware import timed_wrapper, TimedService, timed
from celery.result import AsyncResult

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.views.generic import View
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist

from .forms import PriceForm, OrderForm
from .models import Supplier, Order, OrderItem
from .utils import json_response
from core.celery import app
from .tasks import load_price, load_order, update_order


class FileUploadBaseView(TemplateResponseMixin, ContextMixin, View):
    template_name = 'books/load_file.html'
    form_cls = PriceForm
    started = False
    loader = None
    i = 0

    def __init__(self, *args, **kwargs):
        super(FileUploadBaseView, self).__init__(*args, **kwargs)
        self.form = self.form_cls()

    def post(self, request):
        post_service = TimedService('post')
        post_service.start()

        if not request.FILES:
            data = {
                'error': True,
                'error_text': 'file not posted'
            }
            return self.render_to_response(self.get_context_data(**data))

        form = self.form_cls(request.POST, request.FILES)
        if not form.is_valid():
            data = {
                'error': True,
                'error_text': 'form not valid'
            }
            return self.render_to_response(self.get_context_data(**data))

        if not self.process_post_data(form.cleaned_data):
            data = {
                'error': True,
                'error_text': 'что-то пошло не так'
            }
            return self.render_to_response(self.get_context_data(**data))

        postfile = request.FILES['file']
        filename, file_extension = os.path.splitext(postfile.name)
        if file_extension not in ('.xls', '.xlsx'):
            data = {
                'form': form,
                'error': True,
                'error_text': 'Поддерживаются только *.xls, *.xlsx'
            }
            return self.render_to_response(self.get_context_data(**data))

        fs_storage = FileSystemStorage()
        filename = fs_storage.save(postfile.name, postfile)
        uploaded_file_path = fs_storage.path(filename)

        ret = self.create_async_task(file_extension, uploaded_file_path)

        data = {
            'message': 'Загрузка запущена',
            'task_id': ret.id,
            'task_type': self.task_type
        }
        post_service.end()
        with timed('render'):
            return self.render_to_response(self.get_context_data(**data))

    def get(self, *args, **kwargs):
        data = {
            'form': self.form
        }
        return self.render_to_response(self.get_context_data(**data))

    def process_post_data(self, data):
        print(data)
        return True


class PriceLoadView(FileUploadBaseView):
    task_type = 'supplier'

    def process_post_data(self, data):
        supplier = Supplier.objects.get(
            pk=data.get('supplier'))

        self.supplier_id = supplier.pk
        return True

    def create_async_task(self, file_extension, uploaded_file_path):
        return load_price.apply_async((
            file_extension, uploaded_file_path, self.supplier_id))


class OrderLoadView(FileUploadBaseView):
    form_cls = OrderForm
    task_type = 'order'

    def process_post_data(self, data):
        order = Order(name=data['file'].name)
        order.save()

        self.order_id = order.pk
        self.order_loader = data.get('loader', 'df')
        return True

    def create_async_task(self, file_extension, uploaded_file_path):
        return load_order.apply_async((
            file_extension, uploaded_file_path, self.order_loader, self.order_id))


@staff_member_required
@timed_wrapper('index')
def index(request):
    home_service = TimedService('select')
    home_service.start()

    orders = Order.objects.all()
    items = []
    for order in orders:
        data = {
            'order': order,
            'count': {},
            'count_all': OrderItem.objects.filter(order=order).count()
        }
        for i in range(5):
            data['count'][i] = OrderItem.objects.\
                filter(order=order, status=i).count()

        items.append(data)
    home_service.end()
    context = {
        'items': items
    }

    with timed('render'):
        return render(request, 'books/index.html', context)


@staff_member_required
def order_table(request, order_id, status):
    items = OrderItem.objects.filter(order=order_id, status=status)

    context = {
        'items': items,
        'status': status
    }
    return render(request, 'books/order_table.html', context)


@staff_member_required
def get_csv_file(request, order_id, status):
    items = OrderItem.objects.filter(order=order_id, status=status)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        f'attachment; filename="order_{status}.csv"'

    writer = csv.writer(response, delimiter=';', quotechar='"')
    for item in items:
        row = [item.count, item.name, item.author, item.binding,
               item.publisher, item.quantity]
        if item.product:
            row.append(item.product.article)
            row.append(item.product.author)
            row.append(item.product.publisher)
            row.append(item.product.binding)
            row.append(item.product.price)
            row.append(item.product.supplier.name)
        writer.writerow(row)

    return response


@staff_member_required
def get_xls_file(request, order_id, status):
    items = OrderItem.objects.filter(order=order_id, status=status)

    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet(f'order_{status}')

    i = j = 0
    for item in items:
        row = [item.count, item.name, item.author, item.binding,
               item.publisher, item.quantity]
        if item.product:
            row.append(item.product.article)
            row.append(item.product.author)
            row.append(item.product.publisher)
            row.append(item.product.binding)
            row.append(item.product.price)
            row.append(item.product.supplier.name)

        for cell in row:
            worksheet.write(i, j, cell)
            j += 1
        i += 1
        j = 0

    file_path = os.path.join(settings.MEDIA_ROOT, f'order_{status}.xls')
    workbook.save(file_path)
    xlsfile = open(file_path, 'rb')
    file_data = xlsfile.read()
    xlsfile.close()

    response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = \
        f'attachment; filename="order_{status}.xls"'
    return response


@staff_member_required
def order_update(request, order_id):
    ret = update_order.apply_async((order_id,))

    context = {
        'message': 'Обновление запущено',
        'task_id': ret.id,
        'task_type': 'order'
    }
    return render(request, 'books/load_file.html', context)


@staff_member_required
def order_delete(request, order_id):
    Order.objects.get(pk=order_id).delete()

    return redirect(reverse('index'))


def async_task_status(request):
    task_ids = request.POST.get('task_ids')
    task_type = request.POST.get('task_type')
    response_data = {'status': {}, 'file': {}}
    if task_ids:
        task_ids = task_ids.split(';')
        for task_id in task_ids:
            result = AsyncResult(id=task_id, app=app)
            response_data['status'][task_id] = {'status': result.status}
            try:
                if task_type == 'supplier':
                    obj = Supplier.objects.get(task_id=task_id)
                else:
                    obj = Order.objects.get(task_id=task_id)
                response_data['status'][task_id]['text'] = obj.task_status
            except ObjectDoesNotExist:
                response_data['status'][task_id]['text'] = 'Ошибка 2'
    else:
        response_data['error'] = True
        print('EMPTY task ids list')
    return json_response(response_data)
