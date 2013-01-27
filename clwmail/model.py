from clwmail.utils.objectmaker import PyGenObjects, PyObject
from clwmail.utils.clwconnection import CLWConnection
import psycopg2

class Model (object):
	'''The generic model object. It is a database wrapper class which makes
	calls to the database using the psycopg2 python module. If an error is
	created it stored in as a variable that is accessible via the instance 
	of the model object.'''

	def __init__(self):
		''' The constructor allowing for
			error messages. '''

		# The error message
		self.error = None

	def executequery (self, query, params = None):
		''' This method executes a given
		query with the passed parameters. If an
		error occurs it is stored as an attribute
		which is accessible from the instance. A successfull
		query is always followed by a database commit and 
		any failures cause an immidiate rollback ''' 

		# Get connection singleton
		connection = CLWConnection()
		# Create a new cursor object.
		cursor = connection.cursor()
		# Reset error
		self.error = None
		# Excute said query
		try:
			if params:
				cursor.execute(query,params)
			else:
				cursor.execute(query)
		except (psycopg2.ProgrammingError, psycopg2.InternalError, psycopg2.DataError), err:
			# An error causes a rollback
			cursor.connection.rollback()
			# Set the error
			self.error = str(err)
		else:
			# Success causes a commit
			cursor.connection.commit()

		# return the cursor containing
		# the result
		return cursor

	def getuser(self, userid, domain):
		''' This method retrieves a  
			specific user ''' 

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_mail_user_get_all(%s, %s);'''

		# Excute said query
		cursor = self.executequery(query, (userid, domain))
		# The result
		user = None
		if not self.error:
			# Returns a generator dynamically created
			# object
			user = PyObject(cursor,'User')

		return user; 
