import socket
import json
#import os
import threading
import time



class notifu(object):
	def __init__(self):
		#print "Create Notifu"
		self.c = None
		self.msgcallback = None
	def connect(self):
		#print "Connect"
		self.c = connection()
		#print "Set Connect Callback"
		self.c.setCallback(self.incomingJson);
	def login(self, user, pw):
		s = {}
		s["aktion"] = "autentifizierung"
		s["data"] = {}
		s["data"]["username"]=user
		s["data"]["secret"]=pw
		if(self.c!=None):
			#print "Send Autentification"
			self.c.sendLogin(json.dumps(s))
			return True
		return False
	def sendMessage(self, user, subject, text):
		s = {}
		s["aktion"] = "msg"
		s["data"] = {}
		s["data"]["username"]=user
		s["data"]["msg"]=text
		s["data"]["subject"]=subject
		if(self.c!=None):
			self.c.send(json.dumps(s))
			return True
		return False
	def startReading(self):
		#print "StartReading"
		self.c.connectReader()
	def setMessageCallback(self, c):
		#print "SetCallBack"
		self.msgcallback = c
		
	def stop(self):
		self.c.stop()
	def incomingJson(self, jsonmsg):
		#print "incoming JSON"
		detais = None
		try:
			detais = json.loads(jsonmsg)
		except:
			pass
			#print "Json fehler in:"
			#print jsonmsg
		if(detais!=None):
			if(detais["action"]=="msg"):
				if(self.msgcallback!=None):
					self.msgcallback(detais["data"]["subject"], detais["data"]["msg"])
		





class connection():
	def __init__(self):
		#print "Connection Start"
		ip = "tcp.notifu.schredder.pw"
		#ip = "127.0.0.1"
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((ip, 9005))
		self.c = connectionThread()
		self.c.setCallback(self.callback)
		#self.c.setSocket(self.s)
		self.cb = None
		self.reading = False
		#print "Create Write Socket"

		#print "Connection stable"
	def send(self, msg):
		#print "send MSG"
		self.s.send(msg)
	def connectReader(self):
		#print "Run Connection Thread"
		#self.c.setSocket(self.ss)
		self.c.start()
	def sendLogin(self, msg):
		self.s.send(msg)
		self.c.setLoginMsg(msg)
		time.sleep(1)
	def callback(self, msg):
		#print "Forwording MSG"
		if(self.cb!=None):
			self.cb(msg)
	def setCallback(self, c):
		self.cb = c
	def stop(self):
		self.c.stop()

class connectionThread(threading.Thread):
	def _init__(self):
		self.run = True
		self.c = None
		self.s = None
	def stop(self):
		#print "ENDE"
		self.run = False
	def setCallback(self, c):
		self.c = c
	def setSocket(self, s):
		self.s = s
	def setLoginMsg(self, msg):
		self.loginMSG = msg
	def run(self):
		ip = "tcp.notifu.schredder.pw"
		#ip = "127.0.0.1"
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		s.connect((ip, 9005))
		#s.send('{"aktion":"autentifizierung", "data" : {"username":"soeren", "secret":"bla"}}')
		s.send(self.loginMSG)
		#s.close()
		try: 
			while self.run: 
				#nachricht = raw_input("Nachricht: ") 
				#s.send(nachricht) 
				antwort = s.recv(1024) 
				##print antwort
				self.c(antwort)
		except:
			pass