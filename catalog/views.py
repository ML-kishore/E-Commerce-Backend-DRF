from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminorReadOnly
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from catalog.models import Categories,Products
from .serializers import ProductSerializer,CategorySerializer
from django.db.models import Q

# Create your views here.
search_parameters = ['category__name', 'name' , 'desc']

def search_queryset(queryset,param):

    if not param:
        return queryset

    q = Q()

    for field in search_parameters:
        q  |= Q(**{f"{field}__icontains": param})
        
    return queryset.filter(q) 


@api_view(['POST'])
@permission_classes([IsAdminorReadOnly,IsAuthenticated])
def create_categories(request):
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "New Category added by Admin"},status=201)
    return Response({"error": serializer.errors},status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_categories(request):
    categories = Categories.objects.all()
    if request.method == 'GET':
        serializer = CategorySerializer(categories,many=True)
        return Response(serializer.data,status=200)
    return Response({"error": serializer.errors},status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_products(request):
    products = Products.objects.filter(is_deleted=False)

    #tommorow features function for serach queries and ratings filter..... (25/01/2026)

    search = request.GET.get('search')

    queryset = search_queryset(products,search)

    ordering = request.query_params.get('ordering')
    orders = ['price','-price','ratings','-ratings','categories__name',"name"]

    if ordering:
        if ordering not in orders:
            return Response({"error" : "Give valid order parameter"},status=404)
        else:
            queryset = queryset.order_by(ordering)
        
    serializer = ProductSerializer(queryset,many=True)
    return Response(serializer.data,status=200)

@api_view(['PUT','PATCH','DELETE','GET'])
@permission_classes([IsAdminorReadOnly,IsAuthenticated])
def view_product(request,prod_id):
    try:
        product = Products.objects.get(id=prod_id,is_deleted = False)
    except Products.DoesNotExist:
        return Response({"error":"Product does not exist"},status=404)
    
    #GET
    if request.method == 'GET':
        product = ProductSerializer(product)
        return Response(product.data,status=200)
    
    #PUT 
    elif request.method in ['PUT','PATCH']:
        serializer = ProductSerializer(instance=product,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":f"Product no {prod_id} has updated successfully by admin..."},status=200)
        return Response({"error" : serializer.errors },status=400)
    
    #DELETE
    elif request.method == 'DELETE':
        product.is_deleted = True
        product.save()
        return Response({"message" : f"Product no {prod_id} has deleted successfully by admin"},status=200)
    
    else:
        return Response({"error":"Method not Valid"},status=500)
    
@api_view(['POST'])
@permission_classes([IsAdminorReadOnly,IsAuthenticated])
def add_products(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "New Product added"},status=201)
    return Response({"error" : serializer.error_messages},status=400)