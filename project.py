import re,pickle,datetime
import sqlite3
import math
import time


class Event_Map_Class():
    def __init__(self):
        self.events = []
        self.callbacks = []

    def insertEvent(self,event,lat=None,lon=None):
        if lat:
            if lat > 90 or lat < -90:
                raise ValueError("ERROR WRONG LATITUDE")
            event.lat = lat
        if lon:
            if lon > 180 or lon < -180:
                raise ValueError("ERROR WRONG LONGTITUDE")
            event.lon = lon
        self.events.append(event)
        event.setMap ( self )

        for cb in self.callbacks:
            if event in self.searchAdvanced(cb['rect'], None, None, cb['category'],None):
                self.__fire(cb['observer'], cb['callback'],'INSERT',event)

    def deleteEvent(self,ID):
        event = None
        for e in self.events:
            if ID == id(e):
                event = e

        for cb in self.callbacks:
            if event in self.searchAdvanced(cb['rect'], None, None, cb['category'],None):
                self.__fire(cb['observer'], cb['callback'],'DELETE',event)

        if event != None:
            event.setMap(None)
            self.events.remove(event)

    def eventUpdated(self,ID):
        event = None
        for e in self.events:
            if(id(e)==ID):
                event = e
        for cb in self.callbacks:
            if event in self.searchAdvanced(cb['rect'], None, None, cb['category'],None):
                self.__fire(cb['observer'], cb['callback'],'UPDATE',event)
        print("------------------------------------------------------------------------------------")
        print("Event is updated to {0}".format(event.title))
        print("------------------------------------------------------------------------------------")

    def findClosest(self,lat,lon):
        # return closest event to the coordinate
        if  len ( self.events ) != 0 :
            closestEvent = self.events[0]
            distance = math.sqrt((self.events[0].lat-lat)**2+(self.events[0].lon-lon)**2)
            for e in self.events[1:]:
                tempdist = math.sqrt((e.lat-lat)**2+(e.lon-lon)**2)
                if tempdist < distance:
                    closestEvent = e
                    distance = tempdist
            return closestEvent
        return None
        
    def searchbyRect(self,lattl,lontl,latbr,lonbr):
        # return events in the given range
        rectangle = {'lattl':lattl,'lontl':lontl,'latbr':latbr,'lonbr':lonbr}
        return self.searchAdvanced(rectangle, None, None, None, None)

    def searchbyTime(self,starttime, endtime):        # Time to String --->           time.strftime("%Y/%m/%d %H:%M",time.gmtime(b))
        # return events in the given time range
        return self.searchAdvanced(None,starttime,endtime,None,None)

    def searchbyCategory(self,catstr):
        return self.searchAdvanced(None,None,None,catstr,None)

    def searchbyText(self,catstr): # !! case insensitive
        return self.searchAdvanced(None,None,None,None,catstr)

    def searchAdvanced(self,rectangle,starttime,endtime,category,text):
        returnlist = []
        for e in self.events:

            if rectangle != None :
                if not (e.lat<=rectangle['lattl'] and e.lat>=rectangle['latbr'] and e.lon>=rectangle['lontl'] and e.lon <= rectangle['lonbr']):
                    continue

            if starttime != None or endtime != None :
                if (starttime == None):
                    stime = 0
                if (endtime == None):
                    etime = float(math.inf)
                else:
                    stime = time.strptime(starttime,"%Y/%m/%d %H:%M")   # Convert String to Time.struct_time
                    stime = time.mktime( stime )                        # Convert Time.struct_time to seconds

                    if( re.match("\+([0-9]|1[0-2])\ ([a-z]+)",endtime) ):    # endtime = "+num (hours|days|minutes|months)"  "+1 months"
                        num = int (endtime.split("+")[1].split(" ")[0] )           # Getting the num
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

                    e_stime = time.strptime(e.starttime,"%Y/%m/%d %H:%M")
                    e_stime = time.mktime( e_stime )
                    e_endtime = time.strptime(e.endtime,"%Y/%m/%d %H:%M")
                    e_endtime = time.mktime( e_endtime )
                    if not ( (e_stime >= stime and e_stime < etime ) or (e_endtime > stime and e_endtime <= etime) ) :
                        continue

            if category != None:
                if not (category in e.catlist ):
                    continue 

            if text != None :
                if not ( re.search(text, e.title, re.IGNORECASE) or re.search(text, e.desc, re.IGNORECASE) or re.search(text, e.locname, re.IGNORECASE) ):
                    continue
            returnlist.append(e)
        return returnlist


    def __fire(self, observer, callback, type_, event):
        observer.notify(callback, type_, event)

    def watchArea(self, rectangle, callback, category = None, observer = None):
        new_dict = {'rect':rectangle,'callback':callback,'category':category, 'observer': observer}
        if observer==None:
            new_dict['observer'] = 'all'
        self.callbacks.append(new_dict)

        
        
