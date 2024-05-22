from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, Contact


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    shop = ShopSerializer()

    class Meta:
        model = ProductInfo
        fields = '__all__'

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'

class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = ParameterSerializer()

    class Meta:
        model = ProductParameter
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product_info = ProductInfoSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
