from django import template

register = template.Library()

@register.filter
def addClass(field, css = None):
	# The old html representation of the field
	old_widget = field.field.widget

	# Add the class attribute
	new_widget = old_widget.__class__({'class':css})

	# Replace the original widget
	field.field.widget = new_widget

	return field
