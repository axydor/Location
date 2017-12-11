import json
from socket import * 

def client(port):
    # send n random request
    # the connection is kept alive until client closes it.
    c = socket(AF_INET, SOCK_STREAM)
    c.connect(('127.0.0.1', port))
    while True:
        text = input("> ")
        if text.split(" ")[0]=='insert':
            lon = float(input("lon: "))
            lat = float(input("lat: "))
            locname = input("location name: ")
            title = input("title: ")
            desc = input("description(optional): ")
            catstring = input("categories: ")
            catlist = catstring.split(" ")
            starttime = input("start time: ")
            endtime = input("end time: ")
            timetoann = input("time to announce: ")
            newdict = {'method':'insert', 'params':{}}
            newdict['params']['lon'] = lon
            newdict['params']['lat'] = lat
            newdict['params']['locname'] = locname
            newdict['params']['title'] = title
            newdict['params']['desc'] = desc
            newdict['params']['catlist'] = catlist
            newdict['params']['starttime'] = starttime
            newdict['params']['endtime'] = endtime
            newdict['params']['timetoann'] = timetoann
            c.send('{:10d}'.format(len(json.dumps(newdict).encode())).encode())
            c.send(json.dumps(newdict).encode())
            reply = c.recv(1024)
            print(c.getsockname(), reply)
    c.close()

client(20445)
