from django.shortcuts import render

# Create your views here.
def home(request):
    return HttpResponse('hi from home')