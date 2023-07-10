from django.urls import path
from .views import SubCatViewSet
from .brands import UniqueBrandsAPIView


app_name = 'subcategories'

urlpatterns = [
    
    path('', SubCatViewSet.as_view({'get': 'list'}), name='subcategory-list'),
    path('<str:subcategory>/', SubCatViewSet.as_view({'get': 'list'}), name='subcategory-filtered-list'),
    path('page=<int:page>/', SubCatViewSet.as_view({'get': 'list'}), name='subcategory-list-paginated'),
    #path('brands/', UniqueBrandsAPIView.as_view(), name='unique-brands'),
    path('<str:subcategory>/brands/', UniqueBrandsAPIView.as_view(), name='unique-brands-filtered'),
    
]
