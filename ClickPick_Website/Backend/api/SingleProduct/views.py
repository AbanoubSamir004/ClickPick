from django.http import Http404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import AllowAny

class ProductViewSet(ViewSet):
    permission_classes = [AllowAny]  # Add this line to allow unauthenticated access

    serializer_class = ProductSerializer

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(ProductID=pk)
        except Product.DoesNotExist:
            raise Http404("Product ID not found")

        matching_ids = product.ProductMatchingIDs  # Assuming ProductMatchingIDs is a list field in your model

        # Fetch all products with matching IDs
        matching_products = Product.objects.filter(ProductID__in=matching_ids)

        # Add the main product to the matching products list
        matching_products = [product] + list(matching_products)

        serializer = ProductSerializer(matching_products, many=True)
        return Response(serializer.data)
