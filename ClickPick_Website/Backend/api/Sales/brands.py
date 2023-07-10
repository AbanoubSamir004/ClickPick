from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Sales
from django.db.models import Count



class UniqueBrandsAPIView(APIView):
    def get(self, request):
        unique_brands = (
            Sales.objects
            .exclude(ProductBrand__exact='')
            .values('ProductBrand')
            .annotate(count=Count('ProductBrand'))
            .order_by('-count', 'ProductBrand')
        )
        brand_list = [item['ProductBrand'] for item in unique_brands]
        return Response(brand_list)
