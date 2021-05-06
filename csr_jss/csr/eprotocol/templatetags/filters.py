from django import template
register = template.Library()
	
@register.filter
def str_to_list(str):
	return str.split(';')

@register.filter
def list_to_str(list):
	return ', '.join(list)