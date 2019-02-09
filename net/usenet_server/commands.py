import os.path
import os
from threading import Thread, Lock
from time import *
group_file = "var/groups"
group_dir = "var/"
#class Request():
mutex = Lock()
mutex_sub = Lock()
"""
Returns a list of all groups as well as if a user is subscribed to them
"""
def getGroupList(username=None):
	grouplist=[]
	#open group file
	f = open(group_file)	
	#split file into list using readlines
	sf = f.read().split('\n')
	print sf	
	for i in range(0, len(sf)-1):
		#further split each line
		linesplit = sf[i].split(":")
		# get the group name from the current line
		group = []
		group.append(linesplit[0])
		group.append(linesplit[1])
		group.append(False)
		# get the list of subscribed users from this group
		#if(len(linesplit) == 3):
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

	payload = 'content-length: ' + str(strlen) + ' bytes\n' + 'line-count: ' + str(strlines) + ' lines\n' + '\r\n\r\n' + groupstring

	return payload


"""
Store the contents of a post into the groups folder
"""
def writePost(msg):

	#get the seperate parts of the group
	group = msg[0].split()[1].split('.')
	path = os.path.abspath(group_dir) + '/' # absolute path 
	fd = None # file descriptor

	# create file path to group	
	for i in range(0, len(group)):
		path += str( group[i] )
		path += str( "/" )

	print path

	if(os.path.isdir(path) == False):
		return False

	post_subject = msg[1].split(':')[1]
	post_hash = getHash(post_subject)
	path += str(post_hash)
	mutex.acquire()
	try:
		#prepare to write to post
		fd = open(path, "a+")
		#get old posts first
		old_posts = fd.readlines()
		fd.close()
	
		#overwrite current file so that the newest post is on top
		fd = open(path, "w")
		#write payload to file
		fd.write('Group: ' + '.'.join(group) + '\n')
		fd.write('Subject: ' + post_subject + '\n')
		fd.write('\n'.join(msg[6:len(msg)]))
		if(old_posts != []):
			fd.write('\n\n')
		#write in old posts
		fd.write(''.join(old_posts))
	
		fd.close()
		return True
	finally:
		mutex.release()

def getHash(post_subject):
	return hex(hash(post_subject)%757)

def readPost(group, posthash):
	mutex_sub.acquire()
	try:
		if (isGroup(group) < 0):
			return -2
	finally:
		mutex_sub.release()
		path = os.path.abspath(group_dir) + '/'	
		path += '/'.join(group.split('.')) + '/'
		path += posthash
		mutex.acquire()
	try:
		nlines = 0
		nbytes = 0
		payload = ""
		with open( path, "r" ) as fd:
			for line in fd:
				payload += line
				nbytes  += len( line )
				nlines  += 1

		payload = 'post-subject:' + group + '\n' +\
			  '#-bytes:'	  + str(nbytes) + '\n' +\
			  'line-count:'   + str(nlines) + '\n'+\
			  '\r\n\r\n' +\
              payload
		return payload
	except IOError:
		return -2
	finally:
		mutex.release()
	
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
		current = grouplist[mid].split(':')[0]
		if(group == current):
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
	
	mutex_sub.acquire()
	try:
		fd = open(group_file)

		#perform binary search to find group
		grouplist = fd.read().split('\n')
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
	
		fd = open(group_file, "w")
		fd.writelines('\n'.join(grouplist))
		fd.close()

		return 0
	except IOError:
		return -1
	finally:
		mutex_sub.release()

def unsubscribe(username, group):
	mutex_sub.acquire()
	try:
		fd = open(group_file)
		#perform binary search to find group
		grouplist = fd.read().split('\n')

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
				#print userlist[i]
				if(userlist[i] == username):
					haveuser = True 
					break
		if(haveuser == False):
			return -2
	

		del userlist[i]
		current[2] = ','.join(userlist)
		grouplist[mid] = ':'.join(current)	
		fd.close()
	
		fd = open(group_file, "w")
	
		fd.writelines('\n'.join(grouplist))
		fd.close()

		return 0
	except IOError:
		return -1
	finally:
		mutex_sub.release()



def printPostList(group):
	postlist = []

	path = os.path.abspath(group_dir) + '/'	
	path += '/'.join(group.split('.')) + '/'	
	if(os.path.isdir(path) == False):
		return -1
	posts = os.listdir(path)
	postcount = 0
	mutex.acquire()
	try:
		for i in range(0, len(posts)):
			current = path + posts[i]
			if(os.path.isfile(current) == True):		
				fd = open(current, "r")
				lines = fd.read().split('\n')
				group = lines[1].split(': ')[1]
				dateline = lines[3].split(': ')
				print dateline
				date = dateline[1]
				stamp = mktime\
						(strptime(date, "%a, %b %d %H:%M:%S %Y"))
				postlist.append([group, date, stamp ])		
	except IOError:
		return -2
	finally:
		mutex.release()
	return formatPostList(postlist)
def formatPostList(postlist):
	poststring = ""
	sortedlist = sorted(postlist, key=getKey)
	for i in range(0, len(sortedlist)):
		poststring +=	'( '			  +\
				getHash(sortedlist[i][0]) +\
				', N, '			  +\
				sortedlist[i][1]	  +\
				', '			  +\
				sortedlist[i][0]	  +\
				' )\n'
	#print sortedlist
	return poststring

def getKey(item):
	return item[2]
