from django.http import Http404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import Promotion
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

class PromotionsPagination(PageNumberPagination):
    page_size = 21
    page_size_query_param = 'page_size'
    max_page_size = 500

class PromotionsViewSet(ViewSet):
    permission_classes = [AllowAny]
    serializer_class = PromotionsSerializer
    pagination_class = PromotionsPagination

    def list(self, request):
        promotions = Promotion.objects.all()

        paginator = self.pagination_class()
        paginated_promotions = paginator.paginate_queryset(promotions, request)
        serializer = PromotionsSerializer(paginated_promotions, many=True)
        return paginator.get_paginated_response(serializer.data)

    def filtered_list(self, request, marketplace=None):
        promotions = Promotion.objects.all()

        if marketplace:
            promotions = Promotion.objects.filter(Marketplace__iexact=marketplace)

        paginator = self.pagination_class()
        paginated_promotions = paginator.paginate_queryset(promotions, request)
        serializer = PromotionsSerializer(paginated_promotions, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        if pk is not None:
            try:
                promotion = Promotion.objects.get(PromotionID=pk)
                serializer = PromotionsSerializer(promotion)
                return Response(serializer.data)
            except Promotion.DoesNotExist:
                raise Http404("Promotion ID not found")
        else:
            return self.list(request)
