from django.contrib import admin
from store.models import Item as Product, Order, OrderDetail, Category


admin.site.register(Order)
admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'mojodi', 'active']
    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['item', 'price', 'count', 'date_added']