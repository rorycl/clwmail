from django import template

register = template.Library()

@register.filter
def numdigits(value, num):
	if type(value) == int:
		value = str(value)

	if type (value) ==str and value.isdigit():
		list_val = list(value)
		start = len (list_val)
		while start < num:
			list_val.insert(0,'0')
			start +=1
		
		str_val = "".join(list_val)
		return str_val
			
	return value


