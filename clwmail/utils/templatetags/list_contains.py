from django import template

register = template.Library()

@register.filter
def list_contains(list,value):
	if list:
		for item in list:
			if type (value) == unicode:
				item = item.replace(" ","-")
			if item == value:
				return True

	return False

@register.filter
def contained_list(value, list):
	if list:
		for item in list:
			if type (value) == unicode:
				item = item.replace(" ","-")
			if str(item) == str(value):
				return True
	return False
