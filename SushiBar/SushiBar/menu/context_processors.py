from .models import Cart,Cart_item

def user_cart(request):
    items_count = 0
    if request.user.is_authenticated:
        user = request.user
        try:
            user_cart = Cart.objects.get(user=user)
            user_items = Cart_item.objects.filter(cart=user_cart)
            for item in user_items:
                items_count += item.quantity
            if len(user_items) == 0:
                user_items = None
                return {'user_cart': user_cart,
                        'user_items': user_items,
                        'items_count': items_count,
                        'cart_status_msg': 'no_items'}
            return {'user_cart': user_cart,
            'user_items': user_items,
            'items_count': items_count,
            'cart_status_msg': 'fine'}
        except:
            return {'user_cart': 'Brak koszyka. Skontaktuj się z administratorem.',
                        'items_count': items_count,
            'cart_status_msg': 'no_cart'}
    else:
        return {'user_cart': 'To nigdy nie powinno sie wyswietlic (niezarejstrowany nie ma dostepu do koszyka)',
                        'items_count': items_count,
        'cart_status_msg': 'wtf'}