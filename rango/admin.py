from django.contrib import admin
from rango.models import Category, Page

#c6 for sluggin'
from django.contrib import admin
from rango.models import Category, Page

#c9 for userauth
from rango.models import UserProfile

# Register your models here.
# register class with admin interface
# those both moved down to be after class definitions (or else errors)

#exercises from c5
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'url']
    prepopulated_fields = {'slug':('title',)}
        #bottom line new to ex at end of c6 ?

#from c6 to auto prepopulate slug
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
admin.site.register(Page, PageAdmin)
admin.site.register(Category, CategoryAdmin)

#c9 to complement userprofile
admin.site.register(UserProfile)
    




    # moved here