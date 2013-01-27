#from django.db import models 
#from clwmail.mail_auth.models import MailUser  
#
#
#class Domain (models.Model): 
#	created = models.DateTimeField('Date created', auto_now_add=True) 
#	domain = models.CharField('Domain Name', maxlength=128, primary_key=True)
#
#	class Meta:
#		db_table = 'domain' 
#
#class Holiday (models.Model):
#	created = models.DateTimeField('Date created', auto_now_add=True) 
#	# Cant make composite Foreign keys
#
#	userid = models.ForeignKey(MailUser, to_field='userid', 
#							   db_column='userid', related_name ='holiday_userid')
#
#	domain = models.ForeignKey(MailUser, to_field='domain', 
#							   db_column='userid', related_name ='holiday_dom')
#
#	holidaystart = models.DateTimeField('Holiday start')
#	holidayend = models.DateTimeField('Holiday end')
#	message = models.TextField('message', null=True)
#
#	class Meta: 
#		db_table = 'alias_users' 
#
#class Log (models.Model):
#	dt_created = models.DateTimeField('Date created', auto_now_add=True) 
#	t_message_date = models.TextField('Message date', null=True)
#	t_message_id   = models.TextField('Message id', null=True)
#	t_orig_id =  models.TextField('Original id', null=True)
#	t_recipients = models.TextField('Recipients', null=True)
#	t_subject = models.TextField('Subject', null=True)
#	n_size = models.IntegerField('Size', null=True)  
#	t_from = models.TextField('From', null=True)
#	t_to = models.TextField('To', null=True)
#	t_cc = models.TextField('Cc', null=True)
#	t_sha1sum = models.TextField('SHA 1 sum', null=True)
#	dt_processed = models.DateTimeField('Date processed', null=True)
#	b_processed  = models.BooleanField ('Processed Field', null=True) 
#
#
#	def save (self):
#		if not self.id:
#			self.b_processed = False
#		super(Log,self).save()
#
#	class Meta:
#		db_table = 'log'
#		
#
#
#
