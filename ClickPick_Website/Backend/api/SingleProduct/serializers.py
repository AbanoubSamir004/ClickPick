from .models import Product
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = ("ProductID", "ProductTitle")
        fields = '__all__'

