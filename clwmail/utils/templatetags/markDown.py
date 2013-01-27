
from django import template
from markdown import Markdown

register = template.Library()

@register.filter
def markDown(field):
	markdown_text =Markdown(field,safe_mode=False)

	return markdown_text.toString()
