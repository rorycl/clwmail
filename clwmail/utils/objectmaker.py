##################################################
# Author: Sebastian Ritter
# Date :  December 11 2007
##################################################

from new import classobj

def PyGenObjects (cursor, class_name):
	'''
		This method takes a connection cursor result sequence
		and yields the a dynamically created instance of the type passed to it. 
		Each dictionary's key,value pair
		corresponds to {'column name':row value }. '''

	# Get all returned rows from db query.
	count = cursor.rowcount

	if count > 0:
		return generator (cursor,class_name)
	else:
		cursor.close()
		return 

def generator(cursor, class_name):
  
		rows  = cursor.fetchall()
		# Go through each row  
		for i in range(cursor.rowcount):
			thisdict = {}
			for j in range(len(cursor.description)):
				# cursor.description[x][0] corresponds to the name of the xth column
				thisdict[cursor.description[j][0]]=rows[i][j]

			# yield the class instance of the row.
			# This is dynamically created
			yield  classobj(class_name, (object,), thisdict)()


		cursor.close()	

def PyObject (cursor, class_name):
	'''
		This method takes a connection cursor result sequence
		and yields the a dynamically created instance of the type passed to it. 
		Each dictionary's key,value pair
		corresponds to {'column name':row value }. '''

	# One Row
	try:
		row = cursor.fetchone()
	except:
		return None

	# A temp dictionary
	thisdict = {}

	for j in range(len(cursor.description)):
		# cursor.description[x][0] corresponds to the name of the xth column
		thisdict[cursor.description[j][0]]=row[j]

	# return the class instance of the row.
	# This is dynamically created
	return  classobj(class_name, (object,), thisdict)()
			

	cursor.close()	



