from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SubCat
from collections import Counter

class UniqueBrandsAPIView(APIView):
    def get(self, request, subcategory=None):
        if subcategory:
            subcat = SubCat.objects.filter(ProductSubCategory=subcategory)
        else:
            subcat = SubCat.objects.all()

        brands = subcat.exclude(ProductBrand__in=['', ' ']).values_list('ProductBrand', flat=True)

        brand_counts = Counter(brands)
        sorted_brands = sorted(brand_counts, key=lambda x: brand_counts[x], reverse=True)

        return Response(sorted_brands)
