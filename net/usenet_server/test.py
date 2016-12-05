from socket import *
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('localhost', 12000))

login = 'LOGIN test2 USENET/0.8.1\n\r\n\r\n'

clientSocket.send(login)
msg =  clientSocket.recv(1024)
print msg
post =  'POST comp.lang.c USENET/0.8.1\n'+\
	'post-subject:POSIX Threads\n'+\
	'#-bytes:145\n'+\
	'line-count:5\n'+\
	'\r\n'+\
	'\r\n'+\
	'Author: Rimack Zelnick\n'+\
	'Date: Tue, Nov 22 12:26:54 EST 2016\n'+\
	'\n'+\
	"How can I create a posix thread? What's the difference\n"+\
	'bewtween other implementations'
read =  "READ comp.lang.c USENET/0.8.1\n"+\
	"post-subject:POSIX Threads"
while(1):
	raw  = raw_input();
	if (raw == ""):
		clientSocket.send('LOGOUT USENET/0.8.1\n\r\n\r\n')
		clientSocket.close()
		break

	elif(raw== 'group'):
		clientSocket.send('GROUP USENET/0.8.1\n\r\n\r\n')
		grouplist = clientSocket.recv(1024)
		print grouplist

	elif (raw == 'test'):
		transmission = 'HELP USENET/0.8.1\n\r\n\r\n'
		clientSocket.send(transmission)
		clientSocket.recv(1024)
	elif (raw == 'post'):
		clientSocket.send(post)
		print clientSocket.recv(1024)
	elif (raw == 'read'):
		clientSocket.send(read)
		print clientSocket.recv(1024)		
