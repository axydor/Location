from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Map, Event
from datetime import datetime
from django.http import JsonResponse
import math
from django.views.decorators.csrf import csrf_exempt
import os

# Create your views here.
watches = []

def listMaps(request):
    if request.method == "GET":
        map_list = Map.objects.all()
        context = {'map_list': map_list}
        return render(request, 'eventmap/maplist.html', context)
    
    elif request.method == 'POST':
        map_name = request.POST.get('map_name',None)
        newMap = Map(map_name = map_name)
        newMap.save()
        return HttpResponseRedirect('/eventmap/')

@csrf_exempt
def listEvents(request,mapid):
    if request.method == 'GET':
        if request.GET.get("id", None):
            if 'mapid' in request.COOKIES:
                attachedMapID = request.COOKIES['mapid']
                print(attachedMapID)
                if attachedMapID==str(mapid):
                    eventToUpdate = Event.objects.get( id =  request.GET.get("id", None))

                    date_1 = str(eventToUpdate.starttime.year)+"-"+ '{:02d}'.format(eventToUpdate.starttime.month)+"-"+ '{:02d}'.format(eventToUpdate.starttime.day)+"T"+ '{:02d}'.format(eventToUpdate.starttime.hour)+":"+ '{:02d}'.format(eventToUpdate.starttime.minute)
                    date_2 = str(eventToUpdate.endtime.year)+"-"+ '{:02d}'.format(eventToUpdate.endtime.month)+"-"+ '{:02d}'.format(eventToUpdate.endtime.day)+"T"+ '{:02d}'.format(eventToUpdate.endtime.hour)+":"+ '{:02d}'.format(eventToUpdate.endtime.minute)
                    date_3 = str(eventToUpdate.timetoann.year)+"-"+ '{:02d}'.format(eventToUpdate.timetoann.month)+"-"+ '{:02d}'.format(eventToUpdate.timetoann.day)+"T"+ '{:02d}'.format(eventToUpdate.timetoann.hour)+":"+ '{:02d}'.format(eventToUpdate.timetoann.minute)
                    context = {'event':eventToUpdate,'starttime':date_1, 'endtime':date_2,'timetoann':date_3,'mapid':mapid}   # SENDING EVENT SO THAT INPUT FIELDS WILL NOT BE EMPTY
                    return render(request,'eventmap/updateEvent.html',context)
                else:
                    return HttpResponseRedirect("/eventmap/")
        elif request.GET.get("category", None) or (
                request.GET.get("text", None)) or (
                    request.GET.get("lattl", None)) or(
                        request.GET.get("fromtime", None)):
            if 'mapid' in request.COOKIES:
                attachedMapID = request.COOKIES['mapid']
                print(attachedMapID)
                if attachedMapID==str(mapid):
                    print(request)
                    event_list = Event.objects.filter(mapid__id=mapid)
                    category = request.GET.get("category", None)
                    text = request.GET.get("text", None)
                    lattl = request.GET.get("lattl", None)
                    lontl = request.GET.get("lontl", None)
                    latbr = request.GET.get("latbr", None)
                    lonbr = request.GET.get("lonbr", None)
                    fromtime = request.GET.get("fromtime", None)
                    untiltime = request.GET.get("untiltime", None)
                    if category:
                        event_list = event_list.filter(catlist__contains=category)
                    if text:
                        event_list = event_list.filter(title__contains=text) | event_list.filter(desc__contains=text)
                    if lattl:
                        event_list = event_list.filter(lat__gte=latbr, lat__lte=lattl, lon__gte=lontl, lon__lte=lonbr)
                    if fromtime:
                        event_list = event_list.filter(starttime__gte=fromtime,starttime__lt=untiltime) | event_list.filter(endtime__gt=fromtime, endtime__lte=untiltime) | event_list.filter(starttime__lte=fromtime, endtime__gte=untiltime)
                    

                    context = {'event_list': event_list, 'mapid':mapid}  # Inserted mapid here for inserting event 
                    context['event_list'] = list(event_list.values())
                    return JsonResponse(context)
                else:
                    return HttpResponseRedirect("/eventmap/")

        elif request.GET.get("lat", None):
            if 'mapid' in request.COOKIES:
                attachedMapID = request.COOKIES['mapid']
                print(attachedMapID)
                if attachedMapID==str(mapid):
                    events = list(Event.objects.filter(mapid__id=mapid).values())
                    event_ = None
                    if len(events) > 0:
                        lat = float(request.GET.get("lat", None))
                        lon = float(request.GET.get("lon", None))
                        closestEvent = events[0]
                        distance = math.sqrt((closestEvent['lat']-lat)**2
                                + (closestEvent['lon']-lon)**2)
                        for e in events[1:]:
                            tempdist = math.sqrt((e['lat']-lat)**2+(e['lon']-lon)**2)
                            if tempdist < distance:
                                closestEvent = e
                                distance = tempdist
                        event_ = closestEvent
                        print(event_)
                    context = {'event_' : event_, 'mapid' : mapid}
                    return JsonResponse(context)
                else:
                    return HttpResponseRedirect("/eventmap/")

        elif request.GET.get("delid",None):
            if 'mapid' in request.COOKIES:
                attachedMapID = request.COOKIES['mapid']
                print(attachedMapID)
                if attachedMapID==str(mapid):
                    event = Event.objects.get( id =  request.GET.get('delid'))
                    for w in watches:
                        if w['category'] and w['category'] not in event.catlist.split(";"):
                            print(event.catlist.split(";"))
                            continue
                        if w['latbr']:
                            print(w['latbr'])
                            if not (event.lat<=w['lattl'] and event.lat>=w['latbr'] and event.lon>=w['lontl'] and event.lon <= w['lonbr']):
                                continue
                        print("printf '{\"id\":\"" + w['id'] + "\", \"message\":\"delete of event " 
                                + event.title + "\"}' | nc -u -w 1 127.0.0.1 9999")
                        os.system("printf '{\"id\":\"" + w['id'] + "\", \"message\":\"delete of event " 
                                + event.title + "\"}' | nc -u -w 1 127.0.0.1 9999")
                    event.delete()
                    print("event " + event.title + " deleted")

                    event_list = Event.objects.filter(mapid__id=mapid)
                    context = {'event_list': event_list, 'mapid':mapid}  # Inserted mapid here for inserting event 
                    context['event_list'] = list(event_list.values())
                    return JsonResponse(context)                    
                else:
                    return HttpResponseRedirect("/eventmap/")                    

        else:
            event_list = Event.objects.filter(mapid__id=mapid)
            context = {'event_list': event_list, 'mapid':mapid}  # Inserted mapid here for inserting event 
            response = render(request,'eventmap/eventlist.html',context)
            response.set_cookie('mapid', mapid)
            return response
    else: # request.method == 'POST'
        if request.POST.get('eventToBeDeleted') != None:
            eventToDelete = Event.objects.get( id =  request.POST.get('eventToBeDeleted'))
            eventToDelete.delete()
            event_list = Event.objects.filter(mapid__id=mapid)
            context = {'event_list': event_list, 'mapid':mapid}  # Inserted mapid here for inserting event 
            return render(request,'eventmap/eventlist.html',context) 

        elif request.POST.get('myid', None):
            myid = request.POST.get('myid')
            category = request.POST.get('category_w', None)
            lattl = request.POST.get('lattl_w', None)
            lontl = request.POST.get('lontl_w', None)
            latbr = request.POST.get('latbr_w', None)
            lonbr = request.POST.get('lonbr_w', None)
            w = {'id' : myid, 'category' : category, 'lattl': lattl, 'lontl' :lontl,
                    'latbr' : latbr, 'lonbr' : lonbr}
            watches.append(w)
            print("category: "+w['category'])
            return JsonResponse({'message':'watch operation was successful'})
        
        else:  # WHEN THE USER POST DATA(PUSH THE UPDATE EVENT BUTTON) FROM THE updateEvent.html THE USER COMES HERE
            lon = float(request.POST.get('lon',None))
            lat = float(request.POST.get('lat',None))
            locname = request.POST.get('locname',None) 
            title = request.POST.get('title',None)
            desc = request.POST.get('desc',None)
            catlist = request.POST.get('category',None)
            starttime = request.POST.get('starttime',None)
            endtime = request.POST.get('endtime',None)
            timetoann = request.POST.get('timetoann',None)
            ourMap = Map.objects.get(id=mapid)
            newEvent = Event(lon=lon,lat=lat,locname=locname,title=title,desc=desc,catlist=catlist,
                starttime=starttime,endtime=endtime,timetoann=timetoann,mapid=ourMap)
            newEvent.save()   #Insert event to database belonging to the map with id =  mapid
            for w in watches:
                print("category: "+w['category'])
                if w['category'] and w['category'] not in newEvent.catlist.split(";"):
                    print(newEvent.catlist.split(";"))
                    continue
                if w['latbr']:
                    print(w['latbr'])
                    if not (newEvent.lat<=w['lattl'] and newEvent.lat>=w['latbr'] and newEvent.lon>=w['lontl'] and newEvent.lon <= w['lonbr']):
                        continue
                os.system("printf '{\"id\":\"" + w['id'] + "\", \"message\":\"new event inserted with title " 
                        + newEvent.title + "\"}' | nc -u -w 1 127.0.0.1 9999")
            event_list = Event.objects.filter(mapid__id=mapid)
            context = {'event_list': event_list, 'mapid':mapid}  # Inserted mapid here for inserting event 
            context['event_list'] = list(event_list.values())
            return JsonResponse(context)            
            #return updateEvent(request,mapid)


