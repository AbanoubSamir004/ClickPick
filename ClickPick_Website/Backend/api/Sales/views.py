from django.http import Http404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import Sales
from .serializers import SalesSerializer
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from rest_framework.permissions import AllowAny



class SalesPagination(PageNumberPagination):
    page_size = 21  # Change the page size to your desired value
    page_size_query_param = 'page_size'
    max_page_size = 100

class SalesViewSet(ViewSet):
    serializer_class = SalesSerializer
    pagination_class = SalesPagination

    def list(self, request):
        sales = Sales.objects.all()
        paginator = self.pagination_class()
        paginated_sales = paginator.paginate_queryset(sales, request)
        serializer = SalesSerializer(paginated_sales, many=True)
        return paginator.get_paginated_response(serializer.data)
        

    def retrieve(self, request, pk=None):
        if pk is not None:
            try:
                sales = Sales.objects.get(ProductID=pk)
                serializer = SalesSerializer(sales)
                return Response(serializer.data)
            except Sales.DoesNotExist:
                raise Http404("Sales ID not found")
        else:
            return self.list(request)


class FilteredSalesViewSet(ViewSet):
    serializer_class = SalesSerializer
    pagination_class = SalesPagination

    def list(self, request, *args, **kwargs):
        queryset = Sales.objects.all()

        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        brand = request.query_params.get('brand')
        marketplace = request.query_params.get('marketplace')

        # Apply filters
        if min_price:
            min_price_float = float(min_price)
            queryset = queryset.filter(ProductPrice__gte=min_price_float)
        if max_price:
            max_price_float = float(max_price)
            queryset = queryset.filter(ProductPrice__lte=max_price_float)
        if brand:
            queryset = queryset.filter(ProductBrand__iexact=brand)
        if marketplace:
            queryset = queryset.filter(Marketplace__iexact=marketplace)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = SalesSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        if pk is not None:
            try:
                sales = Sales.objects.get(ProductID=pk)
                serializer = SalesSerializer(sales)
                return Response(serializer.data)
            except Sales.DoesNotExist:
                raise Http404("Sales ID not found")
        else:
            return self.list(request)
