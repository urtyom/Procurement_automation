import yaml
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, views
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, Contact
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, ShopSerializer, CategorySerializer, ProductSerializer, ProductInfoSerializer, OrderSerializer, OrderItemSerializer, ContactSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class UploadYAMLView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = yaml.safe_load(file.read())
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем или создаем магазин
        shop_name = data['shop']
        shop, created = Shop.objects.get_or_create(name=shop_name)

        # Добавляем категории
        for category_data in data['categories']:
            category, created = Category.objects.get_or_create(id=category_data['id'],
                                                               defaults={'name': category_data['name']})
            shop.categories.add(category)

        # Добавляем товары и их параметры
        for product_data in data['goods']:
            category = Category.objects.get(id=product_data['category'])
            product, created = Product.objects.get_or_create(id=product_data['id'], category=category,
                                                             defaults={'name': product_data['name']})

            product_info, created = ProductInfo.objects.get_or_create(
                product=product,
                shop=shop,
                defaults={
                    'name': product_data['name'],
                    'quantity': product_data['quantity'],
                    'price': product_data['price'],
                    'price_rrc': product_data['price_rrc']
                }
            )

            for param_name, param_value in product_data['parameters'].items():
                parameter, created = Parameter.objects.get_or_create(name=param_name)
                ProductParameter.objects.create(product_info=product_info, parameter=parameter, value=param_value)

        return Response({"message": "Data uploaded successfully"}, status=status.HTTP_201_CREATED)


# Регистрация пользователя
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Вход пользователя
class LoginView(TokenObtainPairView):
    serializer_class = UserSerializer


# Список товаров с фильтрацией и поиском
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category')
        name = self.request.query_params.get('name')
        if category:
            queryset = queryset.filter(category__name=category)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


# Корзина пользователя
class CartView(generics.ListCreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        order, created = Order.objects.get_or_create(user=user, status='cart')
        return OrderItem.objects.filter(order=order)


    def post(self, request, *args, **kwargs):
        user = self.request.user
        order, created = Order.objects.get_or_create(user=user, status='cart')
        product_info_id = request.data.get('product_info')
        quantity = request.data.get('quantity')

        product_info = get_object_or_404(ProductInfo, id=product_info_id)

        order_item, created = OrderItem.objects.get_or_create(order=order, product_info=product_info, defaults={'quantity': quantity})
        if not created:
            order_item.quantity += int(quantity)
            order_item.save()

        return Response(OrderItemSerializer(order_item).data, status=status.HTTP_201_CREATED)


# Удаление товара из корзины
class CartItemDeleteView(generics.DestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        order, created = Order.objects.get_or_create(user=user, status='cart')
        return OrderItem.objects.filter(order=order)


# Добавление контакта
class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Подтверждение заказа
class ConfirmOrderView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_id = request.data.get('cart_id')
        contact_id = request.data.get('contact_id')

        order = get_object_or_404(Order, id=cart_id, user=user, status='cart')
        contact = get_object_or_404(Contact, id=contact_id, user=user)

        order.status = 'confirmed'
        order.save()

        return Response({"message": "Order confirmed"}, status=status.HTTP_200_OK)


# Статус и история заказов
class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user).exclude(status='cart')