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
from django.db.models import Q,Sum,F

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


possible_queries = ['items__product__name',"items__product__category__name"]
#later with ratings possible_queireies
def search_query(queryset,param):
    if not param:
        return queryset
    print(param, "hihello")
    print("just checking from serach")
    q = Q()

    for field in possible_queries:
        q = q | Q(**{f"{field}__icontains" : param})
    
    return queryset.filter(q)

filter_params = {
    "name" : "items__product__name",
    "category" : "items__product__category__name",
    "search" : "items__product__name"
    
}

def apply_filters(queryset,params):

    filters = {}
    if not params:
        return queryset
    
    for param,field in filter_params.items():
        value = params.get(param)
        print(value)
        if value is None:
            continue
        if field == "items__product__name":
            filters[f"{field}__icontains"] = value
        else:
            filters[field] = value
    return queryset.filter(**filters)            

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_item_in_cart(request):
    cart_qs = Cart.objects.filter(user=request.user)
    if not cart_qs.exists():
        return Response({"error" : "Cart Does not exist"},status=404)
    
    search = request.query_params.get('search')
    #search_norm = search.lower().rstrip('s')
    zx = Categories.objects.values_list('name').filter(name='Mobiles').first()
    #print(zx ,len(zx))
    #print(search, "hi hellowdaw", len(search))
    params = request.query_params
    print(params, "this is params daw....")

    if search:
        cart_items = CartItem.objects.filter(cart__user = request.user).filter(Q(product__name__icontains = search) | 
                                Q(product__category__slug__iexact=search))
        print(
    CartItem.objects.filter(
        product__category__name__icontains='Mobile'
    ).query
)

        
        cart_ids = cart_items.values_list('cart_id',flat=True)
        queryset = cart_qs.filter(id__in = cart_ids)
    else:
        queryset = cart_qs

    queryset = apply_filters(queryset,params)

    serializer = CartSerializer(queryset,many=True)
    return Response(serializer.data,status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_summary(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    if not cart:
        return Response({"total_cart_item_count" : 0,"grand_total" : 0},status=200)
    summary_items = cart.items.aggregate(total_items_count=Sum('quantity'), grand_total=Sum(F('quantity') * F('product__price')))
    response_dict = {"total_items_count" : summary_items['total_items_count'] or 0, "grand_total" : summary_items['grand_total'] or 0}
    return Response(response_dict,status=200)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    user = request.user
    cart=Cart.objects.get(user=user)
    if not cart:
        return Response({"message":"cart does not exist"},status=200)
    cart.delete()
    return Response({"message" : "Cart has cleared....."},status=200)
    




    





