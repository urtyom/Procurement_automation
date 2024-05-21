import yaml
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import FileSystemStorage
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


class UploadYAMLView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        shop_name = data['shop']
        shop, created = Shop.objects.get_or_create(name=shop_name)
        for category_data in data['categories']:
            category, created = Category.objects.get_or_create(id=category_data['id'],
                                                               defaults={'name': category_data['name']})
            shop.categories.add(category)

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
