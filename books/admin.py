from django.contrib import admin

from .models import Supplier, Product, Order, OrderItem


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'loader_type')
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'binding', 'price', 'publisher',
                    'article', 'supplier')
    readonly_fields = ('name_search', 'author_search', 'binding_search')
    list_filter = ('supplier',)
    search_fields = ('name', 'article', 'author')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product',)
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_create')
    inlines = [
        OrderItemInline,
    ]


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
