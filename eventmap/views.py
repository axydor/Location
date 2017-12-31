from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Map, Event

# Create your views here.

def listMaps(request):
    map_list = Map.objects.all()
    context = {'map_list': map_list}
    return render(request, 'eventmap/maplist.html', context)

def listEvents(request,mapid):
    if request.method == 'GET':
        event_list = Event.objects.filter(mapid__id=mapid)
        context = {'event_list': event_list, 'mapid':mapid}  # Inserted mapid here for inserting event 
        return render(request,'eventmap/eventlist.html',context)
    else: # request.method == 'POST'
        eventToDelete = Event.objects.get( id =  request.POST.get('eventToBeDeleted'))
        eventToDelete.delete()
        event_list = Event.objects.filter(mapid__id=mapid)
        context = {'event_list': event_list, 'mapid':mapid}  # Inserted mapid here for inserting event 
        return render(request,'eventmap/eventlist.html',context)

def insertEvent(request,mapid):
    if request.method == 'GET':
        context = {'mapid': mapid}
        return render(request,'eventmap/insertEvent.html',context)
    if request.method == 'POST':
        lon = float(request.POST.get('lonfield',None))
        lat = float(request.POST.get('latfield',None))
        locname = request.POST.get('locnamefield',None) 
        title = request.POST.get('titlefield',None)
        desc = request.POST.get('descfield',None)
        catlist = request.POST.get('categoryfield',None) # ONLY GET 1 CATEGORY
        starttime = request.POST.get('starttimefield',None)
        endtime = request.POST.get('endtimefield',None)
        timetoann = request.POST.get('timetoannfield',None)
        ourMap = Map.objects.get(id=mapid)
        newEvent = Event(lon=lon,lat=lat,locname=locname,title=title,desc=desc,catlist=catlist,
            starttime=starttime,endtime=endtime,timetoann=timetoann,mapid=ourMap)
        newEvent.save()   #Insert event to database belonging to the map with id =  mapid
        event_list = Event.objects.filter(mapid__id=mapid)
        context = {'event_list': event_list, 'mapid':mapid}  # Inserted mapid here for inserting event 
        return HttpResponseRedirect("/eventmap/"+str(mapid) +"/")
