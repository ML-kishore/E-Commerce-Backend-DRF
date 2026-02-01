from django.shortcuts import render
from users.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from catalog.permissions import IsAdminorReadOnly
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str


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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh = request.data.get("refresh")
        token = RefreshToken(refresh)

        token.blacklist()
        return Response({"message" : "User has been logged out"},status=205)
    except Exception as e:
        return Response({"error" : str(e)},status=205)
    
@api_view(['POST'])
@permission_classes([])
def password_reset_request(request):
    email = request.data.get('email')
    user = User.objects.get(email=email).first()
    if user:
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        return Response({"uidb64" : uidb64, "token" : token},status=200)
    else:
        return Response({"error" : "User not found ..."},status=404)

@api_view(['POST'])
@permission_classes([])
def password_reset(request):
    uidb64 = request.data.get('uidb64')
    token = request.data.get('token')
    new_password = request.data.get('password')
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user is None

    if user and default_token_generator.check_token(user,token):
        user.set_password(new_password)
        user.save()
        return Response({"message" : "Password Reset Successfully"},status=200)
    else:
        return Response({"error":"Invalid Token"},status=400)

