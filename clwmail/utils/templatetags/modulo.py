from django import template

register = template.Library()

@register.filter
def modulo(value, modulo):
	
	if type(value) == type(0):
		if  type(modulo) == type(0):
			return (value % modulo)
	return value


