
from django.urls import path
from . import views


urlpatterns = [
    path('buy_product/', views.buy_product, name='buy_product'),
]