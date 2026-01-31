from django.shortcuts import render
from cart.models import Cart,CartItem
from catalog.models import Categories,Products
from .models import Orders,OrderItem
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from catalog.permissions import IsAdminorReadOnly
from django.db import transaction
from rest_framework.response import Response
from .serializers import OrderSerializer,OrderItemSerializer
# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
        
    except Cart.DoesNotExist:
        return Response({"error" : "Cart Does Not Exist...."},status=404)
    cart_items = cart.items.select_related('product')

    if not cart_items.exists():
        return Response({"message" : "Cart has no items..."},status=404)
    with transaction.atomic():
        order = Orders.objects.create(user=user,amount=0)
        total = 0
        for item in cart_items:
            if item.product.stock_left < item.quantity:
                return Response({"message" : f"Insufficient Stock... {item.product} has only {item.product.stock_left} left...."},status=200)
            
        for item in cart_items:
            order_item = OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity,price_at_purchase=item.product.price)

            total += order_item.subtotal

            #reduce stock
            item.product.stock_left -= item.quantity
            item.product.save()

        order.amount = total
        order.save()

        cart_items.delete()


    return Response({"message" : "Order placed successfully..."},status=201)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def cancel_order(request,order_id):
    user = request.user
    try:

        order = Orders.objects.get(user=user,id=order_id,is_cancelled=False)
    except Orders.DoesNotExist:
        return Response({"error" : "Order Does Not Ecsit..."},status=404)
    
    if order.is_cancelled == True:
        return Response({"error" : "Order is Already Cancelled.."},status=409)
    

    order_items = OrderItem.objects.select_related('product').filter(order=order)
    
    #order status checking
    if order.order_status == 'DELIVERED':
        return Response({"error" : "You scammer...."},status=403)

    with transaction.atomic():
        for item in order_items:
            product = item.product

            product.stock_left += item.quantity
            product.save()

        #cancelling order
        order.is_cancelled = True
        order.save()

    return Response({"message" : "Order Cancelled..."},status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Orders.objects.filter(user=request.user).select_related('user')
    serializer = OrderSerializer(orders,many=True)
    return Response(serializer.data,status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_one_order(request,order_id):
    try:
        order = Orders.objects.select_related('user').prefetch_related('orderitem__product').filter(id=order_id,user=request.user)
    except Orders.DoesNotExist:
        return Response({"error" : "Order Does Not Exist..."},status=404)
    
    serializer = OrderSerializer(order)
    return Response(serializer.data,status=200)


@api_view(['PATCH'])
@permission_classes([IsAdminorReadOnly,IsAuthenticated])
def update_status(request,order_id):
    try:
        order = Orders.objects.get(user=request.user,id=order_id)
    except Orders.DoesNotExist:
        return Response({"error" : "Order Does Not Exist..."},status=404)
    
    current_status = order.order_status.upper()
    new_status = request.data.get('order_status')
    next_status = new_status.upper()
    print(next_status)
    
    if order.is_cancelled:
        return Response({"Message" : "Cant change status when order is cancelled...."},status=400)
    
    if order.order_status == 'delivered' or 'DELIVERED':
        return Response({"message" : "The Order has been delivered.."},status=400)
    
    allowed_flow = {
        'ORDER_PLACED' : 'SHIPPED',
        'SHIPPED' : 'OUT_FOR_DELIVERY',
        'OUT_FOR_DELIVERY' : 'DELIVERED'
    }

    if allowed_flow[current_status] != new_status:
        print(allowed_flow)
        print(allowed_flow.get(order.order_status) , new_status)
        return Response({"message" : "Invalid Status Transition allowed...."},status=404)
    
    print(allowed_flow.get(order.order_status) , new_status) 
    order.order_status = new_status.lower()
    order.save()

    return Response({"message" : "Status Updated...."},status=200)