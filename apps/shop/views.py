from django.shortcuts import render
from django.http import JsonResponse

from apps.accounts.models import Product, Order, Customer
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def buy_product(request):
    try:
        cuantity = int(request.POST['cuantity'])
        product = Product.objects.get(pk=int(request.POST['product_id']))
        customer = Customer.objects.get(pk=int(request.POST['user_id']))
        for i in range(0, cuantity):
            Order.objects.create(customer=customer, product=product, status='Pending')
            print("Orden lista")
        return JsonResponse({'data':""})
    except Exception as e:
        print(e)
        return JsonResponse({'data':None})