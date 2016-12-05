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
from commands import *
version = 'USENET/0.8.1'
#group_requests = ['SUBSCRIBE', 'UNSUBSCRIBE']
#read_requests = 

"""
Wrapper class that calls various validation functions to see if a request is valid
"""
def validateMsg(msg):
	#print msglist	
	if ( (msg == None)):
		return False

	command = msg[0].split()[0]
	#print command
	if (checkRequest(command) == False):
		return False
	elif(command == 'POST' and validatePost(msg) == False):
		return False
	elif(command == 'READ' and validateRead(msg) == False):
		return False
	else:	
		return True	

"""
Validates a READ request
"""
def validateRead(msglist):
	return True


def validateLogout(msglist):
	if (msglist == None or len(msglist) != 4 or msglist[1] != '\r' \
	or msglist[2] != '\r'):
		return False
	command = msglist[0].split()
	if ( command==None or len(command) != 2 or command[0]!='LOGOUT'\
	or command[1] != version):
		return False
	else:
		return True


"""
Validates a LOGIN request
"""
def validateLogin(msglist):
	if (msglist == None or len(msglist) != 4 or msglist[1] != '\r' \
	or msglist[2] != '\r'):
		return False
	command = msglist[0].split()
	if ( command==None or len(command) != 3 or command[0]!='LOGIN'\
	or command[2] != version):
		return False
	else:
		return True

"""
Validates a POST request
"""
def validatePost(msglist):
	#read the first element of the list
	#should contain POST, the username, and the version number
	header = msglist[0].split()
	if(len(header) != 3 or header[0] != 'POST' or header[2] != version):
		return False
	subject = msglist[1].split(':')
	if(len(subject) != 2 or subject[0] != 'post-subject'):
		return False
	count = msglist[2].split(':')
	if(len(count) != 2 or count[0] != '#-bytes' or count[1].isdigit==False):
		return False
	line = msglist[3].split(':')
	if(len(line) != 2 or line[0] != 'line-count' or line[1].isdigit==False):
		return False	
	if(msglist[4] != "\r"):
		return False
	if (msglist[5] != "\r"):
		return False
	#check if payload has same number of lines as 
	lines = int(line[1])
	byte = int(count[1])
	if ( (len(msglist) - 6) != lines ):
		return False
	body = ''.join(msglist[6:len(msglist)])
	if( len(body) != (byte - lines + 1) ):
		print len(body)
		return False

	return True

def getResponseMsg(response,payload=None):
	msg = []
	msg.append(version)
	options={'AUTHORIZED': ['710', 'AUTHORIZED'],
		'UNAUTHORIZED': ['720', 'UNAUTHORIZED'],
		'EGID': ['810', 'EGID'],
		'EPID': ['820', 'EPID'],
		'SUBSCRIBE': ['830', 'SUBSCRIBE'],
		'UNSUBSCRIBE':['840', 'UNSUBSCRIBE'],
		'INVALID' : ['890', 'INVALID'],
		'PASS': ['910', 'PASS']
	}
	msg.extend(options[response])

	ret = ' '.join(msg)
	if (payload != None):
		ret+='\n' + payload
	return ret
		
def checkRequest(request):
	if(request == "LOGIN"
	or request == "GROUP"
	or request == "SUBSCRIBE"
	or request == "UNSUBSCRIBE"
	or request == "LIST" 
	or request == "READ"
	or request == "POST"
	or request == "MARK"
	or request == "HELP"
	or request == "LOGOUT"):
		return True
	else:
		return False


def createResponse(msg, username=None):
	command = msg[0].split()[0]
	if(command == 'POST'):
		if(writePost(msg) == False):
			return getResponseMsg('EPID')
		else:
			return getResponseMsg('PASS')
	elif(command == 'GROUP'):
		response = printGroupList(username)
		return getResponseMsg('PASS', response)		
	elif(command == 'READ'):
		group = msg[0].split()[1]
		subject ='_'.join(msg[1].split(':'[1].split())) 
		response = readPost(group, subject)
		if (response == False):
			return getResponseMsg("EPID")
		else:	
			return getResponseMsg('PASS', response)
	elif(command == 'LIST'):
		return getResponseMsg("EGID")
	elif(command == 'SUBSCRIBE'):
		groupid = msg[0].split()[1]
		response = subscribe(username, groupid)
		if(response==-1):
			return getResponseMsg("EGID")
		elif(response==-2):
			return getResponseMsg("SUBSCRIBE")
		else:
			return getResponseMsg("PASS")
	elif(command == 'UNSUBSCRIBE'):
		groupid = msg[0].split()[1]
		response = unsubscribe(username, groupid)
		if(response==-1):
			return getResponseMsg("EGID")
		elif(response==-2):
			return getResponseMsg("UNSUBSCRIBE")
		else:
			return getResponseMsg("PASS")

