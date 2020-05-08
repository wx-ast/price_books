from django.urls import path

from .views import PriceLoadView, OrderLoadView, index, get_csv,\
     get_csv_file, get_xls_file, order_update


urlpatterns = [
    path('', index, name='index'),
    path('price', PriceLoadView.as_view(), name='price_load_view'),
    path('order/', OrderLoadView.as_view(), name='order_load_view'),
    path('order/<int:order_id>/update', order_update, name='order_update'),
    path('get_csv/', get_csv, name='get_csv'),
    path('get_csv/<int:order_id>/<int:status>/', get_csv, name='get_csv'),
    path('get_csv_file/<int:order_id>/<int:status>/', get_csv_file,
         name='get_csv_file'),
    path('get_xls_file/<int:order_id>/<int:status>/', get_xls_file,
         name='get_xls_file'),
]
