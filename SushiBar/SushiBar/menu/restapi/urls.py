from django.urls import path
from .views import get_products,product_detail,get_product_detail,get_orders,get_order_detail,user_cart_view,user_cart_product_item_view,get_product_detail_id
app_name = "menu"

urlpatterns = [
    path('', get_products, name = 'get_products'),
    path('product/', get_product_detail_id, name = 'get_products'),
    path('orders/',get_orders, name = 'get_orders'),
    path('cart/',user_cart_view, name = 'user_cart_view'),
    path('cartproduct/',user_cart_product_item_view, name = 'user_cart_view'),
    path('orders/<int:id>/',get_order_detail, name = 'get_order'),
    # path('create/', create_product, name = 'create_product'),
    path('edit/<slug:slug>/', product_detail, name = 'edit_product_detail'),
    path('<slug:slug>/', get_product_detail, name = 'get_product_detail'),

    
]
