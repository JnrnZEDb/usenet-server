from socket import *
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('localhost', 12000))

transmission = 'LOGIN test2 USENET/0.8.1\r\n\r\n'

clientSocket.send(transmission)
msg =  clientSocket.recv(1024)
print msg
post = 'POST comp.os.usenet USENET/0.8.1\npost-subject:Test post\n#-bytes:15\nline-count:1\r\n\r\nHello, Usenet!'

while(1):
	raw  = raw_input();
	if (raw == ""):
		clientSocket.send('LOGOUT USENET/0.8.1\r\n\r\n')
		clientSocket.close()
		break

	elif(raw== 'list'):
		clientSocket.send('LIST USENET/0.8.1\r\n\r\n')
		grouplist = clientSocket.recv(1024)
		print grouplist

	elif (raw == 'test'):
		transmission = 'HELP USENET/0.8.1\r\n\r\n'
		clientSocket.send(transmission)
		clientSocket.recv(1024)
	elif (raw == 'post'):
		clientSocket.send(post)
		
