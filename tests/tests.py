import unittest
import sys, os

sys.path[0]=('<path_to>/clwmail/')
os.environ['DJANGO_SETTINGS_MODULE'] =  'clwmail.settings'

from clwmail import settings
from clwmail.utils.clwconnection import CLWConnection
from clwmail.utils.objectmaker import PyGenObjects, PyObject
from clwmail.admin.sql.viewdb import AdminModel
from clwmail.mailstore.sql.viewdb import MailModel
from clwmail.mail_auth.sql.viewdb import AuthModel 
from clwmail.exim.sql.viewdb import EximModel 
from clwmail.mail_auth.permissions import canview 
from datetime import datetime, timedelta

urlrel = settings.RELATIVE_URL

test_db_name = 'clwmail' 
test_db_user = 'user' 
test_db_pass = 'password' 
test_db_host = 'localhost'

class MailTestCase(unittest.TestCase):

	def setUp(self):
		# Get connection singleton
		connection = CLWConnection(test_db_host, test_db_name, test_db_user,
								   test_db_pass)
		# Create a new cursor object.
		cursor = connection.cursor()

		params = {'mode': 1,
				  'domainname': 'example.co.uk',
				  'newdomainname': None,
				  }
		self.adminmodel = AdminModel()
		self.authmodel = AuthModel()
		self.mailmodel = MailModel()
		self.eximmodel = EximModel()

		domainadded = self.adminmodel.managedomain(params)

		# Create a user		
		params = {'mode': 1,
				  'userid': 'test.a',
				  'password': 'password',
				  'home': '/home/mailstore/',
				  'domain': 'example.co.uk',
				  'uid': 1001,
				  'gid': 1001,
				  'status': 1,
				  'typer':'Person',
				  'role':"",
				  'fullname':'Test User', 
				  'notes':None
				  }
		# add the user
		useradded = self.adminmodel.manageuser(params)
		# Check user added
		self.assertNotEqual(useradded, False)

	def test_auth(self):
		# Check login
		user = self.authmodel.login('test.a@example.co.uk', 'password')
		# check user returned
		self.assertEqual(user.userid, 'test.a')
		# Check not working
		user = self.authmodel.login('none@example.co.uk', 'password')
		self.assertEqual(user.userid, None)

	def test_usermanage(self):
		# Create a user		
		params = {'mode': 1,
				  'userid': 'test.b',
				  'password': 'password',
				  'home': '/home/mailstore/',
				  'domain': 'example.co.uk',
				  'uid': 1001,
				  'gid': 1001,
				  'status': 1,
				  'typer':'Person',
				  'role':"Architect",
				  'fullname':'Test User', 
				  'notes':"here are some notes"
				  }
		# add the user
		useradded = self.adminmodel.manageuser(params)
		# Check user added
		self.assertNotEqual(useradded, False)

		# add the user
		useradded = self.adminmodel.manageuser(params)

		user = self.adminmodel.getuser('test.b', 'example.co.uk')
		self.assertNotEqual(user, None)
		self.assertEqual(user.password,'password')
		self.assertEqual(user.userid,'test.b')
		self.assertEqual(user.domain,'example.co.uk')
		self.assertEqual(user.status,1)
		self.assertEqual(user.typer,'Person')
		self.assertEqual(user.uid,1001)
		self.assertEqual(user.gid,1001)
		self.assertEqual(user.role,'Architect')
		self.assertEqual(user.notes,'here are some notes')

		# Edit a user		
		params = {'mode': 2,
				  'userid': 'test.b',
				  'password': 'changedpass',
				  'home': '/home/mailstore/',
				  'domain': 'example.co.uk',
				  'uid': 1001,
				  'gid': 1001,
				  'status': 1,
				  'typer':'Person',
				  'role':"Architect",
				  'fullname':'Test User edited', 
				  'notes':"here are some notes"
				  }
		# edit the user
		useredited = self.adminmodel.manageuser(params)
		# Check user edited 
		self.assertNotEqual(useredited, False)

		user = self.adminmodel.getuser('test.b', 'example.co.uk')
		self.assertNotEqual(user, None)
		self.assertEqual(user.password,'changedpass')
		self.assertEqual(user.fullname,'Test User edited')

		#hide a user		
		params = {'mode': 4,
				  'userid': 'test.b',
				  'password': None,
				  'home': None,
				  'domain':'example.co.uk',
				  'uid': None,
				  'gid': None,
				  'status': 9,
				  'typer':None,
				  'role':None,
				  'fullname':None, 
				  'notes':None
				  }
		# edit the user
		userhidden = self.adminmodel.manageuser(params)
		# Check user edited 
		self.assertNotEqual(userhidden, False)
	

		user = self.adminmodel.getuser('test.b', 'example.co.uk')
		self.assertNotEqual(user, None)
		self.assertEqual(user.status,9)

		# delete a user		
		params = {'mode': 3,
				  'userid': 'test.b',
				  'password': None,
				  'home': None,
				  'domain': 'example.co.uk',
				  'uid': None,
				  'gid': None,
				  'status': 9,
				  'typer':None,
				  'role':None,
				  'fullname':None, 
				  'notes':None
				  }

		# delete the user
		userdeleted = self.adminmodel.manageuser(params)

		self.assertNotEqual(userdeleted, False)

		user = self.adminmodel.getuser('test.b', 'example.co.uk')
		self.assertEqual(user.userid, None)

	def test_goupmanage(self):
		# Create a group		
		params = {'mode': 1,
				  'alias': 'agroup',
				  'domain': 'example.co.uk',
				  'new_alias': None,
				  'notes':"test" 
				  }

		# try add the group 
		groupadded = self.adminmodel.managealias(params)
		# Check group was added 
		self.assertEqual(groupadded, True)

		params = {'mode':1, # add alias users
				  'alias':'agroup',
				  'userid':'test.a',
				  'domain':'example.co.uk'
				 }
		# check added user to alias
		aliasuseradded = self.adminmodel.managealiasuser(params)
		self.assertEqual(aliasuseradded, True)

		# Retrieve info	
		alias = self.adminmodel.getalias('agroup', 'example.co.uk')
		self.assertNotEqual(alias, None)
		self.assertEqual(alias.aliasname,'agroup')
		self.assertEqual(alias.notes,'test')

		users = self.adminmodel.getaliasusers('agroup','example.co.uk')
		self.assertNotEqual(users, None)
		users = list(users)
		self.assertEqual(len(users),1)
		user = users[0]
		self.assertEqual(user.username,'test.a@example.co.uk')

		# create function parameter list
		params = {'mode': 2,
				  'alias': 'agroup',
				  'domain': 'example.co.uk',
				  'new_alias': 'bgroup',
				  'notes': None
					  }
		# edit the group 
		groupedited = self.adminmodel.managealias(params)
		# Check alias edited 
		self.assertNotEqual(groupedited, False)

		alias = self.adminmodel.getalias('bgroup', 'example.co.uk')
		self.assertNotEqual(alias, None)
		self.assertEqual(alias.aliasname,'bgroup')
		self.assertEqual(alias.notes,None)

		users = self.adminmodel.getaliasusers('bgroup','example.co.uk')
		self.assertNotEqual(users, None)
		users = list(users)
		self.assertEqual(len(users),1)
		user = users[0]
		self.assertEqual(user.username,'test.a@example.co.uk')

		# create function parameter list
		params = {'mode': 3,
				  'alias': 'bgroup',
				  'domain': 'example.co.uk',
				  'new_alias': None,
				  'notes':None 
					  }
		# delete the group 
		groupdeleted = self.adminmodel.managealias(params)
		# Check user edited 
		self.assertNotEqual(groupdeleted, False)

		# Ensure there was a cascding delete of alias users
		users = self.adminmodel.getaliasusers('bgroup','example.co.uk')
		self.assertEqual(users, None)

	def test_domainmanage(self):
		# Create a domain		
		params = {'mode': 1,
				  'domainname': 'HOPKINS.CO.UK',
				  'newdomainname': None,
				  }

		# try add the domain 
		domainadded = self.adminmodel.managedomain(params)
		# Check domain was NOT added 
		self.assertEqual(domainadded, False)
		self.assertEqual(self.adminmodel.error, "This domain already exists\n")

		# Create a domain		
		params = {'mode': 1,
				  'domainname': 'otherdomain.com',
				  'newdomainname': None,
				  }
		# try add the domain 
		domainadded = self.adminmodel.managedomain(params)
		# Check domain was added 
		self.assertEqual(domainadded, True)

		# Get the domain
		request_domain = self.adminmodel.getdomain('otherdomain.com')
		self.assertEqual(request_domain.domainname, 'otherdomain.com')
		
		params = {'mode': 2,
				  'domainname': 'example.co.uk',
				  'newdomainname': 'newexample.co.uk',
				  }

		# check edited domain 
		domainedited = self.adminmodel.managedomain(params)
		self.assertEqual(domainedited, True)

		# Get the domain
		request_domain = self.adminmodel.getdomain('newexample.co.uk')
		self.assertEqual(request_domain.domainname, 'newexample.co.uk')

		# Check changed reflected in users
		user = self.adminmodel.getuser('test.a', 'newexample.co.uk')
		self.assertNotEqual(user, None)
		self.assertEqual(user.domain, 'newexample.co.uk')
		self.assertEqual(user.userid, 'test.a')

		# Delete a domain		
		params = {'mode': 3,
				  'domainname': 'otherdomain.com',
				  'newdomainname': None,
				  }
		# try delete the domain 
		domaindeleted = self.adminmodel.managedomain(params)
		# Check domain was deleted
		self.assertEqual(domaindeleted, True)
		
		# Get the domain
		request_domain = self.adminmodel.getdomain('otherdomain.com')
		self.assertEqual(request_domain.domainname, None)

		# try delete domain with reference to user		
		params = {'mode': 3,
				  'domainname': 'newexample.co.uk',
				  'newdomainname': None,
				  }
		# try delete the domain 
		domaindeleted = self.adminmodel.managedomain(params)
		# Check domain was Not deleted
		self.assertEqual(domaindeleted, False)
		self.assertEqual(self.adminmodel.error,
						"This domain is referenced by users of the system and cannot be deleted.\n")
		
		
		# Get the domain
		request_domain = self.adminmodel.getdomain('newexample.co.uk')
		self.assertNotEqual(request_domain, None)

	def test_holidaymanage(self):
		#Add holiday
		param_dict = {'mode':1,
					  'username':'test.a',
					  'domain':'example.co.uk',
					  'hstart':'2008-01-01 09:00:00',
					  'hend':'2008-01-10 09:00:00',
					  'message':"The holiday message",
					  'id':-1,
					  'b_default':False}
		
		result = self.mailmodel.manageholiday(**param_dict)
		self.assertNotEqual(result, None)

		holidays = self.mailmodel.getuserholidays( 'test.a', 'example.co.uk')	
		self.assertNotEqual(holidays, None)
		holidays = list(holidays)
		self.assertEqual(len(holidays), 1)
		holiday = holidays[0]

		self.assertEqual(holiday.holstart.year,2008)
		self.assertEqual(holiday.holstart.month,1)
		self.assertEqual(holiday.holstart.day,1)
		self.assertEqual(holiday.holstart.hour,9)
		self.assertEqual(holiday.holstart.minute,0)

		self.assertEqual(holiday.holend.year,2008)
		self.assertEqual(holiday.holend.month,1)
		self.assertEqual(holiday.holend.day,10)
		self.assertEqual(holiday.holend.hour,9)
		self.assertEqual(holiday.holend.minute,0)

		self.assertEqual(holiday.holmsg,'The holiday message')

		#Edit holiday
		param_dict = {'mode':2,
					  'username':'test.a',
					  'domain':'example.co.uk',
					  'hstart':'2008-01-01 10:00:00',
					  'hend':'2008-01-10 09:00:00',
					  'message':"The edit message",
					  'id':holiday.holid,
					  'b_default':False}

		
		result = self.mailmodel.manageholiday(**param_dict)
		self.assertNotEqual(result, None)

		holidays = self.mailmodel.getuserholidays( 'test.a', 'example.co.uk')	
		self.assertNotEqual(holidays, None)
		holidays = list(holidays)
		self.assertEqual(len(holidays), 1)
		holiday = holidays[0]

		self.assertEqual(holiday.holstart.year,2008)
		self.assertEqual(holiday.holstart.month,1)
		self.assertEqual(holiday.holstart.day,1)
		self.assertEqual(holiday.holstart.hour,10)
		self.assertEqual(holiday.holstart.minute,0)
	
		self.assertEqual(holiday.holmsg,'The edit message')

		#Delete holiday
		param_dict = {'mode':3,
					  'username':'test.a',
					  'domain':'example.co.uk',
					  'hstart':None,
					  'hend':None,
					  'message':None,
					  'id':holiday.holid,
					  'b_default': None}

		result = self.mailmodel.manageholiday(**param_dict)
		self.assertNotEqual(result, None)

		holidays = self.mailmodel.getuserholidays( 'test.a', 'example.co.uk')	
		self.assertEqual(holidays, None)

		# Check setting of holdiday to current
		now = datetime.now()
		tendays = now + timedelta (days =10)

		#Add holiday
		param_dict = {'mode':1,
					  'username':'test.a',
					  'domain':'example.co.uk',
					  'hstart':now,
					  'hend':tendays,
					  'message':"current message",
					  'id':-1,
					  'b_default':False}
		
		result = self.mailmodel.manageholiday(**param_dict)
		self.assertNotEqual(result, None)

		b_holset = self.eximmodel.setholidays()
		self.assertEqual(b_holset, 1)

		holmessage = self.mailmodel.getcurrentholiday('test.a','example.co.uk')
		self.assertNotEqual(holmessage, None)
		self.assertEqual(holmessage.message, 'current message')

		# Remove current holiday
		param_dict = {'mode':2,
					  'username':'test.a',
					  'domain':'example.co.uk',
					  'hstart':None,
					  'hend':None,
					  'message':None,
					  'id':None}

		result = self.mailmodel.removeleave(**param_dict)

		user = self.adminmodel.getuser('test.a', 'example.co.uk')
		self.assertNotEqual(user, None)

		self.assertEqual(user.status,1)
		
		# Test leaver

		# Create a user		
		params = {'mode': 1,
				  'userid': 'leaver',
				  'password': 'password',
				  'home': '/home/mailstore/',
				  'domain': 'example.co.uk',
				  'uid': 1001,
				  'gid': 1001,
				  'status': 1,
				  'typer':'Person',
				  'role':"",
				  'fullname':'Leaver', 
				  'notes':None
				  }

		# add the user
		useradded = self.adminmodel.manageuser(params)
		# Check user added
		self.assertNotEqual(useradded, False)

		# set user to leaver		
		params = {'mode': 1,
				  'userid': 'leaver',
				  'domain': 'example.co.uk',
				  'leavedate': now,
				  'message': 'This person has left'
				  }

		result = self.eximmodel.manageleaver(params)
		self.assertNotEqual(result, None)

		message = self.eximmodel.getleavermessage('leaver','example.co.uk')
		self.assertNotEqual(message,None)
		self.assertEqual(message,'This person has left')
		
		# unset user to leaver		
		params = {'mode': 2,
				  'userid': 'leaver',
				  'domain': 'example.co.uk',
				  'leavedate':None,
				  'message':None 
				  }

		result = self.eximmodel.manageleaver(params)
		self.assertNotEqual(result, None)

		# Check changed reflected in users
		user = self.adminmodel.getuser('test.a', 'example.co.uk')
		self.assertNotEqual(result, None)
		self.assertEqual(user.status,1)
		
	def test_exim(self):
		''' This test case ensures that the exim functions used are
			working properly'''
		active_user = self.eximmodel.getactiveuser('test.a','example.co.uk')
		self.assertNotEqual(active_user, None)
		self.assertEqual(active_user.userid,'test.a')

		holiday_user = self.eximmodel.getactiveuser('test.a','example.co.uk')
		self.assertNotEqual(holiday_user, None)
		self.assertEqual(holiday_user.userid,'test.a')

		now = datetime.now()
		tendays = now + timedelta (days =10)

		#Add holiday
		param_dict = {'mode':1,
					  'username':'test.a',
					  'domain':'example.co.uk',
					  'hstart':now,
					  'hend':tendays,
					  'message':"current message",
					  'id':-1,
					  'b_default':False}
		
		result = self.mailmodel.manageholiday(**param_dict)
		self.assertNotEqual(result, None)

		b_holset = self.eximmodel.setholidays()
		self.assertEqual(b_holset, 1)

		# unset user to leaver		
		params = {'mode': 1,
				  'userid': 'test.a',
				  'domain': 'example.co.uk',
				  'leavedate':now,
				  'message':"leaving" 
				  }

		result = self.eximmodel.manageleaver(params)
		self.assertNotEqual(result, None)

		leave_user = self.eximmodel.getleaveruser('test.a','example.co.uk')
		self.assertNotEqual(leave_user, None)
		self.assertEqual(leave_user.userid,'test.a')

		params = {'userid': 'test.a',
				  'domain': 'example.co.uk'}

		result = self.eximmodel.manageactiveusers(params)
		self.assertNotEqual(result, None)
		active_user = self.adminmodel.getuser('test.a','example.co.uk')
		self.assertNotEqual(active_user, None)
		self.assertEqual(active_user.status,1)
		

	def tearDown(self):
		query  = "DELETE FROM users;"
		self.adminmodel.executequery(query)
		query  = "DELETE FROM domains;"
		self.adminmodel.executequery(query)

if __name__ == "__main__":
	unittest.main()
