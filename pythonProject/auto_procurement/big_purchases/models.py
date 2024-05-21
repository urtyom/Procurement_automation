from django.db import models
from django.contrib.auth.models import User


class Shop(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    shops = models.ManyToManyField(Shop, related_name='categories')

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_infos')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='product_infos')
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_rrc = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.shop.name}"


class Parameter(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, related_name='product_parameters')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name='product_parameters')
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.parameter.name}: {self.value}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    dt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


class Contact(models.Model):
    CONTACT_TYPES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    type = models.CharField(max_length=10, choices=CONTACT_TYPES)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type}: {self.value}"