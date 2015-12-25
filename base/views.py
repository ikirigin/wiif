from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("you're in my town now, mother fucker")
