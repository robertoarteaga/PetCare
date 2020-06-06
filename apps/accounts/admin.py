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

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['model_instance'] = Customer.objects.get(pk=object_id)
        extra_context['orders'] = Order.objects.filter(customer_id=object_id)
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'date_created')
    ordering = ['date_created']
    list_filter = (        
        'date_created',
        'status',
        'product',
    )
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
