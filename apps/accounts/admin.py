from django.contrib import admin

#from .models import *
from . models import Customer, Order, Product

# admin.site.register(Customer)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'date_created')

    search_fields = (
        'name',
        'email',
    )
    list_filter = (        
        'date_created',
    )

class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'date_created')

    list_filter = (        
        'date_created',
        'product',
    )
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
