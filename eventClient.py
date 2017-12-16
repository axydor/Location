import json,time
from socket import * 
from threading import Thread

flag = 0
attached = 0

def client(c):
    while True:
        global flag
        global attached
        flag = 1
        text = input("> ")
        flag = 0
        method = text.split(" ")[0]
        newdict = {'method': method, 'params':{}}

        if method=='quit':
            c.send('{:10d}'.format(len(method.encode())).encode())
            c.send(method.encode())
            break

        elif method=='list':
            newdict['params']['arg'] = text.split(" ")[1]
            if text.split(" ")[1] == 'events' and attached == 0:
                print("YOU SHOULD FIRST ATTACH TO A MAP")
            else:
                c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                c.send(json.dumps(newdict).encode())

        elif method=='attach':
            try:
                mapID = text.split(" ")[1]
                if mapID=='NEW':
                    newdict['params']['ID'] = text.split(" ")[1]
                else:
                    newdict['params']['ID'] = int(text.split(" ")[1])
            except:
                newdict['params']['ID'] = 'NEW'
            attached = 1
            c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
            c.send(json.dumps(newdict).encode())

        else:
            if attached == 1:     
                if method=='detach':
                    attached = 0
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())
                        
                elif method=='save':
                    name = text.split(" ")[1]
                    newdict['params']['name'] = name
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())
                    
                elif method=='insert':
                    lon = input("lon: ")
                    while lon=="":
                        print("please enter a value for longitude.")
                        lon = input("lon: ")
                    newdict['params']['lon'] = float(lon)
                    lat = input("lat: ")
                    while lat=="":
                        print("please enter a value for latitude.")
                        lat = input("lat: ")
                    newdict['params']['lat'] = float(lat)
                    newdict['params']['locname'] = input("location name: ")
                    while newdict['params']['locname']=="": 
                        print("please enter a location name.")
                        newdict['params']['locname'] = input("location name: ")
                    newdict['params']['title'] = input("title: ")
                    while newdict['params']['title']=="":
                        print("please enter a title.") 
                        newdict['params']['title'] = input("title: ")
                    newdict['params']['desc'] = input("description(optional): ")
                    categories = input("categories: ")
                    while categories=="":
                        print("please enter category names separated with blanks.")
                        categories = input("categories: ")
                    newdict['params']['catlist'] = categories.split(" ")
                    newdict['params']['starttime'] = input("start time: ")
                    while newdict['params']['starttime']=="":
                        print("please enter a starttime.") 
                        newdict['params']['starttime'] = input("start time: ")
                    newdict['params']['endtime'] = input("end time: ")
                    while newdict['params']['endtime']=="":
                        print("please enter an endtime.") 
                        newdict['params']['endtime'] = input("end time: ")
                    newdict['params']['timetoann'] = input("time to announce: ")
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())
                            
                elif method=='delete':
                    newdict['params']['ID'] = int(text.split(" ")[1])
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())

                elif method=='findClosest':
                    newdict['params']['lat'] = float(text.split(" ")[1])
                    newdict['params']['lon'] = float(text.split(" ")[2])
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())

                    
                elif method=='updateEvent':
                    try:
                        newdict['ID'] = text.split(" ")[1]
                    except:
                        print("please enter an event ID to update.")
                        newdict['ID'] = input("ID: ")
                        while newdict['ID']=="":
                            print("please enter an event ID to update.")
                            newdict['ID'] = input("ID: ")
                    newdict['ID'] = int(newdict['ID'])
                    lon = input("lon: ")
                    if lon!="":
                        newdict['params']['lon'] = float(lon)  
                    lat = input("lat: ")
                    if lat!="":
                        newdict['params']['lat'] = float(lat)  
                    locname = input("location name: ")
                    if locname!="":
                        newdict['params']['locname'] = locname
                    title = input("title: ")
                    if title!="":
                        newdict['params']['title'] = title
                    desc = input("description(optional): ")
                    if desc!="":
                        newdict['params']['desc'] = desc
                    categories = input("categories: ")
                    if categories!="":
                        newdict['params']['catlist'] = categories.split(" ")
                    starttime = input("start time: ")
                    if starttime!="":
                        newdict['params']['starttime'] = starttime
                    endtime = input("end time: ")
                    if endtime!="":
                        newdict['params']['endtime'] = endtime
                    timetoann = input("time to announce: ")
                    if timetoann!="":
                        newdict['params']['timetoann'] = timetoann
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())
                                
                elif method == "searchAdvanced":   # searchEvent,39.9,31,39.7,32.8,2017/11/27 19:00,+5 days,musical,opera
                    newdict = {'method': method,'params':{}}
                    rect = {}
                    #rect={'lattl':39.9,'lontl':31,'latbr':39.7,'lonbr':32.8}
                    if input("Rectangle:> ") == 'None':
                        rect = None
                    else:
                        rect['lattl'] = float(input("lattl: "))
                        rect['lontl'] = float(input("lontl: "))
                        rect['latbr'] = float(input("latbr: "))
                        rect['lonbr'] = float(input("lonbr: "))
                        starttime = input("starttime: ")
                        endtime   = input("endtime: ")
                        category  = input("category: ")
                        text      = input("text: ")

                    if starttime  == 'None':
                        starttime = None
                    if endtime    == 'None':
                        endtime   = None
                    if category   == 'None':
                        category  = None
                    if text       == 'None':
                        text      = None

                    newdict['params']['rectangle'] = rect
                    newdict['params']['starttime'] = starttime
                    newdict['params']['endtime']   = endtime
                    newdict['params']['category']  = category
                    newdict['params']['text']      = text
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())

                elif method == "searchbyCategory":
                    newdict = {'method': method,'params':{}}
                    category = input("> ") 
                    newdict['params']['category'] = category
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())

                elif method == "searchbyText":
                    newdict = {'method': method,'params':{}}
                    text = input("Text:> ") 
                    newdict['params']['text'] = text
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())

                elif method == "searchbyRect":
                    newdict = {'method': method, 'params' : {}}
                    rect = {}
                    rect['lattl'] = float(input("lattl: "))
                    rect['lontl'] = float(input("lontl: "))
                    rect['latbr'] = float(input("latbr: "))
                    rect['lonbr'] = float(input("lonbr: "))            
                    newdict['params']['rectangle'] = rect
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())            

                elif method == "searchbyTime":
                    newdict = {'method': method,'params':{}}
                    starttime = input("starttime:> ") 
                    endtime = input("endtime:> ") 
                    newdict['params']['starttime'] = starttime
                    newdict['params']['endtime'] = endtime
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())

                elif method == "watchArea":
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())

                else:
                    if text != '':
                        print("YOU HAVE ENTERED AN ILLEGAL OPERATION, TRY AGAIN")
            else:
                print("YOU SHOULD FIRST ATTACH TO A MAP")

        time.sleep(0.1)


def clientNotifier(c):
    while True:
        length = int(c.recv(10))
        reply = c.recv(length)
        reply = json.loads(reply.decode())
        global flag
        if flag==1:
            print()
        if type(reply ) is list :
            if len(reply) == 0 :
                print(" NOTHING HAS FOUND ")
            else:
                if isinstance(reply[0],dict):
                    for e in reply:
                        print("TITLE: ", e['title'], "LOCNAME: " , e['locname'], "LON: ", e['lon'], "LAT: " ,e['lat'])
                        print("STARTTIME: ", e['starttime'],"ENDTIME: ",e['endtime'])
                        print("DESC: ",e['desc'])
                        print()
                elif isinstance(reply[0],list):
                    print(reply)            
        else:
            print(reply)
        if flag==1:
            print('> ', end='', flush=True)
            flag = 0
        if reply=="connection closed":
            break
    c.close()

c = socket(AF_INET, SOCK_STREAM)
c.connect(('127.0.0.1', 20445))

t = Thread(target=client, args=(c,))
t2 = Thread(target=clientNotifier, args=(c,))

t.start()
t2.start()
