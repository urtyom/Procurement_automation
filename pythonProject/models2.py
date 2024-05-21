from django.db import models
from django.contrib.auth.models import User


class Shop(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return f'{self.name} {self.url}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} {self.shop}'


class Category(models.Model):
    name = models.CharField(max_length=100)
    shops = models.ManyToManyField(Shop, related_name='categories')

    def __str__(self):
        return f'{self.name} {self.shops}'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f'{self.category} {self.name} {self.shop}'


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_rrc = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product} {self.shop} {self.name} {self.quantity} {self.price} {self.price_rrc}'


class Parameter(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.product_info} {self.parameter} {self.value}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dt = models.DateTimeField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user} {self.dt} {self.status}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.order} {self.product} {self.shop} {self.quantity}'


class Contact(models.Model):
    type = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.type} {self.user} {self.value}'
