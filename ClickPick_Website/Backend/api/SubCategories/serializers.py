from rest_framework import serializers
from .models import SubCat
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 21
    page_size_query_param = 'page_size'
    max_page_size = 1000

class SubCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCat
        fields = '__all__'
        pagination_class = CustomPagination