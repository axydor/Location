import re
import math

class Event_Map_Class():
	def __init__(self):
		self.events = []
	
	def insertEvent(self,event,lat,lon):
		event.lat = lat
		event.lon = lon
		self.event.append(event)

	def deleteEvent(self,id):
		self.events.delete(id)
		
	def eventUpdated(self,id):
		print("Event with id: {0} is updataed".format(id))
	
	def searchbyRect(lattl,lontl,latbr,lonbr):
        	# return events in the given range
        	eventsinRect = []
        	for e in self.events:
            		if e.lat<=lattl and e.lat>=latbr and e.lon>=lontl and e.lon<=lonbr:
                		eventsinRect.append(e)
        	return eventsinRect

	def findClosest(self,lat,lon):
		# return closest event to the coordinate
		closestEvent = self.events[0]
		distance = math.sqrt((e.events[0].lat-lat)**2+(e.events[0].lon-lon)**2)
		for e in self.events[1:]:
			tempdist = math.sqrt((e.lat-lat)**2+(e.lon-lon)**2)
	    		if tempdist<distance:
				closestEvent = e
				distance = tempdist
		return closestEvent

	    # return events in the given time range

	 def searchbyTime(self,starttime, endtime):
		eventsbyTime = []
		for e in self.events:
	    		if e.starttime>=starttime and e.endtime<=endtime:
				eventsbyTime.append(e)
		return e

	def searchbyCategory(self,catstr):
		eventsbyCategory = []
		for e in self.events:
	    		if catstr in e.cat:	
				eventsbyCategory.append(e)
		return eventsbyCategory

	def searchbyText(self,catstr): # !! case insensitive
		eventsbyText = []
		for e in self.events:
	    		if re.search(catstr, e.title, re.IGNORECASE) or re.search(catstr, e.desc, re.IGNORECASE): # event text?
				eventsbyText.append(e)
		return eventsbyText
	
	def searchAdvanced(self,rectangle,starttime,endtime,category,text):
		returnlist = []
		for e in self.events:
			if rectangle != None and not ( e.lat<=rectangle['lattl'] and e.lat>=rectangle['latbr'] and e.lon>=rectangle['lontl'] and e.lon<=rectangle['lonbr'] ):
				continue
			if starttime != None and not ( e.starttime>=starttime ):
				continue
			if endtime != None and not   ( e.endtime<=endtime     ):
				continue
			if category != None and not ( catstr in e.cat):
				continue
			if text != None and not (re.search(text, e.title, re.IGNORECASE) or re.search(text, e.desc, re.IGNORECASE) ):
				continue
			returnlist.append(e)
		return returnlist
	
class Event():
	def __init__(self,lon,lat,title,desc,catlist,fromt,to,timetoann):
		self.lon = lon
		self.lat = lat
		self.title = title
		self.desc = desc
		self.catlist = catlist
		self.fromt = fromt
		self.to = to
		self.timetoann = timetoann
		self.map = None		

	def updateEvent(self,dicti):
		self.lat = dicti['lat']
		self.lon = dicti['lon']
		self.catlist = dicti['catlist']
		self.fromt = dicti['fromt']
		self.to = dicti['to']
		self.timetoann =   dicti['timetoann']
		self.map.eventUpdated(id(self))
	
	def getEvent(self):
		return self.__dict__
		
	def setMap(self,mapobj):
		self.map = mapobj

	def getMap(self):
		return self.map

catlist=['music','art']

fromt = "2017/11/03 19:00"
to    = "2017/11/03 21:00"
timetoann = "2017/10/03 09:00"

a = Event(33.785,39.89,"Fazil Say Concert","Music concert",catlist,fromt,to,timetoann)

b = a.getEvent()









