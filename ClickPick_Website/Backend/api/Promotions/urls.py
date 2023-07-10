from django.urls import path
from . import views

urlpatterns = [
    path('', views.PromotionsViewSet.as_view({'get': 'list'}), name='promotion-list'),
    path('filter/marketplace=<str:marketplace>/', views.PromotionsViewSet.as_view({'get': 'filtered_list'}), name='promotion-list-filtered'),
]
"""
"http://127.0.0.1:8000/api/promotions/?page=1" for all promotions no filter
"http://127.0.0.1:8000/api/promotions/filter/marketplace={marketplacename}/?page=1" for all filters options 
"""