
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingPage, name='index'),
    path('base/',views.base, name='base'),
    path('shop/',views.shop, name='shop'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('graphics/', views.graphics, name="graphics"),
    path('get_sales/', views.get_sales, name="get_sales"),
    path('products/', views.products, name="products"),
    path('add_product/', views.add_product, name="add_product"),
    path('sales/', views.sales, name="sales"),
    path('products/', views.products, name="products"),
    path('sales/', views.sales, name="sales"),
    path('clients/', views.clients, name="clients"),
    path('config/', views.config, name="config"),
    path('buy/',views.buy, name="buy"),
    path('login/',views.login, name="login"),
]
