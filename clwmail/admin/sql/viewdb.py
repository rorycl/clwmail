from clwmail.utils.objectmaker import PyGenObjects, PyObject
from clwmail.model import Model

class AdminModel (Model):
	''' The admin model for CLWMail. This extends from
		the generic Model class which contains the error
		maker as well as model functions which are common
		to all applications'''

	def __init__(self):
		super(AdminModel,self).__init__()

	def manageuser(self, params):
		''' This method manages all
			users that are not admins ''' 

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_user_manage(%(mode)s, %(userid)s, %(domain)s,
											%(password)s, %(home)s,
											%(uid)s, %(gid)s, 
											%(typer)s, %(role)s, %(fullname)s, 
											%(notes)s, %(status)s) as result'''
		# Excute said query
		cursor = self.executequery(query, params)
		# The result
		managed = False 
		# Check there was no error
		if not self.error:
			# Returns True or false as result 
			user = PyObject(cursor,'User')
			managed = user.result

		return managed; 

	def getallusers(self):
		''' This method retrieves all
			users that are not admins ''' 

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_mail_get_user_list();'''

		# Excute said query
		cursor = self.executequery(query)
		# The result
		all_users = None
		if not self.error:
			# Returns a generator dynamically created
			# object
			all_users= PyGenObjects(cursor,'AllUsers')

		return all_users; 


	def getalldomains(self):
		''' This method retrieves all
			available domains ''' 

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_mail_get_domain_list();'''

		# Excute said query
		cursor = self.executequery(query)
		# The result
		all_domains = None
		if not self.error:
			# Returns a generator dynamically created
			# object
			all_domains = PyGenObjects(cursor,'AllDomains')

		return all_domains; 


	def managedomain(self,params):
		''' This method retrieves all
			available domains ''' 

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_domain_manage(%(mode)s,%(domainname)s,
										 %(newdomainname)s) as result;'''

		# Excute said query
		cursor = self.executequery(query, params)
		# The result
		managed = False 
		if not self.error:
			# Returns a generator dynamically created
			# object
			domain = PyObject(cursor,'Domain')
			managed = domain.result

		return managed

	def getdomain(self, domain_name):
		''' This method retrieves all
			available domains ''' 

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_domain_get_all(%s);'''

		# Excute said query
		cursor = self.executequery(query, (domain_name, ))
		# The result
		domain = None 
		if not self.error:
			# Returns a generator dynamically created
			# object
			domain = PyObject(cursor,'Domain')

		return domain 

	def getallaliases(self):

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_mail_get_alias_list();'''
		# Excute said query
		cursor = self.executequery(query)
		# The result
		all_aliases = None
		# Check there are no errors
		if not self.error:
			# Returns a generator dynamically created
			# object
			all_aliases = PyGenObjects(cursor,'AllAliases')


		return all_aliases; 

	def getalias(self, alias, domain):

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_alias_get_all(%s, %s);'''

		# Excute said query
		cursor = self.executequery(query, (alias, domain))
		# The result
		alias = None
		if not self.error:
			# Returns a generator dynamically created
			# object
			alias = PyObject(cursor,'Alias')

		return alias; 

	def getaliasusers(self, alias, domain):

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_mail_alias_resolve(%s, %s);'''

		# Excute said query
		cursor = self.executequery(query, (alias, domain))
		# The result
		aliasusers = None
		if not self.error:
			# Returns a generator dynamically created
			# object
			aliasusers = PyGenObjects(cursor,'AliasUsers')

		return aliasusers; 



	def managealias(self, params):

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_alias_manage(%(mode)s, %(alias)s, %(domain)s,
										%(new_alias)s, %(notes)s) as result;'''
		# Excute said query
		cursor = self.executequery(query, params)
		# The result
		managed = False 
		if not self.error:
			# Returns a single dynamically created
			# object
			alias = PyObject(cursor,'Alias')
			managed = alias.result

		return managed; 

	def managealiasuser(self, params):

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_alias_users_manage(%(mode)s, %(userid)s, %(alias)s,
											 %(domain)s) as result;'''
		# Excute said query
		cursor = self.executequery(query, params)
		# The result
		managed = False 
		if not self.error:
			# Returns a sing dynamically created
			# object
			aliasuser = PyObject(cursor,'Alias')
			managed = aliasuser.result

		return managed; 


	def getnondisabledusers(self, domain):

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_mail_everyone(%s);''' 
		# Excute said query
		cursor = self.executequery(query, (domain,))
		nondisabled = None

		if not self.error:
			# Returns a generator dynamically created
			# object
			nondisabled = PyGenObjects(cursor,'NonDisabled')

		return nondisabled; 

	def checkpass(self, password):
		''' This method retrieves all
			available domains ''' 

		# The query to execute
		query = '''SELECT 
						* 
				   FROM 
						fn_mail_pass_exists	(%s) as exists;'''

		# Excute said query
		cursor = self.executequery(query, (password, ))
		check = PyObject(cursor,'Bool')

		return check.exists; 

