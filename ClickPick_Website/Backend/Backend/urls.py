from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import default

urlpatterns = [
    path('', default),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
