"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls import url
#had to add this line from StackX
from django.conf.urls import include

from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #^ matches beginning, $ matches end so this matches empty
    # using '' would match to any bit of emptiness (so all URLs would go, not good)
    url(r'^admin/', admin.site.urls),
    # was in file already path('admin/', admin.site.urls),
    url(r'^rango/', include('rango.urls'))
    #maps any URL starting with rango to be handled by rango app
    # after stripping away "rango" part
    # so therefore need to create urls.py file in rango folder
    # so rango app knows how to handle urls
]
