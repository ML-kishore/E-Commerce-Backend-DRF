from rest_framework import serializers
from users.models import User
from django.contrib.auth.password_validation import validate_password 


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(write_only=True,validators=[validate_password],required=True)

    class Meta:
        model = User
        fields = ['username','email','password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user
    
