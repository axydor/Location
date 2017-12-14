import re,pickle,datetime
from threading import Thread, RLock
#from multiprocessing import Process, Queue
from socket import *
import json
import sqlite3
import math
import time


class Event_Map_Class():
    def __init__(self):
        self.mutex = RLock()
        self.events = []
        self.callbacks = []

    def insertEvent(self,event,lat=None,lon=None):
        with self.mutex:
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
        with self.mutex:
            if ID>=0 and ID<len(self.events):
                for cb in self.callbacks:
                    if self.events[ID] in self.searchAdvanced(cb['rect'], None, None, cb['category'],None):
                        self.__fire(cb['observer'], cb['callback'],'DELETE', self.events[ID])

                self.events[ID].setMap(None)
                del self.events[ID]

    def eventUpdated(self,ID):
        with self.mutex:
            event = None
            for e in self.events:
                if(id(e)==ID):
                    event = e
            for cb in self.callbacks:
                if event in self.searchAdvanced(cb['rect'], None, None, cb['category'],None):
                    self.__fire(cb['observer'], cb['callback'],'UPDATE',event)

    def findClosest(self,lat,lon):
        # return closest event to the coordinate
        with self.mutex:
            if len(self.events)>0:
                closestEvent = self.events[0]
                distance = math.sqrt((self.events[0].lat-lat)**2+(self.events[0].lon-lon)**2)
                for e in self.events[1:]:
                    tempdist = math.sqrt((e.lat-lat)**2+(e.lon-lon)**2)
                    if tempdist < distance:
                        closestEvent = e
                        distance = tempdist
                return closestEvent
            else:
                return None

    def searchbyRect(self,lattl,lontl,latbr,lonbr):
        # return events in the given range
        with self.mutex:
            rectangle = {'lattl':lattl,'lontl':lontl,'latbr':latbr,'lonbr':lonbr}
            return self.searchAdvanced(rectangle, None, None, None, None)

    def searchbyTime(self,starttime, endtime):        # Time to String --->           time.strftime("%Y/%m/%d %H:%M",time.gmtime(b))
        # return events in the given time range
        with self.mutex:
            return self.searchAdvanced(None,starttime,endtime,None,None)

    def searchbyCategory(self,catstr):
        with self.mutex:
            return self.searchAdvanced(None,None,None,catstr,None)

    def searchbyText(self,catstr): # !! case insensitive
        with self.mutex:
            return self.searchAdvanced(None,None,None,None,catstr)

    def searchAdvanced(self,rectangle,starttime,endtime,category,text):
        with self.mutex:
            returnlist = []
            for e in self.events:

                if rectangle != None :
                    if e.lat<=rectangle['lattl'] and e.lat>=rectangle['latbr'] and e.lon>=rectangle['lontl'] and e.lon <= rectangle['lonbr']:
                        if e not in returnlist:
                            returnlist.append(e)
                    else:
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
                        if ( (e_stime >= stime and e_stime < etime ) or (e_endtime > stime and e_endtime <= etime) ) :
                            if e not in returnlist:
                                returnlist.append(e)
                        else:
                            continue

                if category != None:
                    if category in e.catlist:
                        if e not in returnlist:
                            returnlist.append(e)
                    else:
                        continue 

                if text != None :
                    if re.search(text, e.title, re.IGNORECASE) or re.search(text, e.desc, re.IGNORECASE) or re.search(text, e.locname, re.IGNORECASE):
                        if e not in returnlist:
                            returnlist.append(e)
                    else:
                        continue
                if e not in returnlist:
                    returnlist.append(e)
            return returnlist


    def __fire(self, observer, callback, type_, event):
        with self.mutex:
            observer.notify(callback, type_, event)

    def watchArea(self, rectangle, callback, category = None, observer = None):
        with self.mutex:
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
        self.mutex = RLock()

    def updateEvent(self,dicti):
        with self.mutex:
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
        with self.mutex:
            res =  self.__dict__.copy()
            del res['map']
            del res['mutex']
            return res

    def setMap(self,mapobj):
        with self.mutex:
            self.map = mapobj

    def getMap(self):
        with self.mutex:
            return self.map


#class Singleton(type):
#    _instances = {}
#    def __call__(cls, *args, **kwargs):
#        if cls not in cls._instances:
#            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#        return cls._instances[cls]  


class EMController(Event_Map_Class):
    def __init__(self, ID = 'NEW'):
        if ID!='NEW':
            DBcur = DB.execute("select * from map where _rowid_={}".format(ID))
            for row in DBcur:
                self.attachedMap = pickle.loads(row[1])
                print("#### Attached to the map")
                print(row[0])
        else:
            self.attachedMap = Event_Map_Class()

        self.events = self.attachedMap.events
        self.callbacks = self.attachedMap.callbacks

    def detach(self):
        self.events = []
        for cb in self.attachedMap.callbacks:
            if cb['observer']==self:
                self.attachedMap.callbacks.remove(cb)
        self.attachedMap = None

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
        

