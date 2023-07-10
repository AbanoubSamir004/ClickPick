from django.shortcuts import render
from django.http import Http404
from rest_framework.viewsets import ViewSet
from .models import Search
from .serializers import SearchSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class ProductPagination(PageNumberPagination):
    page_size = 21  # Change the page size to your desired value
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductViewSet(ViewSet):
    serializer_class = SearchSerializer
    pagination_class = ProductPagination

    def list(self, request):
        queryset = Search.objects.all()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        if pk is not None:
            try:
                product = Search.objects.get(ProductID=pk)
                serializer = self.serializer_class(product)
                return Response(serializer.data)
            except Search.DoesNotExist:
                raise Http404("Product ID not found")
        else:
            return Response("Product ID is required for retrieval.")

    def search(self, request, query):
        products = Search.objects.filter(ProductTitle__icontains=query)
        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = self.serializer_class(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)
