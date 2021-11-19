from typing import ItemsView
from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id)
            print('cart', cart )
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                print('Items', cart_item)
                cart_count += cart_item.quantity
                print('cart_count', cart_count)
        except Cart.DoesNotExist:
            cart_count = 0 
    return dict(cart_count=cart_count)  