import os.path
import os
group_file = "var/groups"
group_dir = "var/"
#class Request():
global mutex_lock 
"""
Print out a help message for the client

return a help message for the client
"""
def printHelp():
	helpString = 'login <username>: Log in to Usenet with a username argument\n'+\
		'help: Display this helpful help message\n'+\
		'(the following commands can only be used once login)\n'+\
		'ag [N]: List the names of all existing group, N groups at a time.\n'+\
		'(If N is not given, will return 5 groups at a time)\n'+\
		'sg [N]: List the names of all subscribed groups, N groups at a time.\n'+\
		'(If N is not given, will return 5 groups at a time)\n'+\
		'rg <gname> [N]: Displays all posts in the group <gname>, N posts at a time.\n'+\
		' (If N is not given, will return 5 posts at a time)\n'+\
		'(using this option puts the user into rg mode, and only the following commands can be used\n'+\
		'[id]: A number between 1 and N denoting the post with the list of N posts to display\n'+\
		'r: mark a post as read\n'+\
		'n: List the next N posts\n'+\
		'p: post to the group\n'+\
		'q: exit from the rg command\n'+\
		'logout: logout from Usenet'
 	helpLen = len(helpString)
	linecount = 0
	for i in range(0, len(helpString)):
		if(helpString[i]=='\n'):
			linecount += 1


	payload = []
	payload.append('content-length:')
	payload.append(str(helpLen))
	payload.append('line-count:')
	payload.append(str(linecount))
	payload.append('\r\n\r\n')
	payload.append(helpString)
	
	return payload

"""
Returns a list of all groups as well as if a user is subscribed to them
"""
def getGroupList(username=None):
	grouplist=[]
	#open group file
	f = open(group_file)	
	#split file into list using readlines
	sf = f.readlines()
	
	for i in range(0, len(sf)):
		#further split each line
		linesplit = sf[i].split(":")
		# get the group name from the current line
		group = linesplit[0: len(linesplit)-1]
		# get the list of subscribed users from this group
		userlist = linesplit[len(linesplit)-1].split(",")
		# initially assume user is not subscribed to this group
		group.append(False)
		for j in range(0, len(userlist)):
			# check if user is subscribed to group
			if(userlist[j] == username):
				group[len(group)-1] =True
				break
			
		grouplist.append(group)

	return grouplist


"""
formats a list containing information about a group into a single string
that can be used as a payload to send to the client
"""
def printGroupList(username=None):
	grouplist = getGroupList(username)
	#create an empty string
	groupstring = ""
	#iteration through each entry in the list
	for i in range(0, len(grouplist)):
		#select the current element in the list
		group = grouplist[i]
		#add index number + 1
		groupstring += str(i+1) + '. '
		#check if this group was subscribed to
		subscribed = group[len(group)-1]
		if (subscribed == True):
			groupstring += '(s) '
		else:	
			groupstring += '( ) '
		#add the name of the group
		for j in range(0, len(group)-1):
			groupstring+= group[j]
			if (j != len(group)-2):
				groupstring += '.'
		# add a new line
		groupstring += '\n'
	
	strlen = len(groupstring)
	strlines = len(grouplist)

	payload = '# Bytes: ' + str(strlen) + '\n' + 'Line Count: ' + str(strlines) + '\n' + '\r\n\r\n' + groupstring

	return payload


"""
Store the contents of a post into the groups folder
"""
def writePost(msg):
	#get the seperate parts of the group
	group = msg[0].split()[1].split('.')
	startpath = os.path.abspath(group_dir) + '/' # absolute path 
	path = startpath #current path
	fd = None # file descriptor
	# create file path to group	
	for i in range(0, len(group)):
		path += group[i]
		path+= '/'
	print path
	if(os.path.isdir(path) == False):
		return False
	post_subject = msg[1].split(':')[1]
	path+= post_subject
	fd = open(path, "a")
	fd.write(msg[2]+'\r\n')	# #-bytes
	fd.write(msg[3]+'\r\n') # line-count
	fd.write(msg[4]+'\r\n')	# \r
	fd.write(msg[5]+'\r\n') # \r
	
	#payload
	for i in range(6, len(msg)):
		fd.write(msg[i])
		if(i != len(msg)-1):
			fd.write('\n')
	fd.write('\r\n')
	fd.close()
	return True











	#havesubgroup = False	# we are looking for a subgroup
		#dirlist = os.listdir(path) # look through directory
		#loop through current directory
		#for j in range(0, len(dirlist)):
		#	if (dirlist[j] == group[i]):
				#add to current path
		#		path += '/' + dirlist[j]
		#		havesubgroup = True #found a subgroup
		#		break
		#if(havesubgroup==False):
		#	print "Error: Group does not exist!"
		#	return False
		#if (i == len(group)-1):
		#	break

