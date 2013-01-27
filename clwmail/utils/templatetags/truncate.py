from django import template

register = template.Library()

@register.filter
def truncated(value,length):
	try:
		ilength = int(length)
	except ValueError:
		pass
	else:
		if isinstance (value,str) and len(value) > ilength:
			return value [:ilength] + ' ...'

	return value 
