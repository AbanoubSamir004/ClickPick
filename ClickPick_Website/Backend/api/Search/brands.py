from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Search
from collections import Counter

class UniqueBrandsSearchAPIView(APIView):
    def get(self, request, query=None):
        if query:
            query_search = Search.objects.filter(ProductTitle__icontains=query)
        else:
            query_search = Search.objects.all()

        brands = query_search.exclude(ProductBrand__in=['', ' ']).values_list('ProductBrand', flat=True)

        brand_counts = Counter(brands)
        sorted_brands = sorted(brand_counts, key=lambda x: brand_counts[x], reverse=True)

        return Response(sorted_brands)
