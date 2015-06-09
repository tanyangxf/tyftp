#!/usr/bin/env python
import SocketServer
import time
import os
import socket
HOST = ''
PORT = 9999
BUFFSIZE = 1024
class MyFtpHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		print '...connected from:', self.client_address
		if self.request.recv(BUFFSIZE) == 'auth':
			print 'User auth bengin'
			while True :
				self.request.send('Username')
				username = self.request.recv(BUFFSIZE)
				if username == 'ty' :
					self.request.send('correct')
					print 'Username %s is correct,welcome login to tyftp' % username
					break
				else :
					self.request.send('incorrect')
					print "Username %s is incorrect,connection is failed" % username
					continue

		def GetFromClient(file_name) :
			with open(file_name, 'wb+') as f :
				while True :
					file_data = self.request.recv(BUFFSIZE)
					if file_data == 'EOF' :
						break
					f.write(file_data)
		def SendToClient(file_name) :
			file_data = file(self.file_name,'rb+').read()
			self.request.sendall(file_data)
			time.sleep(0.5)
			self.request.send('EOF')

		while True :
			user_input = self.request.recv(BUFFSIZE).strip()
			try :
				self.cmd = user_input.split()[0]
				self.file_name = user_input.split()[1]
				if self.cmd == 'get' :
					try :
						os.stat(self.file_name)
					except OSError :
						msg = "'No such file or directory, %s' %file_name "
						self.request.send(msg)
					self.request.send('server_send')
					SendToClient(self.file_name)
				if self.cmd == 'send' :
					self.request.send('server_get')
					GetFromClient(self.file_name)
					
			except IndexError :
				print "Client %s logout " % self.client_address[0]
				break

if __name__ == "__main__" :
	try :
		FtpServer = SocketServer.ThreadingTCPServer((HOST,PORT),MyFtpHandler)
		print "Wait for client...."
		FtpServer.serve_forever()
	except socket.error,e :
		print "Ftp Server Socket Error!"
	except KeyboardInterrupt :
		print "Ftp Server closed!"

