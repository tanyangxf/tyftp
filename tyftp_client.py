#!/usr/bin/env python
import socket
import os
import time
HOST = "localhost"
PORT = 9999
BUFFSIZE = 1024
TYsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
TYsock.connect((HOST,PORT))

def GetFromServer(file_name) :
	with open(file_name,'wb+') as f :
		while True :
			file_data = TYsock.recv(BUFFSIZE)
			if file_data == 'EOF' :
				break
			f.write(file_data)

def SendToServer(file_name) :
	TYsock.send('OK')
	file_data = file(file_name, 'rb+').read()
	TYsock.sendall(file_data)
	time.sleep(0.5)
	TYsock.send('EOF')
		

TYsock.send('auth')
while True :
	if TYsock.recv(BUFFSIZE) == 'Username' :
		print "Please input your username"
		while True :
			username = raw_input('Username> ').strip()
			if len(username) == 0 :
				continue
			else :
				break
		TYsock.send(username)
		if TYsock.recv(BUFFSIZE) == 'correct' :
			print "Welcome to login tyftp"
			break
		else :
			print "Your account or password is incorrect"
			continue

while True :
	user_input = raw_input('tyftp>').strip()
	if len(user_input) == 0 :
		continue
	elif user_input == 'exit' : 
		TYsock.close()
		break
	elif user_input == 'quit' : 
		TYsock.close()
		break
	elif user_input == 'get' or user_input == 'send' :
		print "No file specified,use %s file_name" % user_input
		continue
	else :
		try :
			file_name = user_input.split()[1]
		except IndexError :
			print "Invalid command"
			continue
	try :
		TYsock.send(user_input)
		file_status = TYsock.recv(BUFFSIZE)
		if file_status == 'server_send' :
			GetFromServer(file_name)
			print "file %s get done" % file_name
		elif file_status == 'server_get' :
			SendToServer(file_name)
			print "file %s send done" % file_name
		else :
			print file_status
	except IOError :
		print "No such file or directory"
TYsock.close()
