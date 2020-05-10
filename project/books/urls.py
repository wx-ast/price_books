from django.urls import path, include
from django.contrib.admin.views.decorators import staff_member_required

from .views import PriceLoadView, OrderLoadView, index, order_table,\
     get_csv_file, get_xls_file, order_update, order_delete


urlpatterns = [
    path('', index, name='index'),
    path('price', staff_member_required(PriceLoadView.as_view()),
         name='price_load_view'),
    path('order/', staff_member_required(OrderLoadView.as_view()),
         name='order_load_view'),
    path('order/<int:order_id>/update', order_update, name='order_update'),
    path('order/<int:order_id>/delete', order_delete, name='order_delete'),
    path('order_table/', order_table, name='order_table'),
    path('order_table/<int:order_id>/<int:status>/', order_table,
         name='order_table'),
    path('get_csv_file/<int:order_id>/<int:status>/', get_csv_file,
         name='get_csv_file'),
    path('get_xls_file/<int:order_id>/<int:status>/', get_xls_file,
         name='get_xls_file')
]
