from django import template

register = template.Library()

@register.filter
def append(string, value):
	try:
		return str(string) + str(value)
	except:
		return string 
