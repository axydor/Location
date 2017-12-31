from django.shortcuts import render
from django.http import HttpResponse
from .models import Map, Event

# Create your views here.

def listMaps(request):
    map_list = Map.objects.all()
    context = {'map_list': map_list}
    return render(request, 'eventmap/maplist.html', context)

def listEvents(request,mapid):
    category = request.GET.get("category", None)
    if category:
        event_list = Event.objects.filter(catlist__contains=category)
    else:
        event_list = Event.objects.all()

    context = {'event_list': event_list}
    return render(request,'eventmap/eventlist.html',context)
