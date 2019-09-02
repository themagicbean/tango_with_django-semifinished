import os
from selectors import _PollLikeSelector
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
         "url":"https://docs.python.org/3/tutorial/"},
        #changed to py3 url
        #clipping part after last / from all urls (i.e. "index.html"
        {"title":"How to Think like a Computer Scientist",
         "url":"http://www.greenteapress.com/thinkpython/"},
        {"title":"Learn Python in 10 Minutes",
         "url":"https://www.stavros.io/tutorials/python/"},  ]
        #url changed from book
       
    django_pages = [
        {"title":"Official Django Tutorial",
         "url":"https://docs.djangoproject.com/en/2.1/intro/tutorial01/"},
        {"title":"Django Rocks",
         "url":"http://djangorocks.com"},
        {"title":"How to Tango with Django",
         "url":"http://www.tangowithdjango.com/"}   ]
   
    other_pages = [
        {"title":"Bottle",
         "url":"http://bottlepy.org/docs/dev/"},
        {"title":"Flask",
         "url":"http://flask.pocoo.org"}    ]
   
    cats = {
        {"category": "Python",
         "pages": {"pages": python_pages},
         "views":128,
         "likes":64},
        {"category": "Django",
         "pages": {"pages": django_pages},
         "views":64,
         "likes":32},
        {"category": "Other Frameworks",
         "pages": {"pages": other_pages},
         "views":32,
         "likes":16}    }
    # why curly brackets here?  bc dict of dicts?
    # no because square = list -> no attribute "items" error in line 56
    # but curly brackets -> unhashable error
   
    # goes through cat dict, adds each, adds assocaiated pages for each cat
    # changed cats.items() to just cats:
    for dicts in cats:
        cat = dicts["category"]
        catpages = dicts["pages"]
        views = dicts["views"]
        likes = dicts["likes"]
       # python = dicts["Python"]
        #printcheck print(cat, catpages, views, likes)
        # so far is working
        c = add_cat(cat, catpages, views, likes)
        # this works minus the for p stuff
        for pages in catpages:
            cat_data = catpages["pages"]
            for p in cat_data["pages"]:
                add_page(c, p["title"], p["url"])
   
    #print check
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1} - {2}".format(str(c), c.likes, str(p)))
            #bracketed numbers are placeholders for later outputs (str c and p)
           # c.likes gives zero for all
           
def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p
 
def add_cat(cat, catpages, views, likes):
    c = Category.objects.get_or_create(name=cat)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c
 
#this if block is trick to act as reusable module or script
if __name__ == '__main__':
    print("Starting Rango population script ... ")
    populate()