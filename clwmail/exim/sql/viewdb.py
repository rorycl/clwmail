from clwmail.utils.objectmaker import PyGenObjects, PyObject
from clwmail.model import Model

class EximModel (Model):
	''' The exim model for CLWMail. This extends from
		the generic Model class which contains the error
		maker as well as model functions which are common
		to all applications. This class is not used in the
		web interface. This provideds a pythonic hook into 
	    the sql functions used by exim. These methods do 
		show in the test cases however.'''

	def __init__(self):
		super(EximModel,self).__init__()

	def setholidays(self):
		''' Given a username and domain, 
			a unique combination in the system,
			this method retrieves the leaver message
`			of said user.''' 

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_holidays_set() as result;'''
		# Excute said query
		cursor = self.executequery(query)
		result = None
		if not self.error:		
			# Returns a single dynamically created object
			holidayset = PyObject(cursor,'HolidaySetter')
			result = holidayset.result 

		return result 

	def getactiveuser(self, username, domain):
		''' Given a username and domain, 
			a unique combination in the system,
			this method retrieves the user if he is active.''' 

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_mail_user_get_active(%s,%s) as userid;'''
		# Excute said query
		cursor = self.executequery(query, (username, domain))
		activeuser = None
		if not self.error:		
			# Returns a single dynamically created object
			activeuser = PyObject(cursor,'ActiveUser')

		return activeuser 
		
	def getholidayeuser(self, username, domain):
		''' Given a username and domain, 
			a unique combination in the system,
			this method retrieves the user if he is on holiday.''' 

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_mail_user_get_holiday(%s,%s) as userid;'''
		# Excute said query
		cursor = self.executequery(query, (username, domain))
		holidayuser = None
		if not self.error:		
			# Returns a single dynamically created object
			holidayuser = PyObject(cursor,'ActiveUser')

		return holidayuser 

	def getleaveruser(self, username, domain):
		''' Given a username and domain, 
			a unique combination in the system,
			this method retrieves the user if he has left.''' 

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_mail_user_get_leaver(%s,%s) as userid;'''
		# Excute said query
		cursor = self.executequery(query, (username, domain))
		leaveuser = None
		if not self.error:		
			# Returns a single dynamically created object
			leaveuser = PyObject(cursor,'ActiveUser')

		return leaveuser 

	def getleavermessage(self, username, domain):
		''' Given a username and domain, 
			a unique combination in the system,
			this method retrieves the leaver message
`			of said user.''' 

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_mail_leaver_message(%s,%s) as leave_msg;'''
		# Excute said query
		cursor = self.executequery(query, (username, domain))
		message = None
		if not self.error:		
			# Returns a single dynamically created object
			leaver = PyObject(cursor,'Leaver')
			message = leaver.leave_msg

		return message 

	def manageleaver(self,params):
		''' Given a username and domain, 
			a unique combination in the system,
			this method manages the leaver aspect of a user''' 

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_user_leaver_manage(%(mode)s,%(userid)s,%(domain)s,%(leavedate)s,
											  %(message)s) as result;'''
		# Excute said query
		cursor = self.executequery(query, params)
		managed = False
		if not self.error:		
			# Returns a single dynamically created object
			leaver = PyObject(cursor,'Leaver')
			managed = leaver.result

		return managed 

	def manageactiveusers(self,params):
		''' Given a username and domain, 
			a unique combination in the system,
			this method manages the active users''' 

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_user_active_manage(%(userid)s,%(domain)s) as result;'''
		# Excute said query
		cursor = self.executequery(query, params)
		managed = False
		if not self.error:		
			# Returns a single dynamically created object
			activate = PyObject(cursor,'Activate')
			managed = activate.result

		return managed 
