from clwmail.utils.objectmaker import PyGenObjects, PyObject
from clwmail.model import Model

class MailModel (Model):
	''' The mail model for CLWMail. This extends from
		the generic Model class which contains the error
		maker as well as model functions which are common
		to all applications'''

	def __init__(self):
		super(MailModel,self).__init__()

	def getuserdetails(self, username, domain):
		''' Given a username and domain, 
			a unique combination in the system,
			this method retrieves a detail view,
			of the requested user.'''

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_mail_user_get_all(%s,%s);'''
		# Excute said query
		cursor = self.executequery(query, (username, domain))
		# Returns a single dynamically created
		# object
		userAll = PyObject(cursor,'UserAll')
		return userAll 

	def getuserholidays(self, username, domain):
		''' Given a username and domain, 
			a unique combination in the system,
			this method retrieves a all know holidays
			for the requested user.'''

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_holidays_show(%s,%s);'''
		# Excute said query
		cursor = self.executequery(query, (username, domain))
		# Returns a generator object
		userAll = PyGenObjects(cursor,'UserAll')
		return userAll 

	def getcurrentholiday(self, username, domain):
		''' Given a username and domain, 
			a unique combination in the system,
			this method retrieves the request user's
			current holiday message.'''

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_mail_holiday_message	(%s,%s) as message;'''
		cursor = self.executequery(query, (username, domain))
		# Returns a single dynamic object
		holiday = PyObject(cursor,'Holiday')
		return holiday 

	def manageholiday(self, mode=-1, username=None, domain=None, 
					  hstart=None, hend=None, b_default=False,
					  message='', id=-1):
		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_mail_holiday_manage	(%s,%s,%s,%s,%s,%s,%s,%s) 
				   AS	
						status;''' 

		# The result
		result = None
		cursor = self.executequery(query, (mode, username, domain, hstart,
										   hend, message, id, b_default))
		if not self.error:
			# Returns a single dynamic object
			result = PyObject(cursor,'Result')

		return result


	def getholiday(self, hol_id, userid, domain):

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_mail_holiday_get_all	(%s, %s, %s)''' 

		# The result
		result = None
		# Excute said query
		cursor = self.executequery(query, (hol_id, userid, domain))
		if not self.error:
			# Returns a single dynamic object
			result = PyObject(cursor,'Holiday')

		return result


	def removeleave(self, mode=-1, username=None, domain=None, 
					  hstart=None, hend=None,
					  message='', id=-1):
		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_holiday_manage	(%s,%s,%s,%s,%s,%s,%s) as status;''' 
		# The result
		result = None
		cursor = self.executequery(query, (mode, username, domain, hstart, hend, message, id))
		if not self.error:
			# Returns a single dynamic object
			result = PyObject(cursor,'Leave')

		return result
