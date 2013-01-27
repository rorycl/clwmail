from django import forms

class LoginForm(forms.Form):
	username = forms.EmailField(label ="Username",
							required =True)

	password = forms.CharField(label ='Password',
							   required = True, 
							   max_length =64)

	
