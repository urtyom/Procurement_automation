import yaml
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from big_purchases.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


@api_view(['GET'])
def demo(request):
    data = {'message': 'hello'}
    return Response(data)


class LoadGoodsAPIView(APIView):
    def post(self, request):

        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'File is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = yaml.safe_load(file)
        except yaml.YAMLError as e:
            return Response({'error': 'Error parsing YAML file'}, status=status.HTTP_400_BAD_REQUEST)

        shop_name = data.get('shop')
        shop, created = Shop.objects.get_or_create(name=shop_name)

        categories = data.get('categories', [])
        for category_data in categories:
            category_id = category_data.get('id')
            category_name = category_data.get('name')
            category, created = Category.objects.get_or_create(id=category_id, name=category_name, shop=shop)

        return Response({'message': 'File uploaded and processed successfully'}, status=status.HTTP_200_OK)