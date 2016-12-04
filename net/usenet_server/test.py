from socket import *
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('localhost', 12000))

transmission = 'LOGIN test2 USENET/0.8.1\n\r\n\r\n'

clientSocket.send(transmission)
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

while(1):
	raw  = raw_input();
	if (raw == ""):
		clientSocket.send('LOGOUT USENET/0.8.1\n\r\n\r\n')
		clientSocket.close()
		break

	elif(raw== 'list'):
		clientSocket.send('LIST USENET/0.8.1\n\r\n\r\n')
		grouplist = clientSocket.recv(1024)
		print grouplist

	elif (raw == 'test'):
		transmission = 'HELP USENET/0.8.1\n\r\n\r\n'
		clientSocket.send(transmission)
		clientSocket.recv(1024)
	elif (raw == 'post'):
		clientSocket.send(post)
		print clientSocket.recv(1024)		
