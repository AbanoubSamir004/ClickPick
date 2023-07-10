from django.shortcuts import render
from django.http import Http404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import SubCat
from .serializers import SubCatSerializer, SubCatSerializer
from rest_framework.pagination import PageNumberPagination

class SubCatPagination(PageNumberPagination):
    page_size = 21  # Change the page size to your desired value
    page_size_query_param = 'page_size'
    max_page_size = 100

class SubCatViewSet(ViewSet):
    serializer_class = SubCatSerializer
    pagination_class = SubCatPagination

    def list(self, request, subcategory):
        subcat = SubCat.objects.filter(ProductSubCategory=subcategory)
        paginator = self.pagination_class()
        paginated_subcat = paginator.paginate_queryset(subcat, request)
        serializer = SubCatSerializer(paginated_subcat, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        if pk is not None:
            try:
                subcat = SubCat.objects.get(ProductID=pk)
                serializer = SubCatSerializer(subcat)
                return Response(serializer.data)
            except SubCat.DoesNotExist:
                raise Http404("subcategory ID not found")
        else:
            return self.list(request)
