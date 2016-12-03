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
	if ( (msg == None) or (checkRequest(msg[0]) < 0)):
		return False
	retlist = []
	valid = False
	for i in range(1, len(msg)):
		if (msg[i] == version):
			valid=True
			break		
	#print retlist
	#if (valid == False):
	#	return False
	return valid	

"""
Validates a POST request
"""
def validatePost(msg):
	#split the msg up
	msglist = msg.split('\n')
	#read the first element of the list
	#should contain POST, the username, and the version number
	header = msglist[0].split()
	if(len(header) != 3 or header[0] != 'POST' or header[2] != version):
		return False
	subject = msglist[1].split(':')
	if(len(subject) != 2 or subject[0] != 'post-subject'):
		return False
	count = msglist[2]
	if(len(count) != 2 or count[0] != '#-bytes' or count[1].isdigit==False):
		return False
	line = msglist[3]
	if(len(line) != or line[0] != 'line-count' or line[1].isdigit==False):
		return False	
	if(msglist[4] != "\r"):
		return False
	if (msglisg[5] != "\r"):
		return False
	body = msglist[6]
	#check if payload has same number of lines as 
	if ( (len(msglist) - 6) != int(line[1])



def getResponseMsg(response,payload=None):
	msg = []
	msg.append(version)
	options={'AUTHORIZED': ['710', 'AUTHORIZED'],
		'UNAUTHORIZED': ['720', 'UNAUTHORIZED'],
		'EGID': ['810', 'EGID'],
		'EPID': ['820', 'EPID'],
		'SUBSCRIBE': ['830', 'SUBSCRIBE'],
		'UNSUBSCRIBE':['840', 'UNSUBSCRIBE'],
		'PASS': ['910', 'PASS',]
	}
	msg.extend(options[response])

	ret = ' '.join(msg)
	if (payload != None):
		ret+='\n' + payload
	return ret
		
def checkRequest(request):
	if(request == "LOGIN"
	or request == "SUBSCRIBE"
	or request == "UNSUBSCRIBE"
	or request == "LIST" 
	or request == "READ"
	or request == "POST"
	or request == "MARK"
	or request == "HELP"
	or request == "LOGOUT"):
		return 0
	else:
		return -1

def parseMsg(msg, username = None):
	command = msg[0]
	if (command == 'HELP'):
		payload = printHelp()
	if (command == 'LIST'):
		payload = printGroupList(username)	

	return payload	




