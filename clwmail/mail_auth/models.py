#from django.db import models
#from clwmail.mailstore.models import Domain
#
#class Alias (models.Model): 
#	alias = models.CharField('Domain Name', maxlength=128) 
#	domain = models.ForeignKey(Domain, db_column="domain") 
#	created = models.DateTimeField('Date created', auto_now_add=True) 
#	notes = models.TextField('Notes', null=True)	
#
#	class Meta: 
#		db_table = 'aliases' 
#		# Cant make composite Primary keys
#		unique_together = (("alias", "domain"),)
#
#class MailUser (models.Model):
#	# The choices for the status
#	STATUS_CHOICES = ( (1,1),
#					   (2,2),
#					   (3,3),
#					   (9,9),)
#
#	# actually only needs to be unique agains DOMAIN
#	userid = models.CharField('User Name', maxlength=128) 
#
#	created = models.DateTimeField('Date created', auto_now_add=True) 
#	password = models.CharField('Password', maxlength=64)
#	home = models.CharField('Home',maxlength=256)
#	domain = models.ForeignKey(Domain, db_column="domain") 
#	uid = models.IntegerField('UID') 
#	gid = models.IntegerField('GID') 
#	status = models.IntegerField('Status', choices = STATUS_CHOICES)
#	typer = models.CharField('Person or Project', maxlength=12, null=True)
#	role = models.CharField('Role',maxlength=64, null=True)
#	notes = models.TextField('Notes', null=True)
#	holidaymsg = models.TextField('Holiday message', null=True)
#	holidayend = models.DateTimeField('Holiday end')
#	leavedate = models.DateTimeField('Leave date')
#	leavemsg = models.TextField('Leave message', null=True)
#
#	def save(self):
#		# Set the default status
#		if not self.id:
#			self.status =1
#
#		super(MailUser,self).save()
#
#	class Meta:
#		db_table = 'users' 
#		# Cant make composite Primary keys
#		unique_together = (("domain", "userid"),)
#
#
#class AliasUsers (models.Model): 
#	alias  = models.ForeignKey(Alias, to_field='alias', db_column='alias') 
#	domain = models.ForeignKey(Domain, db_column="domain") 
#	userid = models.ForeignKey(MailUser, to_field='userid', db_column='userid')
#
#	class Meta: 
#		db_table = 'alias_users' 
#		unique_together =(('domain', 'alias', 'userid'),)
