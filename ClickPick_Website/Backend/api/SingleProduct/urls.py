from rest_framework import routers
from . import views
from django.urls import path, include

router = routers.DefaultRouter()
router.register('', views.ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
