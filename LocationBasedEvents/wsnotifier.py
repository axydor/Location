#!/usr/bin/python3

import sys
import os
from socket import *
import asyncio
import websockets
import logging
import json
from threading import Thread


## Uncomment following to use session_keys from django.
## This way request authentication will be
## achieved. similarly CSRF token can be used as
## authentication as well.

#import django
#from django.contrib.session.models import Session
#
#def setupDjango(projectpath, projectname):
#	'''call this once to setup django environment'''
#	sys.path.append(projectpath)
#	os.environ.setdefault('DJANGO_SETTINGS_MODULE',projectname + '.settings')
#	django.setup()
#
#def checksession(sessionkey):
#	'''check UDP/WS supplied id againts django session keys
#	   for browser, 'sessionid' cookie will save this id
#	   for django view request.session.session_key gives this id.
#		simply view sends udp notifications with request.session.session_key and
#		browser sends sessionid cookie. Note that they don't need to match.
#		User A can send notification to user B. But both have session ids.
#	'''
#	try:
#		Session.objects.get(session_key=sessionkey)
#		return True
#	except:	
#		return False

class Notifications:
	'''An observer class, saving notifications and notifiying
		registered coroutines'''
	def __init__(self):
		self.observers = {}
		self.messages = {}

	def register(self, cond, cid):
		'''register a Lock and an id string'''
		if cid in self.observers:
			self.observers[cid].add(cond)
		else:
			self.observers[cid] = set([cond])
		print(self.observers)

	def unregister(self, cond, cid):
		'''remove registration'''
		if cid not in self.observers:
			return
		self.observers[cid].discard(cond)
		if self.observers[cid] == set():
			del self.observers[cid]
		print(self.observers)

	def addNotification(self, oid, message):
		'''add a notification for websocket conns with id == oid
			the '*' oid is broadcast. Message is the dictionary
			to be sent to connected websockets.
		'''
		mt = [0, message]
		if oid == '*':     # broadcast message
			for oid in self.observers:
				mt[0] += len(self.observers[oid])  # increment reference count
				if oid in self.messages:
					self.messages[oid].append(mt)
				else:
					self.messages[oid] = [mt]	
				print('addnotification * ',self.messages)
				for c in self.observers[oid]:
					c.release()
		elif oid in self.observers:
			mt[0] += len(self.observers[oid])
			if oid in self.messages:
				self.messages[oid].append(mt)
			else:
				self.messages[oid] = [mt]
			print('addnotification',self.messages)
			for c in self.observers[oid]:
				c.release()


	def newmessages(self, oid):
		'''returns a list of messages for the connection with id==oid'''
		ret = []
		if oid not in self.messages:
			return "[]"
		for mt in self.messages[oid]:
			ret.append(mt[1])
			mt[0] -= 1
			if mt[0] == 0:
				self.messages[oid].remove(mt)
				if self.messages[oid] ==[]:
					del self.messages[oid]

		print(ret, self.messages)
		return json.dumps(ret)
	
# initialize a global notifications object
notifications = Notifications()

class GetNotifications:
	''' Class for getting notifications as udp packets'''
	def connection_made(self, transport):
		self.transport = transport
		print("Starting UDP server")

	def datagram_received(self, data, addr):
		try:
			mess = json.loads(data.decode())
		except:
			print('Cannot parse {}\n'.format(data.decode()))
			self.transport.sendto(b'cannot parse', addr)
			return
		notifications.addNotification(mess['id'], mess)
		print('Received %r from %s' % (mess, addr))

		
@asyncio.coroutine 
def websockethandler(websocket, path):
	''' function sending notifications to browsers
        it expects browser to send an identification string
		later all notifications for this id will be sent to
		the browser'''
	myid = yield from websocket.recv()
	print('connected', myid)
	mycond = asyncio.Lock()
	notifications.register(mycond, myid)
	try:
		while True:
			yield from mycond.acquire()
			with (yield from mycond):
				yield from websocket.send(notifications.newmessages(myid))
	except:
		pass
	finally:
		print('closing', myid)
		notifications.unregister(mycond, myid)
		websocket.close()

#enable logging
logging.basicConfig(level=logging.DEBUG)

try:
	# normalize user supplied addresses and validate
	udp_addr = sys.argv[1].split(':',1)
	if udp_addr[0] == '' : udp_addr[0] = '0'
	udp_addr = getaddrinfo(udp_addr[0], udp_addr[1], AF_INET, SOCK_DGRAM)
	udp_addr = udp_addr[0][4]

	ws_addr = sys.argv[2].split(':',1)
	if ws_addr[0] == '' : ws_addr[0] = '0'
	ws_addr = getaddrinfo(ws_addr[0], ws_addr[1], AF_INET, SOCK_STREAM)
	ws_addr = ws_addr[0][4]
except Exception as e:
	sys.stderr.write("{}\nusage: {} udpip:port wsip:port\n".format(e, sys.argv[0]))
	sys.exit()



## Following creates a UDP handler
loop = asyncio.get_event_loop()
loop.set_debug(True)
udplistener = loop.create_datagram_endpoint(
    	GetNotifications, local_addr=udp_addr )
# following creates a websocket handler
ws_server = websockets.serve(websockethandler, ws_addr[0], ws_addr[1], loop = loop)

#loop.run_until_complete(ws_server)
# start both in an infinite service loop
asyncio.async(ws_server)
loop.run_until_complete(udplistener)
loop.run_forever()
