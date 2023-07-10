from django.http import JsonResponse 
from .models import *

def home(request):
    return JsonResponse({'Info':'React & Django eCommerce',"name":"ClickPick"})