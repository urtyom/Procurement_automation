import yaml
from models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


def load_goods_from_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

        shop_name = data.get('shop')
        shop, created = Shop.objects.get_or_create(name=shop_name)

        categories = data.get('categories', [])
        for category_data in categories:
            category_id = category_data.get('id')
            category_name = category_data.get('name')
            category, created = Category.objects.get_or_create(id=category_id, name=category_name)
            category.shops.add(shop)

        goods = data.get('goods', [])
        for good_data in goods:
            category_id = good_data.get('category')
            category = Category.objects.get(id=category_id)

            product, created = Product.objects.get_or_create(
                category=category,
                name=good_data.get('name')
            )

            product_info = ProductInfo.objects.create(
                product=product,
                shop=shop,
                name=good_data.get('model'),
                quantity=good_data.get('quantity'),
                price=good_data.get('price'),
                price_rrc=good_data.get('price_rrc')
            )

            parameters = good_data.get('parameters', {})
            for key, value in parameters.items():
                parameter, created = Parameter.objects.get_or_create(name=key)
                ProductParameter.objects.create(
                    product_info=product_info,
                    parameter=parameter,
                    value=value
                )
