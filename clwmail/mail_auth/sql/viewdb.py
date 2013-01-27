from clwmail.utils.objectmaker import PyGenObjects, PyObject
from clwmail.model import Model

class AuthModel (Model):
	''' The authentication model for CLWMail. This extends from
		the generic Model class which contains the error
		maker as well as model functions which are common
		to all applications'''

	def __init__(self):
		super(AuthModel,self).__init__()

	def login(self, username, password):
		''' This method checks to see if the
			username (userid@domain) and password
			is found in the db '''

		query = '''SELECT 
						* 
				   FROM 
						fn_mail_user_get_login(%s,%s);'''
		cursor = self.executequery(query, (username, password))
		user = None
		if not self.error:
			user = PyObject(cursor,'User')
			
		return user

	def has_permission(self, userid, domain):
		''' This method checks to see if the
			user has permission to see a page'''

		query = '''SELECT 
						* 
				   FROM 
						fn_permission_check(%s,%s) as has_perm;'''
		cursor = self.executequery(query, (username, domain))
		has_perm = False
		if not self.error:
			user = PyObject(cursor,'User')
			has_perm = user.has_perm
			
		return has_perm 
