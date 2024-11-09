from rest_framework import serializers
from menu.models import Product, Category, Cart, Cart_item, Ingredient, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class GetProductsSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True, many=True)
    ingredients = IngredientSerializer(read_only=True, many=True)
    class Meta:
        model = Product
        fields = ['id', 'name','description','price','promotion_price','is_promoted','status','kcal','slug','image','categories','ingredients']
    
class GetOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product_name','created','quantity','price']

class GetOrderSerializer(serializers.ModelSerializer):

    order_items = GetOrderItemSerializer(read_only= True, many = True)
    
    class Meta:
        model = Order
        fields = ['id','user','status','total_price','created','payment','payment_status','user_first_last_name','comments','phone_number',
        'city','house_number','flat_number','street','postal_code','sessionId','orderId', 'order_items']

class GetUserCartItemSerializer(serializers.ModelSerializer):

    product = GetProductsSerializer()

    class Meta:
        model = Cart_item
        fields = '__all__'

class GetUserCartSerializer(serializers.ModelSerializer):

    cart_items = GetUserCartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'


# class CreateProductSerializer(serializers.ModelSerializer):
#     categories = CategorySerializer(many=True)
#     class Meta:
#         model = Product
#         fields = ['name','description','price','status','kcal','categories'] 
    
#     # def save(self):
#     #     print("elo")
#     #     categories = self.validated_data.pop('categories')
#     #     product = Product.objects.create(**self.validated_data)
#     #     print(self.validated_data)

#     #     # for cat in categories:
#     #     #     product.categories.add(cat)
#     #     product.save()




