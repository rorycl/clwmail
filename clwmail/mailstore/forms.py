from django import forms

class HolidayForm(forms.Form):
	hstart_date = forms.DateTimeField(label="Start Date",
								  required=True)

	hend_date = forms.DateTimeField(label="End Date",
								  required=True)

	message = forms.CharField(label ='Holiday Message',
							   required = True )

	b_default = forms.BooleanField(label ='Default message',
							   required = False )
	
