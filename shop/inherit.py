import json
from . models import *

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() # gather all the items 
        cartItems = order.get_cart_items # how many items in the cart 
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    return {'cartItems':cartItems, 'items':items, 'order':order}