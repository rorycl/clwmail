from django import forms
from django.forms import Field
from clwmail.admin.sql.viewdb import AdminModel 
from django.forms.util import ErrorList
from clwmail import settings
import re

# Get the valid types from settings
types = settings.TYPERS

class MultiSelectField (Field):
	''' This field ensures that a set of selections
		is made within a limited set of options '''

	def __init__(self,required =True, label="",initial="",widget=None,
				 help_text='', choices=[]):
			''' Constructor method '''

			# Call the parent constructor
			super(MultiSelectField,self).__init__(required=required, 
													 label =label, 
													 initial =initial, 
													 widget=widget, help_text=help_text)
			# The available choices
			self.choices = choices

	def clean(self, value):
		''' The validator method '''
		
		if not value:
			# Check that the value is required
			if self.required:
				raise forms.ValidationError('This field is required.')
			else:
				return None 

		if not type (value) == list:
			raise forms.ValidationError('A list of selections is required' )

		for item in value:
			found = False
			for choice in self.choices:
				if item.lower() == choice.lower():
					found = True
					break
			if not found:
				raise forms.ValidationError('An invalid choice has been made.' )

		return value

class MultipleOptionField (Field):
	''' This field ensures that a selection
		is made within a limited set of options '''

	def __init__(self,required =True, label="",initial="",widget=None,
				 help_text='', choices=[], b_spaces = True):
			''' Constructor method '''

			# Call the parent constructor
			super(MultipleOptionField,self).__init__(required=required, 
													 label =label, 
													 initial =initial, 
													 widget=widget, help_text=help_text)
			# The available choices
			self.choices = choices
			# If the choice is allowed to have spaces
			self.allowspaces = b_spaces

	def clean(self, value):
		''' The validator method '''
		
		if not value:
			# Check that the value is required
			if self.required:
				raise forms.ValidationError('This field is required.')
			else:
				return None 

		if not value in self.choices:
			raise forms.ValidationError('An invalid choice has been made.' )

		# Check there are no spaces in the entered choice
		elif not self.allowspaces and _hasspaces (value):
			raise forms.ValidationError('This field cannot contain spaces.' )

		else:
			return value

class UniqueField (Field):

    def __init__(self,required =True, label="",initial="",widget=None,
				 help_text='', max_length=None, others=[], exclude=None,
				 b_spaces=True):

			super(UniqueField,self).__init__(required=required, 
													 label=label, 
													 initial=initial, 
													 widget=widget, help_text=help_text)
			self.others = others
			self.max_length = max_length
			self.exclude = exclude 
			self.allowspaces = b_spaces 

    def clean(self, value):

		if not value:
			if self.required:
				raise forms.ValidationError('This field is required.')
			else:
				return None 

		if self.max_length and len(value) > self.max_length:
			raise forms.ValidationError('Please limit this field to %s characters.' % self.max_length)

		if (value.lower() in self.others):
			if self.exclude:
				if not value.lower() == self.exclude.lower():
					 raise forms.ValidationError('This value already exists.' )
			else:
				 raise forms.ValidationError('This value already exists.')
	

		# Check there are no spaces in the entered choice
		elif not self.allowspaces and _hasspaces (value):
			raise forms.ValidationError('This field cannot contain spaces.' )

		return value


class UserAdd(forms.Form):

	def __init__(self, kargs=None):
		super(UserAdd,self).__init__(kargs)
		self.model = AdminModel()
		self.extras = {}
		self.fields['domain'].choices = [domain.domainname for domain in self.model.getalldomains()]
		self.fields['typer'].choices = [typer for typer in types]




	fullname = forms.CharField(label="fullname", 
								 max_length=32,
								 min_length=3,
								 required=True)

	userid = forms.CharField(label="userid", 
								 max_length=64,
								 min_length=1,
								 required=True)

	password = forms.CharField(label="password", 
								 max_length=64,
								 required=True)
	
	role = forms.CharField(label="role", 
								 max_length=64,
								 required=False)
	
	domain = MultipleOptionField(label="Domain", required=True, choices=[],
								 b_spaces = False)

	typer = MultipleOptionField(label="type", required=True, choices=[])

	notes = forms.CharField(label="notes", required=False)

	def clean_userid (self):
		cleaned_data = super(UserAdd, self).clean()
		try:
			userid = cleaned_data['userid']
		except KeyError:
			pass
		else:
			if _hasspaces (userid):
				raise forms.ValidationError('This field cannot contain spaces.' )

			if not _validlocalpart (userid):
				raise forms.ValidationError('Please enter a valid userid.' )

			return userid


	def clean(self):
		cleaned_data = super(UserAdd, self).clean()

		try:
			value = cleaned_data['userid']
		except KeyError:
			pass
		else:
			if _validascii(value):
				self.checkusername(cleaned_data)

			# If any errors were picked up raise a validation error so that
			# the form does not validate.
			if self.extras:
				# This error message is generic as the only purpose is to
				# raise *an* error.
				raise forms.ValidationError('General Form Errors have occured.')

		return cleaned_data

	def _createError(self,key,error_message):

		errorList = ErrorList()
		errorList.append(error_message)
		self.extras[key] = errorList

	def checkusername(self, cleaned_data):
	
		try:
			userid = cleaned_data['userid']
			domain = cleaned_data['domain']
		except KeyError:
			# we dont worry about 
			# key error as it implies and error
			# has already been caught elsewhere
			pass 
		else:
			user = self.model.getuser(userid, domain)
			if user and user.userid:
				self._createError('userid','This user already exists.')
	
