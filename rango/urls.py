# created this urls.py in rango for rango to handle urls (see p 24)

# needed to add include in c11 to work with registration 
from django.conf.urls import url, include
from rango import views
# backends added c11 to override login redirect page
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.forms import PasswordChangeForm #NECESSARY HERE?
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

class MyRegistrationView(RegistrationView):
	def get_success_url(self, request, user):
		return '/rango/'

#updated patterns in c6 to account for slugs
#patterns has been deprecated - > issue 
#changed to just a list
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^about/', views.about, name='about'),
	#?P makes group to match the slug 
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
	views.show_category, name='show_category'),
	#next added at c7 for forms
	#ordering may matter for processing of requests -- see official docs 
	url(r'^add_category/$', views.add_category, name='add_category'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
	#added c9 for registration
	url(r'^register/$', views.register, name='register'),
	#added c9 for login
	url(r'^login/$', views.user_login, name='login'),
	url(r'^restricted/$', views.restricted, name='restricted'),
	url(r'^logout/$', views.user_logout, name='logout'),
	#c11 after adding class above to redirect
	url(r'^accounts/register/$',
		MyRegistrationView.as_view(),
			name='registration_register'),
	# needed to add include import (c11 registration)
	url(r'^accounts/', include('registration.backends.simple.urls')),
	url(r'^password/change/', PasswordChangeView.as_view(), name='password_change'),
	url(r'^password/change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
	# kind of ugly because redirects to same form after PW change goes through
	
	url(r'^search/', views.search, name='search')
	]
	