def echoservice(sock):
    ''' echo uppercase string back in a loop'''
    length = int(sock.recv(10))
    req = sock.recv(length)
    while req and req != '':
        # remove trailing newline and blanks
        req = req.rstrip().decode()

        if req=="quit":
            sock.send("connection closed".encode())
            break


        req = json.loads(req)

        if req['method']=="save":
            newctrl.save(req['params']['name'])
            sock.send("attached map saved.".encode())

        elif req['method']=='attach':
            try:
                newctrl = EMController(req['params']['ID'])
            except:
                newctrl = EMController()
            sock.send("Attached to the map".encode())

        elif req['method']=='detach':
            newctrl.detach()
            sock.send("detached from map".encode())

        elif req['method']=='list' and req['params']['arg']=='maps':
            mapList = EMController.list()
            sock.send('{:10d}'.format(len(json.dumps(mapList).encode())).encode())
            sock.send(json.dumps(mapList).encode())

        elif req['method']=='list' and req['params']['arg']=='events':
            eventList = []
            for e in newctrl.events:
                eventList.append(e.getEvent())
            sock.send('{:10d}'.format(len(json.dumps(eventList).encode())).encode())
            sock.send(json.dumps(eventList).encode())

        elif req['method']=='insert':
            newEvent = Event(**req['params'])
            newctrl.attachedMap.insertEvent(newEvent)
            sock.send("new event successfully inserted.".encode())
            print(newctrl.attachedMap.events)

        elif req['method']=='delete':
            newctrl.attachedMap.deleteEvent(req['params']['ID'])
            sock.send("event successfully deleted.".encode())
            print(newctrl.attachedMap.events)

        elif req['method']=='findClosest':
            closestEvent = newctrl.attachedMap.findClosest(req['params']['lat'], req['params']['lon'])
            if closestEvent != None:
                print(closestEvent.getEvent())
                sock.send('{:10d}'.format(len(json.dumps(closestEvent.getEvent()).encode())).encode())
                sock.send(json.dumps(closestEvent.getEvent()).encode())
            else:
                sock.send('{:10d}'.format(len(json.dumps("map is empty.").encode())).encode())
                sock.send(json.dumps("map is empty.").encode())

        elif req['method']=='updateEvent':
            newctrl.attachedMap.events[req['ID']].updateEvent(req['params'])
            sock.send(("event with ID:"+str(req['ID'])+" successfully updated.").encode())
            print(newctrl.attachedMap.events)

        elif req['method'] == 'searchAdvanced':
            searchedEvents = []
            searchedEvents = EMController().attachedMap.searchAdvanced(**req['params'])
            sock.send('{:10d}'.format(len(json.dumps(searchedEvents).encode())).encode())
            sock.send(json.dumps(searchedEvents).encode())

        elif req['method'] == 'searchbyRect':
            searchedEvents = []
            searchedEvents = EMController().attachedMap.searchbyRect(**req['params'])
            sock.send('{:10d}'.format(len(json.dumps(searchedEvents).encode())).encode())
            sock.send(json.dumps(searchedEvents).encode())            

        elif req['method'] == 'searchbyCategory':
            searchedEvents = []
            searchedEvents = EMController().attachedMap.searchbyCategory(**req['params'])
            sock.send('{:10d}'.format(len(json.dumps(searchedEvents).encode())).encode())
            sock.send(json.dumps(searchedEvents).encode())            

        elif req['method'] == 'searchbyTime':
            searchedEvents = []
            searchedEvents = EMController().attachedMap.searchbyTime(**req['params'])
            sock.send('{:10d}'.format(len(json.dumps(searchedEvents).encode())).encode())
            sock.send(json.dumps(searchedEvents).encode())            

        elif req['method'] == 'searchbyText':
            searchedEvents = []
            searchedEvents = EMController().attachedMap.searchbyText(**req['params'])
            sock.send('{:10d}'.format(len(json.dumps(searchedEvents).encode())).encode())
            sock.send(json.dumps(searchedEvents).encode())            

        length = int(sock.recv(10))
        req = sock.recv(length)
        
    print(sock.getpeername(), ' closing')
    sock.shutdown(SHUT_RDWR)
    sock.close()

        
def server(port):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('',port))
    s.listen(1) 
    try:
        while True:
            ns, peer = s.accept()
            print(peer, "connected")

            t = Thread(target = echoservice, args=(ns,))
            t.start()
    finally:
        s.close()
        

class DBManagement:
    def __init__(self, database):
        try:
            self.con = sqlite3.connect(database, check_same_thread=False)
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


server = Thread(target=server, args=(20445,))
server.start()
