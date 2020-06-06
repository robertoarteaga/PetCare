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
from django.db.models.functions import Cast
from django.views.generic.edit import UpdateView

import datetime

from django.db.models import F, Q, When


def landingPage(request):
    """ Vista que renderiza el landing page """
    return render(request, 'core/index.html', {})


def base(request):
    """ Vista que muestra el html base par pruebas """
    return render(request, 'base/base.html', {})


def dashboard(request):
    return render(request, 'core/dashboard.html', {})


def products_graphics(request):
    # best_selling = Product.products.annotate(total_orders=Count('get_orders'), total_mxn='total_orders'*price).order_by('-total_orders')
    best_selling = Product.products.annotate(
        total_orders=Count('get_orders'),
        total_mxn=Cast(
            Count('get_orders')*F('price'),
            FloatField())
    ).order_by('-total_orders')[0:7]
    worst_selling = Product.products.annotate(
        total_orders=Count('get_orders'),
        total_mxn=Cast(
            Count('get_orders')*F('price'),
            FloatField())
    ).order_by('total_orders')[0:4]
    # SELECT SUM(p.price)
    # FROM accounts_product p, accounts_order o
    # WHERE p.id = o.product_id
    # AND o.date_created > '2020-06-01';
    a_date = datetime.datetime.today()
    week_number = a_date.isocalendar()[1]
    week_close = Order.objects.filter(date_created__week=week_number).exclude(
        product_id__category='Servicio').aggregate(week_close=Sum('product_id__price'))
    print(week_close)
    month_number = a_date.month
    month_close = Order.objects.filter(date_created__month=month_number).exclude(
        product_id__category='Servicio').aggregate(month_close=Sum('product_id__price'))
    print(month_close)
    year_close = Order.objects.exclude(product_id__category='Servicio').aggregate(
        year_close=Sum('product_id__price'))
    january_close = Order.objects.filter(date_created__month=1).exclude(product_id__category='Servicio').aggregate(
        year_close=Sum('product_id__price'))
    february_close = Order.objects.filter(date_created__month=2).exclude(product_id__category='Servicio').aggregate(
        year_close=Sum('product_id__price'))
    march_close = Order.objects.filter(date_created__month=3).exclude(product_id__category='Servicio').aggregate(
        year_close=Sum('product_id__price'))
    april_close = Order.objects.filter(date_created__month=4).exclude(product_id__category='Servicio').aggregate(
        year_close=Sum('product_id__price'))
    may_close = Order.objects.filter(date_created__month=5).exclude(product_id__category='Servicio').aggregate(
        year_close=Sum('product_id__price'))
    june_close = Order.objects.filter(date_created__month=6).exclude(product_id__category='Servicio').aggregate(
        year_close=Sum('product_id__price'))
    context = {
        'is_popup': False,
        'has_permission': True,
        'site_url': '/',
        'best_selling': best_selling,
        'worst_selling': worst_selling,
        'week_close': week_close,
        'month_close': month_close,
        'year_close': year_close,
        'january_close':january_close,
        'february_close':february_close,
        'march_close':march_close,
        'april_close':april_close,
        'may_close':may_close,
        'june_close':june_close
    }
    return render(request, 'core/products_graphics.html', context)


def get_sales_products(request):
    """ Vista que regresa un json con las ventas del año """
    # sales = Order.objects.values('date_created').annotate(cantidad=Count('date_created'))
    # sales = Order.objects.values('date_created').annotate(cantidad=Count('date_created'))
    with connection.cursor() as cursor:
        cursor.execute("""SELECT o.date_created, Count(*) as cantidad 
                        FROM accounts_order o, accounts_product p
                        WHERE o.product_id = p.id AND p.category <> 'Servicio'
                        GROUP BY o.date_created;""")
        rows = cursor.fetchall()
    return JsonResponse(rows, safe=False)


