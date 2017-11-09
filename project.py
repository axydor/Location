class Event_Map_Class():
	def __init__(self):
		self.events = []
	
	def inserEvent(self,event,lat,lon):
		event.lat = lat
		event.lon = lon
		self.event.append(event)

	def deleteEvent(self,id):
		self.events.delete(id)
		
	def eventUpdated(self,id):
		print("Event with id: {0} is updataed".format(id))
	
	def searchbyRect(lattl,lontl,lattbr,lonbr):
		
	
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
		dicti={}
		dicti['lat'] = self.lat
		dicti['lon'] = self.lon
		dicti['catlist'] = self.catlist
		dicti['fromt'] = self.fromt
		dicti['to'] = self.to
		dicti['timetoann'] = self.timetoann
		return dicti
		
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









