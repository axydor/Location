import json,time,re
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
                    while lon=="" or (float(lon)>180 or float(lon)<-180):
                        print("please enter a longitude value between -180 and +180.")
                        lon = input("lon: ")
                    newdict['params']['lon'] = float(lon)
                    lat = input("lat: ")
                    while lat=="" or (float(lat)>90 or float(lat)<-90):
                        print("please enter a latitude value between -90 and +90.")
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
                    starttime = input("starttime: ")
                    while (re.match("[0-9][0-9][0-9][0-9]/(0[0-9]|1[0-2])/([0-9][0-9]|1[0-9]|2[0-9]|3[0-1])\ (1[0-9]|2[0-4]|0[0-9]):([0-5][0-9]|60)",starttime)) == None:
                        print("ENTER STARTTIME IN 'yyyy/mm/dd hh:hh' FORMAT")
                        starttime = input("starttime: ")

                    endtime   = input("endtime: ")
                    while (re.match("[0-9][0-9][0-9][0-9]/(0[0-9]|1[0-2])/([0-9][0-9]|1[0-9]|2[0-9]|3[0-1])\ (1[0-9]|2[0-4]|0[0-9]):([0-5][0-9]|60)",endtime)) == None:
                        print("ENTER ENDTIME IN 'yyyy/mm/dd hh:hh' FORMAT")
                        endtime = input("endtime: ")

                    newdict['params']['starttime'] = starttime
                    newdict['params']['endtime'] = endtime
                    newdict['params']['timetoann'] = input("time to announce: ")
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())
                            
                elif method=='deleteEvent':
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
                        while lon!="" and (float(lon)>180 or float(lon)<-180):
                            print("please enter a longitude value between -180 and +180.")
                            lon = input("lon: ")
                        if lon!="":
                            newdict['params']['lon'] = float(lon)  
                    lat = input("lat: ")
                    if lat!="":
                        while lat!="" and (float(lat)>90 or float(lat)<-90):
                            print("please enter a latitude value between -90 and +90.")
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
                    starttime = input("starttime: ")
                    while starttime!="" and (re.match("[0-9][0-9][0-9][0-9]/(0[0-9]|1[0-2])/([0-9][0-9]|1[0-9]|2[0-9]|3[0-1])\ (1[0-9]|2[0-4]|0[0-9]):([0-5][0-9]|60)",starttime)) == None:
                        print("ENTER STARTTIME IN 'yyyy/mm/dd hh:hh' FORMAT")
                        starttime = input("starttime: ")

                    endtime   = input("endtime: ")
                    while endtime!="" and (re.match("[0-9][0-9][0-9][0-9]/(0[0-9]|1[0-2])/([0-9][0-9]|1[0-9]|2[0-9]|3[0-1])\ (1[0-9]|2[0-4]|0[0-9]):([0-5][0-9]|60)",endtime)) == None:
                        print("ENTER ENDTIME IN 'yyyy/mm/dd hh:hh' FORMAT")
                        endtime = input("endtime: ")

                    if starttime!="":
                        newdict['params']['starttime'] = starttime
                    if endtime!="":
                        newdict['params']['endtime'] = endtime
                    timetoann = input("time to announce: ")
                    if timetoann!="":
                        newdict['params']['timetoann'] = timetoann
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())
                                
                elif method == "searchAdvanced":   # searchEvent,39.9,31,39.7,32.8,2017/11/27 19:00,+5 days,musical,opera
                    rect = {}
                    #rect={'lattl':39.9,'lontl':31,'latbr':39.7,'lonbr':32.8}
                    if input("Rectangle: ") == 'None':
                        rect = None
                    else:
                        rect['lattl'] = float(input("lattl: "))
                        rect['lontl'] = float(input("lontl: "))
                        rect['latbr'] = float(input("latbr: "))
                        rect['lonbr'] = float(input("lonbr: "))
                    starttime = input("starttime: ")
                    while starttime!="" and (re.match("[0-9][0-9][0-9][0-9]/(0[0-9]|1[0-2])/([0-9][0-9]|1[0-9]|2[0-9]|3[0-1])\ (1[0-9]|2[0-4]|0[0-9]):([0-5][0-9]|60)",starttime)) == None:
                        print("ENTER STARTTIME IN 'yyyy/mm/dd hh:hh' FORMAT")
                        starttime = input("starttime: ")

                    endtime   = input("endtime: ")
                    while endtime!="" and (re.match("\+([0-9]|1[0-2])\ ([a-z]+)",endtime)) == None and (re.match("[0-9][0-9][0-9][0-9]/(0[0-9]|1[0-2])/([0-9][0-9]|1[0-9]|2[0-9]|3[0-1])\ (1[0-9]|2[0-4]|0[0-9]):([0-5][0-9]|60)",endtime)) == None:
                        print("ENTER ENDTIME IN 'yyyy/mm/dd hh:hh' or 'n hours/days/minutes/months' FORMAT")
                        endtime = input("endtime: ")
 
                    category  = input("category: ")
                    text      = input("text: ")
 
                    if category   == '':
                        category  = None
                    if text       == '':
                        text      = None

                    newdict['params']['rectangle'] = rect
                    if starttime!="":
                        newdict['params']['starttime'] = starttime
                    else:
                        newdict['params']['starttime'] = None
                    if endtime!="":
                        newdict['params']['endtime']   = endtime
                    else:
                        newdict['params']['endtime']   = None
                    newdict['params']['category']  = category
                    newdict['params']['text']      = text
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())

                elif method == "searchbyCategory":
                    category = input("category: ") 
                    newdict['params']['category'] = category
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())

                elif method == "searchbyText":
                    text = input("Text: ") 
                    newdict['params']['text'] = text
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())

                elif method == "searchbyRect":
                    rect = {}
                    rect['lattl'] = float(input("lattl: "))
                    rect['lontl'] = float(input("lontl: "))
                    rect['latbr'] = float(input("latbr: "))
                    rect['lonbr'] = float(input("lonbr: "))            
                    newdict['params']['rectangle'] = rect
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())            

                elif method == "searchbyTime":
                    starttime = input("starttime: ") 
                    while (re.match("[0-9][0-9][0-9][0-9]/(0[0-9]|1[0-2])/([0-9][0-9]|1[0-9]|2[0-9]|3[0-1])\ (1[0-9]|2[0-4]|0[0-9]):([0-5][0-9]|60)",starttime)) == None:
                        if starttime == 'None':
                            starttime = None
                            break
                        print("ENTER STARTTIME IN 'yyyy/mm/dd hh:hh' FORMAT")
                        starttime = input("starttime: ")

                    newdict['params']['starttime'] = starttime
                    endtime   = input("endtime: ")
                    while (re.match("\+([0-9]|1[0-2])\ ([a-z]+)",endtime)) == None and (re.match("[0-9][0-9][0-9][0-9]/(0[0-9]|1[0-2])/([0-9][0-9]|1[0-9]|2[0-9]|3[0-1])\ (1[0-9]|2[0-4]|0[0-9]):([0-5][0-9]|60)",endtime)) == None:
                        if endtime == 'None':
                            endtime = None
                            break
                        print("ENTER ENDTIME IN 'yyyy/mm/dd hh:hh' or 'n hours/days/minutes/months' FORMAT")
                        endtime = input("endtime: ")
                    newdict['params']['endtime'] = endtime
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())

                elif method == "watchArea":
                    rect = {}
                    #rect={'lattl':39.9,'lontl':31,'latbr':39.7,'lonbr':32.8}
                    if input("rectangle: ") == 'None':
                        rect = None
                    else:
                        rect['lattl'] = float(input("lattl: "))
                        rect['lontl'] = float(input("lontl: "))
                        rect['latbr'] = float(input("latbr: "))
                        rect['lonbr'] = float(input("lonbr: "))
                        
                    newdict['params']['rectangle'] = rect
                    category  = input("category: ")
                    if category=="":
                        newdict['params']['category'] = None
                    else:
                        newdict['params']['category'] = category
                    c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
                    c.send(json.dumps(newdict).encode())
                
                else:
                    if  method != '':
                        print("YOU HAVE ENTERED AN ILLEGAL OPERATION, TRY AGAIN") 
            
            else:
                if  method != '':
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
                print(" NOTHING HAS BEEN FOUND ")
            else:
                if isinstance(reply[0],dict):
                    count = 0
                    for e in reply:
                        print("Event No: ", count)
                        count += 1
                        print("----------------------")
                        print("TITLE: ", e['title'], ",  LOCNAME: " , e['locname'], ",   LON: ", e['lon'], ",   LAT: " ,e['lat'])
                        print("STARTTIME: ", e['starttime'],",     ENDTIME: ",e['endtime'])
                        print("DESC: ",e['desc'])
                    count = 0
                elif isinstance(reply[0],list):
                    print(reply)
        
        elif type(reply) is dict:
                print("TITLE: ", reply['title'], ",  LOCNAME: " , reply['locname'], ",   LON: ", reply['lon'], ",   LAT: " ,reply['lat'])
                print("STARTTIME: ", reply['starttime'],",     ENDTIME: ",reply['endtime'])
                print("DESC: ",reply['desc'])                           
        
        else:
            print(reply)
        if flag==1:
            print('> ', end='', flush=True)
            flag = 0
        if reply=="connection closed":
            break
    c.close()

def start():
    c = socket(AF_INET, SOCK_STREAM)
    c.connect(('127.0.0.1', 20445))

    t = Thread(target=client, args=(c,))
    t2 = Thread(target=clientNotifier, args=(c,))

    t.start()
    t2.start()
start()