def get_monthly_sales_products(request):
    " returns ventas por meses de cada producto"
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT p.name || p.description as 'name',
                count(case when o.date_created >= '2020-01-01 00:00:00' AND o.date_created < '2020-02-01 00:00:00' then 1 end)as Enero,
                count(case when o.date_created >= '2020-02-01 00:00:00' AND o.date_created < '2020-03-01 00:00:00' then 1 end)as Febrero,
                count(case when o.date_created >= '2020-03-01 00:00:00' AND o.date_created < '2020-04-01 00:00:00' then 1 end)as Marzo,
                count(case when o.date_created >= '2020-04-01 00:00:00' AND o.date_created < '2020-05-01 00:00:00' then 1 end)as Abril,
                count(case when o.date_created >= '2020-05-01 00:00:00' AND o.date_created < '2020-06-01 00:00:00' then 1 end)as Mayo,
                count(case when o.date_created >= '2020-06-01 00:00:00' AND o.date_created < '2020-07-01 00:00:00' then 1 end)as Junio
                
            FROM accounts_order o, accounts_product p
            WHERE o.product_id = p.id
            AND p.category <> 'Servicio'
            GROUP BY o.product_id;
            """)
            rows = cursor.fetchall()
    
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'data':None}, safe=False)


def services_graphics(request):
    # best_selling = Product.products.annotate(total_orders=Count('get_orders'), total_mxn='total_orders'*price).order_by('-total_orders')
    best_selling = Product.services.annotate(
        total_orders=Count('get_orders'),
        total_mxn=Cast(
            Count('get_orders')*F('price'),
            FloatField())
    ).order_by('-total_orders')
    january_close = Order.objects.filter(date_created__month=1, product_id__category='Servicio').aggregate(
        year_close=Sum('product_id__price'))
    february_close = Order.objects.filter(date_created__month=2, product_id__category='Servicio').aggregate(
        year_close=Sum('product_id__price'))
    march_close = Order.objects.filter(date_created__month=3, product_id__category='Servicio').aggregate(
        year_close=Sum('product_id__price'))
    april_close = Order.objects.filter(date_created__month=4, product_id__category='Servicio').aggregate(
        year_close=Sum('product_id__price'))
    may_close = Order.objects.filter(date_created__month=5, product_id__category='Servicio').aggregate(
        year_close=Sum('product_id__price'))
    june_close = Order.objects.filter(date_created__month=6, product_id__category='Servicio').aggregate(
        year_close=Sum('product_id__price'))
    # SELECT SUM(p.price)
    # FROM accounts_product p, accounts_order o
    # WHERE p.id = o.product_id
    # AND o.date_created > '2020-06-01';
    a_date = datetime.datetime.today()
    week_number = a_date.isocalendar()[1]
    week_close = Order.objects.filter(date_created__week=week_number, product_id__category='Servicio').aggregate(week_close=Sum('product_id__price'))
    print(week_close)
    month_number = a_date.month
    month_close = Order.objects.filter(date_created__month=month_number, product_id__category='Servicio').aggregate(month_close=Sum('product_id__price'))
    print(month_close)
    year_close = Order.objects.filter(product_id__category='Servicio').aggregate(
        year_close=Sum('product_id__price'))
    context = {
        'is_popup': False,
        'has_permission': True,
        'site_url': '/',
        'best_selling': best_selling,
        'week_close': week_close,
        'month_close': month_close,
        'year_close': year_close,
        'january_close':january_close,
        'february_close':february_close,
        'march_close':march_close,
        'april_close':april_close,
        'may_close':may_close,
        'june_close':june_close
    }
    return render(request, 'core/services_graphics.html', context)

    # best_selling = Product.services.annotate(total_orders=Count('get_orders')).order_by('-total_orders')
    # best_selling = Product.services.annotate(
    #     total_orders=Count('get_orders'),
    #     total_mxn=Cast(
    #         Count('get_orders')*F('price'),
    #         FloatField())
    # ).order_by('-total_orders')
    # context = {
    #     'is_popup': False,
    #     'has_permission': True,
    #     'site_url': '/',
    #     'best_selling': best_selling,
    # }
    
def get_monthly_sales_services(request):
    " returns ventas por meses de cada producto"
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT p.name,
                count(case when o.date_created >= '2020-01-01 00:00:00' AND o.date_created < '2020-02-01 00:00:00' then 1 end)as Enero,
                count(case when o.date_created >= '2020-02-01 00:00:00' AND o.date_created < '2020-03-01 00:00:00' then 1 end)as Febrero,
                count(case when o.date_created >= '2020-03-01 00:00:00' AND o.date_created < '2020-04-01 00:00:00' then 1 end)as Marzo,
                count(case when o.date_created >= '2020-04-01 00:00:00' AND o.date_created < '2020-05-01 00:00:00' then 1 end)as Abril,
                count(case when o.date_created >= '2020-05-01 00:00:00' AND o.date_created < '2020-06-01 00:00:00' then 1 end)as Mayo,
                count(case when o.date_created >= '2020-06-01 00:00:00' AND o.date_created < '2020-07-01 00:00:00' then 1 end)as Junio
                
            FROM accounts_order o, accounts_product p
            WHERE o.product_id = p.id
            AND p.category == 'Servicio'
            GROUP BY o.product_id;
            """)
            rows = cursor.fetchall()
    
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'data':None}, safe=False)

def get_sales_services(request):
    """ Vista que regresa un json con las ventas del año """
    # sales = Order.objects.values('date_created').annotate(cantidad=Count('date_created'))
    # sales = Order.objects.values('date_created').annotate(cantidad=Count('date_created'))
    with connection.cursor() as cursor:
        cursor.execute("""SELECT o.date_created, Count(*) as cantidad 
                        FROM accounts_order o, accounts_product p
                        WHERE o.product_id = p.id AND p.category = 'Servicio'
                        GROUP BY o.date_created;""")
        rows = cursor.fetchall()
    return JsonResponse(rows, safe=False)


def products(request):
    products = Product.objects.all()
    return render(request, 'core/products.html', {'products': products})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_product')
        return render(request, 'core/add_product.html', {'form': form})
    form = ProductForm()
    return render(request, 'core/add_product.html', {'form': form})


def sales(request):
    sales = Order.objects.order_by('date_created')
    return render(request, 'core/sales.html', {'sales': sales})


def clients(request):
    Customer.objects.all()
    return render(request, 'core/clients.html', {})


def config(request):
    return render(request, 'core/config.html', {})


class UpdateCustomer(UpdateView):
    model = Customer
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = None