class Event():
    def __init__(self,lon,lat,locname,title,catlist,starttime,endtime,timetoann,desc=None):
        self.lon = lon
        self.lat = lat
        self.locname = locname
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
        self.locname = dicti['locname']
        self.catlist = dicti['catlist']
        self.starttime = dicti['starttime']
        self.title = dicti['title']
        self.desc = dicti['desc']
        self.endtime = dicti['endtime']
        self.timetoann =   dicti['timetoann']
        self.map.eventUpdated(id(self))

    def getEvent(self):
        return self.__dict__

    def setMap(self,mapobj):
        self.map = mapobj

    def getMap(self):
        return self.map

    

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]  


class EMController(Event_Map_Class, metaclass=Singleton):
    def __init__(self, ID = 'NEW'):
        self.attachedMap = Event_Map_Class()
        if ID!='NEW':
            DBcur = DB.execute("select * from map where _rowid_={}".format(ID))
            for row in DBcur:
                self.attachedMap = pickle.loads(row[1])
                print("#### Attached to the map")
                print(row[0])

        self.events = self.attachedMap.events
        self.callbacks = self.attachedMap.callbacks

    def detach(self):
        self.attachedMap = None
        self.events = None

        for cb in self.attachedMap.callbacks:
            if cb['observer']==self:
                self.attachedMap.callbacks.remove(cb)

    def save(self, name):
        print("#### inserting a new map to the db")
        pickledMap = pickle.dumps(self.attachedMap)

        DBcur = DB.insert((name, pickledMap))

    @classmethod
    def load(cls,name):
        DBcur = DB.execute("select * from map where map_name='{}'".format(name))
        for row in DBcur:
            newEventMap = pickle.loads(row[1])
            mapID = id(newEventMap)
            return mapID

    # class method
    @classmethod
    def list(cls):
        # ret the names of all maps from ss
        print("#### Listing all the maps in db")
        maplist = []
        DBcur = DB.execute("select _rowid_,map_name from map")
        for row in DBcur:
            maplist.append(row[1])
        return maplist

    @classmethod
    def delete(cls,name):
        # del the map w the given name
        DBcur = DB.execute("delete from map where map_name='{}'".format(name))

    def watchArea(self, rectangle, callback, category = None):
        super().watchArea(rectangle, callback, category, self)

    def notify(self, callback, type_, event):
        callback(type_, event)

        

class DBManagement:
    def __init__(self, database):
        try:
            self.con = sqlite3.connect(database)
            self.cur = self.con.cursor()
        except sqlite3.Error as e:
            print ("SQL error: ", e.args[0])

        try:
            self.cur.execute("create table if not exists map(map_name TEXT, map_instance BLOB)")
            self.con.commit()
        except sqlite3.Error as e:
            print ("SQL error: ", e.args[0])

    def execute(self, statement):
        try:
            self.cur.execute(statement)
            self.con.commit()
        except sqlite3.Error as e:
            print("SQL Error: ", e.args[0])
        return self.cur


    def insert(self, arg):
        try:
            self.cur.execute("insert into map values(?,?)", arg)
            self.con.commit()
        except sqlite3.Error as e:
            print("SQL Error: ", e.args[0])
        return self.cur

    def __del__(self):
        self.con.close()




DB = DBManagement("event.db")


