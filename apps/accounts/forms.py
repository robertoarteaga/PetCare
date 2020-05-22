from django.forms import ModelForm
from .models import Customer, Order, Product

class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'

class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = '__all__'