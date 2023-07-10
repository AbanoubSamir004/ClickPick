from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home),
    path('product/', include('api.SingleProduct.urls')),
    path('promotions/', include('api.Promotions.urls')),
    path('auth/', include('api.auth_app.urls')),
    path('sales/',include('api.Sales.urls')),
    path('search/',include('api.Search.urls')),
    path('subcategory/',include('api.SubCategories.urls')),


]
"""
"http://127.0.0.1:8000/api/product/<poductid>/" get the product and its matched products also in one list 
"http://127.0.0.1:8000/api/promotions/" base api for the promptions apis
"http://127.0.0.1:8000/api/auth/" base api for the authantication apis 
"http://127.0.0.1:8000/api/fav/" base api for the fav apis 

"""