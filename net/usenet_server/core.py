#-*- coding: utf-8 -*-
#
# Copyright (C) 2016 Maskaliova, Schroer, Zelnick.
# 
# All rights reserved. No part of this publication may be reproduced,
# distributed, or transmitted in any form or by any means, including
# photocopying, recording, or other electronic or mechanical methods,
# without the prior written permission of the publisher, except in the
# case of brief quotations embodied in critical reviews and certain other
# noncommercial uses permitted by copyright law.

# vim: number ts=4 sw=4 expandtab tw=76

from socket import *
from utils import *
import thread
import argparse
import commands
import utils

"""
establish a new connection with a client and spawn a thread to handle all requests with it.
"""
def connection_thread(socketlist):
	connectionSocket = socketlist[0]
	addr = socketlist[1]
	msg = connectionSocket.recv(1024).split('\n')

	print msg	
	if(validateLogin(msg) == False):		
		connectionSocket.send(getResponseMsg('UNAUTHORIZED'))
		connectionSocket.close()
		return
	else:
		username = msg[0].split()[1]
		print getResponseMsg('AUTHORIZED')
		connectionSocket.send(getResponseMsg('AUTHORIZED'))
		print 'Transmission Accepted. Logging In:' + username
	# loop forever while the user is logged in
	while(1):
		print 'Waiting for a request'
		raw = (connectionSocket.recv(1024))
		print raw
		if (raw == ""):
			print "Error: Client disconnected"
			connectionSocket.close()
			break
		msg = raw.split('\n')
		#if the request is corrupted
		if(validateMsg(msg) == False):
			connectionSocket.send(getResponseMsg('INVALID'))

		#if the user decides to log out
		elif(validateLogout(msg)==True):
			connectionSocket.send(getResponseMsg('PASS'))
			connectionSocket.close()
			break
		else:
			response = createResponse(msg, username)
			connectionSocket.send(response)
				
	print "end of transmission, thread now dies"

serverPort = 12000
parser = argparse.ArgumentParser(description='Option arguments to pass to server.')
parser.add_argument('-p', nargs=1, type=int, help='A port number to use.')

args = parser.parse_args()
if (args.p!= None):
    serverPort = (args.p[0])
#print args['p']
#print serverPort

#create TCP ? welcoming socket

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((gethostname(), serverPort))
print gethostname()
#server begins listening for incoming TCP requests


print 'The server is ready to receive'
serverSocket.listen(1)

#loop forever
while 1:


#	print 'Hello'
	#server waits on accept()
	#for incoming requests, new
	#socket created on return
	connectionSocket, addr = serverSocket.accept()
	socketlist = [connectionSocket, addr]
	
	thread.start_new_thread(connection_thread, (socketlist,))	
	#read bytes from socket (but no address as in UDP)


