from django.db import models
from django.urls import reverse
# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def orders(self):
        order_count = self.order_set.all().count()
        return str(order_count)

    def get_absolute_url(self):
        return reverse('customer-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Pet(models.Model):
    ANIMAL_CHOICES = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Ave', 'Ave'),
        ('Otro', 'Otro'),
    ]
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    age = models.IntegerField()
    type_animal = models.CharField(
        max_length=15, choices=ANIMAL_CHOICES, default='Perro')
    desc = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"

class ServicesManager(models.Manager):
    """ Just get the products in the category of Services """
    def get_queryset(self):
        return super().get_queryset().filter(category="Servicio")

class ProductsManager(models.Manager):
    """ Get all the products excluding the services """
    def get_queryset(self):
        return super().get_queryset().exclude(category="Servicio")


class Product(models.Model):

    CATEGORY = (
        ('Servicio', 'Servicio'),
        ('Comida', 'Comida'),
        ('Accesorio', 'Accesorio'),
        ('Limpieza', 'Limpieza'),
    )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.TextField()
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    img_product = models.ImageField(
        upload_to='productos',  null=True, blank=True)
    
    objects = models.Manager()
    services = ServicesManager()
    products = ProductsManager()

    @property
    def orders(self):
        order_count = self.order_set.all().count()
        return str(order_count)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name = 'get_orders')
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return str(self.product)
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

