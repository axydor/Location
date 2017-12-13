import json
from socket import * 

def client(port):
    # send n random request
    # the connection is kept alive until client closes it.
    c = socket(AF_INET, SOCK_STREAM)
    c.connect(('127.0.0.1', port))
    while True:
        text = input("> ")
        method = text.split(" ")[0]
        newdict = {'method': method, 'params':{}}

        if method=='insert':
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
            reply = c.recv(1024)
            print(c.getsockname(), reply.decode())
        
        elif method=='delete':
            newdict['params']['ID'] = int(text.split(" ")[1])
            c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
            c.send(json.dumps(newdict).encode())
            reply = c.recv(1024)
            print(c.getsockname(), reply.decode())

        elif method=='findClosest':
            newdict['params']['lat'] = float(text.split(" ")[1])
            newdict['params']['lon'] = float(text.split(" ")[2])
            c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
            c.send(json.dumps(newdict).encode())

            length = int(c.recv(10))
            reply = c.recv(length)
            print(c.getsockname(), json.loads(reply.decode()))
            
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
            reply = c.recv(1024)
            print(c.getsockname(), reply.decode())
            
        elif method == "searchEvent":   # searchEvent,39.9,31,39.7,32.8,2017/11/27 19:00,+5 days,musical,opera
            newdict = {'method': method,'params':{}}
            rect = {}
            #rect={'lattl':39.9,'lontl':31,'latbr':39.7,'lonbr':32.8}
            if input("Rectangle:>") == 'None':
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
            if starttime == 'None':
                starttime = None
            if endtime == 'None':
                endtime = None
            if category == 'None':
                category = None
            if text == 'None':
                text = None
            newdict['params']['rectangle'] = rect
            newdict['params']['starttime'] = starttime
            newdict['params']['endtime']   = endtime
            newdict['params']['category']  = category
            newdict['params']['text']      = text
            c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
            c.send(json.dumps(newdict).encode())
            reply = c.recv(1024)
            print(c.getsockname(),reply)            
    c.close()

client(20445)
