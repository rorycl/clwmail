import psycopg2
from clwmail import settings

DB = settings.DATABASES['default']
db_name = DB['NAME']
db_user = DB['USER']
db_pass = DB['PASSWORD']
db_host = DB['HOST']

class CLWConnection(object):

	_connection = None

	def __init__(self ,host=db_host, name=db_name, user=db_user,
				password=db_pass):

		self.connection = self.connectionmaker(host, name, user, password)

	def cursor(self):
		return self.connection.cursor()

	def connectionmaker(self, host, name, user, password):

		if not CLWConnection._connection:
			CLWConnection._connection = psycopg2.connect("host=%s dbname=%s user=%s password=%s"
										   % (host or 'localhost', name, user, password))

		return CLWConnection._connection

		

	