def insertEvent(request,mapid):
    if 'mapid' in request.COOKIES:
        attachedMapID = request.COOKIES['mapid']
        print(attachedMapID)
        if attachedMapID==str(mapid):
            if request.method == 'GET':
                context = {'mapid': mapid}
                return render(request,'eventmap/insertEvent.html',context)
            if request.method == 'POST':
                lon = float(request.POST.get('lonfield',None))
                lat = float(request.POST.get('latfield',None))
                locname = request.POST.get('locnamefield',None) 
                title = request.POST.get('titlefield',None)
                desc = request.POST.get('descfield',None)
                catlist = request.POST.get('categoryfield',None)
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
        else: # user should attach to a map before proceeding
            return HttpResponseRedirect("/eventmap/")


def updateEvent(request,mapid):         # GET THE OBJECT AND UPDATE AND RETURN THE USER TO THE eventmap/{{mapid}}/  page
    if 'mapid' in request.COOKIES:
        attachedMapID = request.COOKIES['mapid']
        print(attachedMapID)
        if attachedMapID==str(mapid):
            event_id = int(request.POST.get('event_id',None))
            event = Event.objects.get(pk = event_id)    # PK: PRIMARY KEY
            event.lon = float(request.POST.get('lonfield',None))
            event.lat = float(request.POST.get('latfield',None))
            event.locname = request.POST.get('locnamefield',None) 
            event.title = request.POST.get('titlefield',None)
            event.desc = request.POST.get('descfield',None)
            event.catlist = request.POST.get('categoryfield',None) # ONLY GET 1 CATEGORY
            event.starttime = request.POST.get('starttimefield',None)
            event.endtime = request.POST.get('endtimefield',None)
            event.timetoann = request.POST.get('timetoannfield',None)
            event.save()   # SAVE THE CHANGES
            print("event " + event.title + " updated")
            return HttpResponseRedirect("/eventmap/"+str(mapid) +"/")
        else:
            return HttpResponseRedirect("/eventmap/")


