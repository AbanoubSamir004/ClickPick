from rest_framework import routers
from . import views
from .brands import UniqueBrandsAPIView
from django.urls import path, include





urlpatterns = [
    path('', views.SalesViewSet.as_view({'get': 'list'}), name='sales-list'),
    path('page=<int:page>/', views.SalesViewSet.as_view({'get': 'list'}), name='sales-list-paginated'),
    path('filter/', views.FilteredSalesViewSet.as_view({'get': 'list'}), name='filtered-sales-list'),
    path('unique-brands/', UniqueBrandsAPIView.as_view(), name='unique-brands'),
]