from django.urls import path
from .views import *
from .brands import *
app_name = 'search'

urlpatterns = [
    path('', ProductViewSet.as_view({'get': 'list'}), name='search-list'),
    path('<str:query>/', ProductViewSet.as_view({'get': 'search'}), name='search-query'),
    path('page=<int:page>/', ProductViewSet.as_view({'get': 'list'}), name='subcategory-list-paginated'),
    path('<str:query>/brands/', UniqueBrandsSearchAPIView.as_view(), name='unique-brands-filtered'),

]
