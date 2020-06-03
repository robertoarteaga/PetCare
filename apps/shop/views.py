import json
from django.core import serializers
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import Http404
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# from django.db.models import Count
from django.db import connection
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import views as admin_views
from apps.accounts.models import Product
from apps.accounts.forms import *
from django.db.models import *
from apps.accounts.models import Product, Order, Customer
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def shop(request):
    products = Product.products.all()
    return render(request, 'shop/shop.html', {'products':products})

def buy(request, id_product):
    """ Vista que muestra la vista de compra de un producto """
    try:
        product = Product.products.get(pk = id_product)
        return render(request, 'shop/buy.html', {'product':product})
    except Product.DoesNotExist:
        raise Http404("Producto inexistente")

def contract_service(request, id_service):
    """ Vista que muestra la vista de compra de un servicio """
    try:
        service = Product.services.get(pk = id_service)
        return render(request, 'shop/contract_service.html', {'service':service})
    except Product.DoesNotExist:
        raise Http404("Servicio inexistente")


def customer_login(request):
    """ Vista que muestra el html base par pruebas """
    return render(request, 'shop/customer_login.html', {})


def services(request):
    services = Product.services.all()
    return render(request, 'shop/services.html',{'services':services})

@csrf_exempt
@require_POST
def fake_customer_auth(request):
    try:
        data = {}
        customer = Customer.objects.get(pk=request.POST['customer_id'])
        data['pk'] = customer.pk
        data['id'] = customer.id
        data['email'] = customer.email
        data['phone'] = customer.email
        data['name'] = customer.name
        return JsonResponse(data)
    except:
        data = {}
        data['pk'] = 0
        data['id'] = 0
        data['email'] = None
        data['phone'] = None
        data['name'] = None
        return JsonResponse(data)

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

@csrf_exempt
def buy_service(request):
    try:
        service = Product.objects.get(pk=int(request.POST['service_id']))
        customer = Customer.objects.get(pk=int(request.POST['user_id']))
        Order.objects.create(customer=customer, product=service, status='Pending')
        print("================0")
        print("Servicio creado")
        print("================0")
        return JsonResponse({'data':None, 'success':True})
    except Exception as e:
        print(e)
        return JsonResponse({'data':None, 'success':False})

def cart(request):
    return render(request, 'shop/cart.html')


def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]
@csrf_exempt
def get_customer_cart(request):
    try:
        user_id = int(request.POST['user_id'])
        # data = Order.objects.filter(customer_id=user_id).values('product_name')
        # print(data)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM accounts_order o, accounts_product as p WHERE o.customer_id = %s AND p.id = o.product_id AND p.category <> 'Servicio' ORDER BY o.date_created;", [user_id])
            # rows = cursor.fetchall()
            products = dictfetchall(cursor)

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM accounts_order o, accounts_product as p WHERE o.customer_id = %s AND p.id = o.product_id AND p.category = 'Servicio' ORDER BY o.date_created;", [user_id])
            # rows = cursor.fetchall()
            services = dictfetchall(cursor)
        return JsonResponse({'products':products, 'services':services}, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'data':None, 'success':False})