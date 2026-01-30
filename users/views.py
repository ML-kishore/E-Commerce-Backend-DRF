from django.shortcuts import render
from users.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from catalog.permissions import IsAdminorReadOnly
from .serializers import UserSerializer


# Create your views here.
@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "User has been Created Successfully....."},status=201)
        return Response({"error" : serializer.errors}, status=400)
    

@api_view(['PUT','PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user_data = User.objects.get(user=request.user)
    if request.method in ['PUT','PATCH']:
        serializer = UserSerializer(instance=user_data,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "User Details has been Updated...."},status=200)
    return Response({"errors" : serializer.errors},status=400)
        

@api_view(['DELETE'])
@permission_classes([IsAdminorReadOnly, IsAuthenticated])
def soft_delete_user(request,user_id):
    try:
        user_data = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error" : "User Not Found"},status=404)
    if request.method == 'DELETE':
        user_data.is_deleted = True
        user_data.save()
        return Response({"message" : "User has been Deleted ....."},status=200)
    return Response({"errors" : "Bad Request"},status=400)


@api_view(['GET'])
@permission_classes([IsAdminorReadOnly, IsAuthenticated])
def view_users(request):
    users = User.objects.all()
    if request.method == 'GET':
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data, status=200)
    return Response(serializer.errors,status=400)

