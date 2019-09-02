# created in 5.7 as data population script
# this shit works
# updated to add likes, views to categories (working)
# #3 file experiment to add views to pages
# #3 file works, renamed as main populate_rango file
# this is after edit for exercises at end of c6
 
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')
# need to set path and import settings (via setup() below)
import django
django.setup()
from rango.models import Category, Page
# must import specifics (cat, page) after import gen settings (preceding line)
 
def populate():
    #Create lists of dicts of pages
    #Then dict of dicts for categories
    #Allows iteration through each data structure
   
    python_pages = [
        {"title": "Official Python Tutorial",
         "url":"https://docs.python.org/3/tutorial/",
         "views":11},
         
        #changed to py3 url
        #clipping part after last / from all urls (i.e. "index.html"
        {"title":"How to Think like a Computer Scientist",
         "url":"http://www.greenteapress.com/thinkpython/",
         "views":22},
        {"title":"Learn Python in 10 Minutes",
         "url":"https://www.stavros.io/tutorials/python/",
         "views":33}  ]
        #url changed from book
        
    django_pages = [
        {"title":"Official Django Tutorial",
         "url":"https://docs.djangoproject.com/en/2.1/intro/tutorial01/",
         "views":44},
        {"title":"Django Rocks",
         "url":"http://djangorocks.com",
         "views":55},
        {"title":"How to Tango with Django",
         "url":"http://www.tangowithdjango.com/",
         "views":66}   ]
   
    other_pages = [
        {"title":"Bottle",
         "url":"http://bottlepy.org/docs/dev/",
         "views":77},
        {"title":"Flask",
         "url":"http://flask.pocoo.org",
         "views":88}    ]
   
    cats = [
        {"category":"Python",
		 "pages":python_pages,
		 "views":128,
         "likes":64},
        {"category":"Django",
		 "pages":django_pages,
         "views":64,
         "likes":32},
        {"category":"Other Frameworks",
		 "pages":other_pages,
         "views":32,
         "likes":16}    ]
   
    # goes through cat dict, adds each, adds assocaiated pages for each cat
	#need nested loop to list through list (of dicts) then dicts
    for dicts in cats:
        cat = dicts["category"]
        catpages = dicts["pages"]
        views = dicts["views"]
        likes = dicts["likes"]
        c = add_cat(cat, views, likes)

        for p in catpages:
            add_page(c, p["title"], p["url"], p["views"])
   
    #print check
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1} views: {2} likes: {3}".format(str(c), str(p.title), int(p.views), int(p.likes)))
            #bracketed numbers are placeholders for later outputs (str c and p)
            
def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c
 
#this if block is trick to act as reusable module or script
if __name__ == '__main__':
    print("Starting Rango population script ... ")
    populate()