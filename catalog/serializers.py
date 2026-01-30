from rest_framework import serializers
from catalog.models import Categories,Products

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field = 'name',
        queryset = Categories.objects.all()
    )
    class Meta:
        model = Products
        fields = ['name','desc','slug','price','category','ratings','stock_left','is_active']
