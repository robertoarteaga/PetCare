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

def landingPage(request):
    """ Vista que renderiza el landing page """
    return render(request, 'core/index.html', {})


def base(request):
    """ Vista que muestra el html base par pruebas """
    return render(request, 'base/base.html', {})

def dashboard(request):
    return render(request, 'core/dashboard.html', {})


def graphics(request):
    best_selling = Product.products.annotate(total_orders=Count('orders')).order_by('-total_orders')
    context = {
        'is_popup':False, 
        'has_permission':True,
        'site_url':'/',
        'best_selling':best_selling,
        }
    return render(request, 'core/graphics.html', context)

def get_sales(request):
    """ Vista que regresa un json con las ventas del año """
    # sales = Order.objects.values('date_created').annotate(cantidad=Count('date_created'))
    # sales = Order.objects.values('date_created').annotate(cantidad=Count('date_created'))
    with connection.cursor() as cursor:
        cursor.execute("SELECT date_created, Count(*) as cantidad FROM accounts_order GROUP BY date_created;")
        rows = cursor.fetchall()
    return JsonResponse(rows, safe=False)
    # return HttpResponse(rows)

def products(request):
    products = Product.objects.all()
    return render(request, 'core/products.html',{'products':products})

def add_product(request):
	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('add_product')
		return render(request, 'core/add_product.html', {'form':form})
	form = ProductForm()
	return render(request, 'core/add_product.html', {'form':form})

def sales(request):
    sales = Order.objects.order_by('date_created')
    return render(request, 'core/sales.html',{'sales':sales})

def clients(request):
    Customer.objects.all()
    return render(request, 'core/clients.html',{})

def config(request):
    return render(request, 'core/config.html',{})
