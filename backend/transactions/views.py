from django.shortcuts import HttpResponse


def index(request):
    return HttpResponse("Django server is running")
