
from django.urls import path
from . import views


urlpatterns = [
    path('buy/<int:id_product>/', views.buy, name='buy'),
    path('buy_product/', views.buy_product, name='buy_product'),
    path('shop/',views.shop, name='shop'),
    path('services/',views.services, name='services'),
    path('customer_login/',views.customer_login, name="customer_login"),
    path('fake_customer_auth/',views.fake_customer_auth, name="fake_customer_auth"),
]