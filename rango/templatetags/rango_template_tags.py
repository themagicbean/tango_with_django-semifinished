from django import template
from rango.models import Category
# this needs to be in folder templatetags, that folder @ level of models.py

register = template.Library()

@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):  # passing of cat is optional, default is none
	return{'cats': Category.objects.all(),
		'act_cat': cat}