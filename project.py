import re,pickle,datetime
import sqlite3
import math



class Event_Map_Class():
    def __init__(self):
        self.events = []

    def insertEvent(self,event,lat=None,lon=None):
        if not lat == None:
            event.lat = lat
        if not lon == None:
            event.lon = lon
        self.events.append(event)
        event.setmap ( self )

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

            if ( (e_stime >= stime and  e_stime < etime ) or (e_etime > stime and e_etime <= etime) ) :
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
            if re.search(catstr, e.title, re.IGNORECASE) or re.search(catstr, e.desc, re.IGNORECASE) or re.search(catstr, e.locname, re.IGNORECASE):                 eventsbyText.append(e)
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
            if text != None and not ( re.search(text, e.title, re.IGNORECASE) or re.search(text, e.desc, re.IGNORECASE) or re.search(text, e.locname, re.IGNORECASE) ) :
                continue
            returnlist.append(e)
        return returnlist

    def watchArea(self, rectangle, callback, category = None):
        pass

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

class EMController(Event_Map_Class):
    def __init__(self, ID = 'NEW'):
        if id == 'NEW':
            self.attachedMap = super(EMController,self).__init__()
        else:
            DBcur = DB.execute("select * from map ")
            for row in DBcur:
                print("#### Attached to the map")
                temp_map = pickle.loads(row[1])
                if id( temp_map ) == ID:
                    self.attachedMap = pickle.loads(row[1]) #####
                    print(row[0])

        self.callbacks = []

    def detach(self):
        self.attachedMap = None
        # TODO all watches will be cleared up

    def save(self, name):
        print("#### inserting a new map to the db")
        pickledMap = pickle.dumps(self.attachedMap)
        print(pickledMap)

        DBcur = DB.insert((name, pickledMap))

    # class method
    @classmethod
    def load(cls,name):
        # given name, return the id of that map from ss
        DBcur = DB.execute("select * from map where map_name='{}'".format(name))
        for row in DBcur:
            print(row[1])
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
            print("ID: " + str(row[0]))
            print("name: " + str(row[1]))
            maplist.append(row[1])
        return maplist

    @classmethod
    def delete(cls,name):
        # del the map w the given name
        DBcur = DB.execute("delete from map where map_name='{}'".format(name))

    def watchArea(self, rectangle, callback, category = None):
        new_dict = {'rect':rectangle,'callback':callback,'category':category}
        self.callbacks.append(new_dict)


    def insertEvent(self,event,lat=None,lon = None):
        event.lat = lat
        event.lon = lon
        self.events.append(event)

        for cb in self.callbacks:
            if event in searchAdvanced(cb[rect], None, None, cb[category],None):
                cb[callback]('INSERT',event)

    def deleteEvent(self,id):
        for cb in self.callbacks:
            if event in searchAdvanced(cb[rect], None, None, cb[category],None):
                cb[callback]('DELETE',event)
        self.events.delete(id)

    def eventUpdated(self,id):
        print("Event with id: {0} is updataed".format(id))
        for cb in self.callbacks:
            if event in searchAdvanced(cb[rect], None, None, cb[category],None):
                cb[callback]('UPDATE',event)

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
            self.cur.execute("insert into map values(?,?)", arg)
            self.con.commit()
        except sqlite3.Error as e:
            print("SQL Error: ", e.args[0])
        return self.cur

    def __del__(self):
        self.con.close()




DB = DBManagement("event.db")


"""
example_time = "2017/11/03 13:43"

catlist=['music','art']

starttime = "2017/11/03 19:00"
to    = "2017/11/03 21:00"
timetoann = "2017/10/03 09:00"

a = Event(33.785,39.89,"Mert'in Evi","Fazil Say Concert","Music concert",catlist,starttime,to,timetoann)


m = Event_Map_Class()
m.insertEvent(a,33.785,39.89)

closest = m.findClosest(30,30)
print(closest.getEvent())

catSearch = m.searchbyCategory('music')
print(closest.getEvent())

b = a.getEvent()
print(b)


#with open("out.txt",'w') as text:
 #   text.write(a.decode("utf-8"))

newCtrl1 = EMController('NEW')
newCtrl1.save('MoviesMap')
newCtrl2 = EMController(1)

EMController.list()

print(EMController.load('MoviesMap'))

EMController.delete('MoviesMap')
EMController.list()
"""
