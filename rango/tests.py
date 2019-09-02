from django.test import TestCase

# Create your tests here.
# from appendix but suggested at end of c5

from django.test import TestCase
from rango.models import Category

class CategoryMethodTests(TestCase):
	def test_enusre_views_are_positive(self):
		"""
		ensure_views_are_positive should result 
		True for Categories where view are zero or positive
		"""
		cat = Category(name='test', views=-1, likes=0)
		cat.save()
		self.assertEqual((cat.views >= 0), True)
		
	
