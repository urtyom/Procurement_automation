from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()


class Category(models.Model):
    name = models.CharField(max_length=255)
    shops = models.ManyToManyField(Shop)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_rrc = models.DecimalField(max_digits=10, decimal_places=2)


class Parameter(models.Model):
    name = models.CharField(max_length=255)


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    dt = models.DateTimeField()
    status = models.CharField(max_length=50)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Contact(models.Model):
    type = models.CharField(max_length=50)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
