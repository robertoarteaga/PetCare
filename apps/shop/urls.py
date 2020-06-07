
from django.urls import path
from . import views


urlpatterns = [
    path('buy/<int:id_product>/', views.buy, name='buy'),
    path('buy_product/', views.buy_product, name='buy_product'),
    path('shop/',views.shop, name='shop'),
    path('services/',views.services, name='services'),
    path('customer_login/',views.customer_login, name="customer_login"),
    path('fake_customer_auth/',views.fake_customer_auth, name="fake_customer_auth"),
    path('contract_service/<int:id_service>/', views.contract_service, name='contract_service'),
    path('buy_service/', views.buy_service, name='buy_service'),
    path('cart/', views.cart, name='cart'),
    path('get_customer_cart/', views.get_customer_cart, name='get_customer_cart'),
]