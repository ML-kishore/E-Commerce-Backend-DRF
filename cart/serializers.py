from rest_framework import serializers
from .models import Cart,CartItem
from catalog.serializers import ProductSerializer



class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only = True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id','product','quantity','subtotal']

    def get_subtotal(self,obj):
        return obj.quantity * obj.product.price
    
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only = True)
    total_price = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id','user','items','total_price','created_at','updated_at']

    def get_total_price(self,obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())