class UserEdit(UserAdd):
	def checkusername(self, cleaned_data):
		''' overload parent checkusername method. We dont
			want to check this anymore as the values sent to 
			the form are read only anyway and we risk checking the
			existance of the user against him/herself ''' 

		pass

class DomainAdd(forms.Form):

	def __init__(self, kargs=None):
		super(DomainAdd,self).__init__(kargs)
		self.model = AdminModel()
		self.fields['domain'].others = [domain.domainname for domain in self.model.getalldomains()]

	
	domain =UniqueField(label="Domain", required=True, max_length=128,
						others=[], b_spaces=False)

	def clean_domain (self):
		cleaned_data = super(DomainAdd, self).clean()
		try:
			domain = cleaned_data['domain']
		except KeyError:
			pass
		else:
			if not _validdomain (domain):
				raise forms.ValidationError('Please enter a valid domain.' )

			return domain


class DomainEdit(forms.Form):

	def __init__(self, domain_name, kargs=None):
		super(DomainEdit,self).__init__(kargs)
		self.model = AdminModel()
		self.fields['domain'].others = [domain.domainname for domain in self.model.getalldomains()]
		self.fields['domain'].exclude = domain_name

	domain = UniqueField(label="Domain", required=True, max_length=128,
						 others=[], b_spaces=False)
	
	def clean_domain (self):
		cleaned_data = super(DomainEdit, self).clean()
		try:
			domain = cleaned_data['domain']
		except KeyError:
			pass
		else:
			if not _validdomain (domain):
				raise forms.ValidationError('Please enter a valid domain.' )

			return domain



class GroupAdd(forms.Form):

	def __init__(self, groupname=None, kargs=None):
		super(GroupAdd,self).__init__(kargs)
		self.extras = {}
		self.model = AdminModel()
		# Get all available domains
		domains = self.model.getalldomains()
		if domains:
			self.fields['domain'].choices = [domain.domainname for domain in domains]
		aliases = self.model.getallaliases()
		if aliases:
			self.fields['alias'].others = [alias.aliasname for alias in aliases] 
			self.fields['alias'].exclude = groupname 

	alias = UniqueField(label="aliases", required=True, max_length=64,
						others=[], exclude=None, b_spaces=False)
	
	domain = MultipleOptionField(label="Domain", required=True, choices=[],
								 b_spaces=False)

	notes = forms.CharField(label="notes", required=False)

	def clean_alias(self):
		cleaned_data = super(GroupAdd, self).clean()
		try:
			alias = cleaned_data['alias']
		except KeyError:
			pass
		else:
			if not _validlocalpart (alias):
				raise forms.ValidationError('Please enter a valid group.' )

			return alias
	

class GroupEdit(GroupAdd):

	def __init__(self, groupname=None, kargs=None):
		super(GroupEdit,self).__init__(groupname=groupname, kargs=kargs)


def _hasspaces(value):
	''' This helper method checks to see if there are any white spaces in the
		passed value. it returns true if there are or false if there arent.'''

	# Strip leading and trailing white space
	value = value.strip()	
	try:
		# Check for a white space
		whitespace = value.index(' ')	
	except ValueError:
		return False
	else:
		return True

def _validascii(value):
	try:
		value = value.encode('US-ASCII')
	except UnicodeEncodeError:
		return False
	except UnicodeDecodeError:
		return False
	else:
		return True

def _validlocalpart(value):

	regex = re.compile(r"^[-_|0-9A-Z]+(\.[-_|0-9A-Z]+)*$" , re.IGNORECASE)

	if regex.match(value):
		return True
	else:
		return False
	

def _validdomain(value):
	regex = re.compile(r"^(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$", re.IGNORECASE)
	if regex.match(value):
		return True
	else:
		return False
	
