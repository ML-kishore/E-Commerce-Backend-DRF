from django.shortcuts import render
from .serializers import CartItemSerializer,CartSerializer
from .models import CartItem,Cart
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from catalog.permissions import IsAdminorReadOnly
from rest_framework.response import Response
from django.db import transaction
from catalog.models import Products,Categories
from users.models import User

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return Response(
            {"message": "Cart is empty"},
            status=200
        )
    serializer = CartSerializer(cart)
    return Response(serializer.data,status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user = request.user
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')

    if not product_id:
        return Response({"message": "Product Id required"}, status=400)

    try:
        product = Products.objects.get(id=product_id)
    except Products.DoesNotExist:
        return Response({"message": "Product does not exist"}, status=404)

    if quantity <= 0:
        return Response({"message": "Quantity must be >= 1"}, status=400)

    with transaction.atomic():
        cart, _ = Cart.objects.get_or_create(user=user)

        cart_item, new = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if new:
            new_quantity = quantity
        else:
            new_quantity = cart_item.quantity + quantity

        # stock validation
        if product.stock_left < new_quantity:
            return Response({"message": "Stocks unavailable"}, status=400)

        cart_item.quantity = new_quantity
        cart_item.save()

    return Response({"message": "Product added successfully"}, status=200)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_cart(request,product_id):
    user = request.user
    quantity = request.data.get('quantity')

    if quantity is None:
        return Response({"error" : "Quantity not Provided"},status=400)

    quantity = int(quantity)

    if quantity < 0:
        return Response({"error" : "Quantity should be greater than 0"},status=404)

    try:
        product = Products.objects.get(id=product_id)
    except Products.DoesNotExist:
        return Response({"error" : "Product Does Not Exist..."},status=400)

    cart = Cart.objects.get(user=user)

    cartitem = CartItem.objects.get(cart=cart,product=product)

    with transaction.atomic():
        if quantity == 0:
            cartitem.delete()
            return Response({"message" : "Product removed from cart..."})
        
        if product.stock_left < quantity:
            return Response({"message" : "Stock Not availables"},status=400)
        
        cartitem.quantity = quantity
        cartitem.save()

        return Response({"message" : "Cart Item Quantity has been saved...."},status=200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request,product_id):
    user = request.user
    try:
        product = Products.objects.get(id=product_id)
    except Products.DoesNotExist:
        return Response({"error" : "Product not Exist...."})
    cart = Cart.objects.get(user=user)
    cart_item = CartItem.objects.filter(cart=cart,product=product)
    if request.method == 'DELETE':
        cart_item.delete()
        return Response({"message" : "Item Removed From Cart...."},status=200)
    return Response({"error" : "Bad Request..."},status=400)



