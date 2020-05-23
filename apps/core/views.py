from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import views as admin_views
from apps.accounts.models import Product
from apps.accounts.forms import *
def landingPage(request):

    return render(request, 'core/index.html', {})


def base(request):

    return render(request, 'base/base.html', {})

def shop(request):
    products = Product.objects.all()
    return render(request, 'core/shop.html', {'products':products})

def dashboard(request):
    return render(request, 'core/dashboard.html', {})


def graphics(request):
    return render(request, 'core/graphics.html', {})


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
    return render(request, 'core/sales.html',{})

def clients(request):
    return render(request, 'core/clients.html',{})

def config(request):
    return render(request, 'core/config.html',{})
