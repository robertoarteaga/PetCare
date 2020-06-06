
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingPage, name='index'),
    path('base/',views.base, name='base'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('products_graphics/', views.products_graphics, name="products_graphics"),
    path('get_sales_products/', views.get_sales_products, name="get_sales_products"),
    path('servicess_graphics/', views.services_graphics, name="services_graphics"),
    path('get_sales_services/', views.get_sales_services, name="get_sales_services"),
    path('products/', views.products, name="products"),
    path('add_product/', views.add_product, name="add_product"),
    path('sales/', views.sales, name="sales"),
    path('products/', views.products, name="products"),
    path('sales/', views.sales, name="sales"),
    path('clients/', views.clients, name="clients"),
    path('config/', views.config, name="config"),
    path('update_customer/<int:pk>', views.UpdateCustomer.as_view(), name="update_customer"),
    path('get_monthly_sales_products/', views.get_monthly_sales_products, name="get_monthly_sales_products"),
    path('get_monthly_sales_services/', views.get_monthly_sales_services, name="get_monthly_sales_services"),
]
