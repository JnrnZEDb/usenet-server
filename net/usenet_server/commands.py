import os.path
import os
group_file = "var/groups"
group_dir = "var/"
#class Request():
global mutex_lock 
"""
Returns a list of all groups as well as if a user is subscribed to them
"""
def getGroupList(username=None):
	grouplist=[]
	#open group file
	f = open(group_file)	
	#split file into list using readlines
	sf = f.read().split('\n')
	
	for i in range(0, len(sf)):
		#further split each line
		linesplit = sf[i].split(":")
		# get the group name from the current line
		group = []
		group.append(linesplit[0])
		group.append(linesplit[1])
		# get the list of subscribed users from this group
		userlist = linesplit[2].split(",")
		# initially assume user is not subscribed to this group		group.append(False)
		for j in range(0, len(userlist)):
			# check if user is subscribed to group
			if(userlist != None \
 			and userlist[j] == username):
				group[2] =True
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
		#check if this group was subscribed to
		subscribed = group[len(group)-1]
		if (subscribed == True):
			groupstring += '( s, '
		else:	
			groupstring += '( ~, '
		#add the number of posts
		groupstring += grouplist[i][1] + ', '
		#add the name of the group
		groupstring+= grouplist[i][0]
		# add a new line
		groupstring += ' )'
		if (i != len(grouplist)-1):
			groupstring += '\n'
	
	strlen = len(groupstring)
	strlines = len(grouplist)

	payload = '#-bytes: ' + str(strlen) + '\n' + 'line-count: ' + str(strlines) + '\n' + '\r\n\r\n' + groupstring

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
	raw_subject = msg[1].split(':')[1].split()
	post_subject = '_'.join(raw_subject)
	path+= post_subject
	fd = open(path, "a")
	#write payload to file
	fd.write('\n'.join(msg[6:len(msg)]))
	
	fd.close()
	return True



def readPost(group, subject):
	if (isGroup(group) == False):
		return False
	path = os.path.abspath(group_dir)	
	path += '/'.join(group.split('.')) + '/'
	path += subject
	if (os.path.isfile(path) == False):
		return False
	try:
		fd = open(path, "r")
	except IOError:
		return False
	post = fd.readlines
	lines = str(len(post))
	poststring = '\n'.join(post)
	numbytes = str(len(poststring))
	payload = 'post-subject:'+group+'#-bytes:'+lines+'line-count:'+numbytes+'\r\n\r\n'+poststring
	
	return payload		
def isGroup(group=None):
	if (group == None):
		return -1
	fd = open(group_file, "r")
	grouplist = fd.readlines()
	
	hi = len(grouplist)-1
	lo = 0
	while(True):
		if (hi<lo):
			return -1
		mid = int((hi+lo)/2)
		print mid
		current = grouplist[mid].split(':')[0]
		print current
		if(group == current):
			print 'success'
			return mid
		elif(group < current):
			hi = mid
			lo = lo
		else:
			hi = hi
			lo = mid + 1

"""
Subscribe a specific user to a specific group
"""
def subscribe(username, group):
	try:
		fd = open(group_file)
	except IOError:
		return -1	

	#perform binary search to find group
	try:
		grouplist = fd.read().split('\n')
	except IOError:
		return -1
	mid = isGroup(group)
	if (mid < 0):
		return -1	
	current = grouplist[mid].split(':')
	userlist = current[2].split(',')
	# if userlist is empty, we're dealing with 0 or 1 entries.

	if(userlist == ['']):
		userlist = []
	else:
		for i in range(0, len(userlist)):
			if(userlist[i] == username):
				return -2	

	userlist.append(username)
	current[2] = ','.join(userlist)
	grouplist[mid] = ':'.join(current)	
	fd.close()
	
	try:
		fd = open(group_file, "w")
	except IOError:
		print 'Error from second open'
		return -1
	
	fd.writelines('\n'.join(grouplist))
	fd.close()

	return 0

def unsubscribe(username, group):
	try:
		fd = open(group_file)
	except IOError:
		return -1	

	#perform binary search to find group
	try:
		grouplist = fd.read().split('\n')
	except IOError:
		return -1
	mid = isGroup(group)
	if (mid < 0):
		return -1	
	current = grouplist[mid].split(':')
	userlist = current[2].split(',')
	haveuser = False
	if(userlist == ['']):
		return -2
	else:
		for i in range(0, len(userlist)):
			print userlist[i]
			if(userlist[i] == username):
				haveuser = True 
				break
	if(haveuser == False):
		return -2
	

	del userlist[i]
	current[2] = ','.join(userlist)
	grouplist[mid] = ':'.join(current)	
	fd.close()
	
	try:
		fd = open(group_file, "w")
	except IOError:
		print 'Error from second open'
		return -1
	
	fd.writelines('\n'.join(grouplist))
	fd.close()

	return 0

	return None

