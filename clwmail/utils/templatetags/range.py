from django import template

register = template.Library()

@register.filter
def range_filter(value):
	list =range(int(value))
	return list 
