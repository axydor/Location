import re,pickle,datetime
import sqlite3
import math

class Event_Map_Class():
    def __init__(self):
        self.events = []
	
    def insertEvent(self,event,lat,lon):
        event.lat = lat
        event.lon = lon
        self.events.append(event)

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
        distance = math.sqrt((self.events[0].lat-lat)**2+(self.events[0].lon-lon)**2)
        for e in self.events[1:]:
            tempdist = math.sqrt((e.lat-lat)**2+(e.lon-lon)**2)
            if tempdist < distance:
                closestEvent = e
                distance = tempdist
        return closestEvent

        # return events in the given time range

    def searchbyTime(self,starttime, endtime):        # Time to String --->           time.strftime("%Y/%m/%d %H:%M",time.gmtime(b))
        eventsbyTime = []

        stime = time.strptime(starttime,"%Y/%m/%d %H:%M")   # Convert String to Time.struct_time
        stime = time.mktime( stime )                        # Convert Time.struct_time to seconds

        if( re.match("\+([0-9]|1[0-2])\ ([a-z]+)",endtime) ):    # endtime = "+num (hours|days|minutes|months)"  "+1 months"
            num = endtime.split("+")[1].split(" ")[0]            # Getting the num 
            date_str = endtime.split("+")[1].split(" ")[1]      

            if ( date_str == "minutes" ):
                etime = stime + 60 * num
            elif ( date_str == "hours" ):
                etime = stime + 60 * 60 * num
            elif (date_str == "days" ):
                etime = stime + 60 * 60 * 24 * num
            elif ( date_str == "months" ):
                etime = stime + 60  * 60 * 24 * 30 * num
        else:
            etime = time.strptime(endtime,"%Y/%m/%d %H:%M") 
            etime = time.mktime(etime)

        for e in self.events:
            e_stime = time.strptime(e.starttime,"%Y/%m/%d %H:%M")  
            e_stime = time.mktime( e_stime )                  

            e_endtime = time.strptime(e.endtime,"%Y/%m/%d %H:%M")  
            e_endtime = time.mktime( e_etime )                  

            if e_stime>= stime and e_etime<=etime:     

                eventsbyTime.append(e)

        return eventsbyTime






    def searchbyCategory(self,catstr):
        eventsbyCategory = []
        for e in self.events:
            if catstr in e.catlist:	
                eventsbyCategory.append(e)
        return eventsbyCategory

    def searchbyText(self,catstr): # !! case insensitive
        eventsbyText = []
        for e in self.events:
            if re.search(catstr, e.title, re.IGNORECASE) or re.search(catstr, e.desc, re.IGNORECASE) or re.search(catstr, e.location, re.IGNORECASE): # event text?
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

    def watchArea(self, rectangle, callback, category = None):
        pass

    
class Event():
    def __init__(self,lon,lat,title,desc,catlist,starttime,endtime,timetoann):
        self.lon = lon
        self.lat = lat
        self.title = title
        self.desc = desc
        self.catlist = catlist
        self.starttime = starttime
        self.endtime = endtime
        self.timetoann = timetoann
        self.map = None		

    def updateEvent(self,dicti):
        self.lat = dicti['lat']
        self.lon = dicti['lon']
        self.catlist = dicti['catlist']
        self.starttime = dicti['starttime']
        self.endtime = dicti['endtime']
        self.timetoann =   dicti['timetoann']
        self.map.eventUpdated(id(self))
    
    def getEvent(self):
        return self.__dict__
            
    def setMap(self,mapobj):
        self.map = mapobj

    def getMap(self):
        return self.map


class EMController(Event_Map_Class):
    def __init__(self, id = 'NEW'):
        if id == 'NEW':
            self.attachedMap = Event_Map_Class()
            print("#### inserting a new map to the db")
            pickledMap = pickle.dumps(self.attachedMap)
            print(pickledMap)
                
            DBcur = DB.insert((pickledMap,))
           
        else:
            DBcur = DB.execute("select * from map where _rowid_=%d" % int(id))
            for row in DBcur:
                print("#### Attached to the map")
                print(row[0])
                self.attachedMap = pickle.loads(row[0]) #####
            print(self.attachedMap)


    def detach(self):
        self.attachedMap = None
        # TODO all watches will be cleared up

    def save(self, name):
        pass

    # class method
    def load(name):
        pass # given name, return the id of that map from ss

    # class method
    def list(): 
        # ret the names of all maps from ss
        print("#### Listing all the maps in db")
        DBcur = DB.execute("select _rowid_,* from map")
        for row in DBcur:
            print("ID: " + str(row[0]))
            print(row[1])
            print(pickle.loads(row[1]))

    def delete(self, name):
        pass # del the map w the given name


class DBManagement:
    def __init__(self, database):
        try:
            self.con = sqlite3.connect(database)
            self.cur = self.con.cursor()
        except sqlite3.Error as e:
            print ("SQL error: ", e.args[0])

        try:
            self.cur.execute("create table map(map_instance BLOB)")
            self.con.commit()
        except:
            pass

    def execute(self, statement):
        print(statement)
        try:
            self.cur.execute(statement)
            self.con.commit()
        except sqlite3.Error as e:
            print("SQL Error: ", e.args[0])
        return self.cur

    def insert(self, arg):
        print(arg)
        try:
            self.cur.execute("insert into map values(?)", arg)
            self.con.commit()
        except sqlite3.Error as e:
            print("SQL Error: ", e.args[0])
        return self.cur

    def __del__(self):
        self.con.close()



DB = DBManagement("event.db")

example_time = "2017/11/03 13:43"

catlist=['music','art']

starttime = "2017/11/03 19:00"
to    = "2017/11/03 21:00"
timetoann = "2017/10/03 09:00"

a = Event(33.785,39.89,"Fazil Say Concert","Music concert",catlist,starttime,to,timetoann)

"""
m = Event_Map_Class()
m.insertEvent(a,33.785,39.89)

closest = m.findClosest(30,30)
print(closest.getEvent())

catSearch = m.searchbyCategory('music')
print(closest.getEvent())

b = a.getEvent()
print(b)


"""
#with open("out.txt",'w') as text:
 #   text.write(a.decode("utf-8"))

newCtrl1 = EMController('NEW')

newCtrl2 = EMController(1)

EMController.list()
