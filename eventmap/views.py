from django.shortcuts import render
from django.http import HttpResponse
from .models import Map

# Create your views here.

def listMaps(request):
    map_list = Map.objects.all()
    context = {'map_list': map_list}
    return render(request, 'eventmap/maplist.html', context)
