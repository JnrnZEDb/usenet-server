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
	sf = f.readlines()
	
	for i in range(0, len(sf)):
		#further split each line
		linesplit = sf[i].split(":")
		# get the group name from the current line
		group = []
		group.append(linesplit[0])
		group.append(linesplit[1])
		# get the list of subscribed users from this group
		userlist = linesplit[2].split(",")
		# initially assume user is not subscribed to this group
		group.append(False)
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
		return False
	fd = open(group_file, "r")
	grouplist = fd.readlines()
	
	hi = len(grouplist)
	lo = 0
	while(True):
		if (hi<lo):
			return False
		mid = int((hi-lo)/2)
		if(group == grouplist[mid]):
			return True
		elif(group < grouplist[mid]):
			hi = mid
			lo = lo
		else:
			hi = hi
			lo = mid + 1


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

