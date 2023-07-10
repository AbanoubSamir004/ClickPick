from django.http import HttpResponse

# Create your views here.

def default(request):
    return HttpResponse("<h3>Hello there this is home page </h3>")
