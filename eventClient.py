import json,time
from socket import * 
from threading import Thread


def client(c):
    while True:
        text = input("> ")
        method = text.split(" ")[0]
        newdict = {'method': method, 'params':{}}

        if method=='quit':
            c.send('{:10d}'.format(len(method.encode())).encode())
            c.send(method.encode())
            break

        elif method=='list':
            newdict['params']['arg'] = text.split(" ")[1]
            c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
            c.send(json.dumps(newdict).encode())

        elif method=='save':
            name = text.split(" ")[1]
            newdict['params']['name'] = name
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
            c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
            c.send(json.dumps(newdict).encode())

        elif method=='detach':
            c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
            c.send(json.dumps(newdict).encode())
            
        elif method=='insert':
            newdict['params']['lon'] = float(input("lon: "))
            newdict['params']['lat'] = float(input("lat: "))
            newdict['params']['locname'] = input("location name: ")
            newdict['params']['title'] = input("title: ")
            newdict['params']['desc'] = input("description(optional): ")
            newdict['params']['catlist'] = input("categories: ").split(" ")
            newdict['params']['starttime'] = input("start time: ")
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
            newdict['ID'] = int(text.split(" ")[1])
            newdict['params']['lon'] = float(input("lon: "))
            newdict['params']['lat'] = float(input("lat: "))
            newdict['params']['locname'] = input("location name: ")
            newdict['params']['title'] = input("title: ")
            newdict['params']['desc'] = input("description(optional): ")
            newdict['params']['catlist'] = input("categories: ").split(" ")
            newdict['params']['starttime'] = input("start time: ")
            newdict['params']['endtime'] = input("end time: ")
            newdict['params']['timetoann'] = input("time to announce: ")
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
  
        time.sleep(0.1)            


def clientNotifier(c):
    while True:
        length = int(c.recv(10))
        reply = c.recv(length)
        reply = json.loads(reply.decode())
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
        if reply=="connection closed":
            break
    c.close()

c = socket(AF_INET, SOCK_STREAM)
c.connect(('127.0.0.1', 20445))

t = Thread(target=client, args=(c,))
t2 = Thread(target=clientNotifier, args=(c,))

t.start()
t2.start()
