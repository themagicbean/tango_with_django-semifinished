from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
# c5 p 42

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    #slugs added in c6 to auto update clean urls
    slug = models.SlugField()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        #slugify eliminates white space (?)
        super(Category, self).save(*args, **kwargs)
       
    class Meta:
        verbose_name_plural = 'categories'
    #who cares?
    
    def __str__(self):
        return self.name
    
    
    # below, changed to make nonnegative in test chapter, p 195
    # could try PositiveIntegerField
    #next added corresponding to p187 / testing 
    
    """
    @property 
    def ensure_views_are_positive(self):
        if self.views < 0:
            views = 0
            return views
      
    def __init__(name, views, likes):
        self.name = name
        self.likes = likes
        if self.views <0:
            self.views = 0  
        else:
            self.views = views    
    
    
    if views < 0:
        views = 0
    """  
        
    # views = max(views, 0)
    


class Page(models.Model):
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    # foreign key in django 2.0 requires on_delete arg
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    # slug added in c6 exercises, caused db / sql errors
    slug = models.SlugField()
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        #had to change name to title
        super(Page, self).save(*args, **kwargs)

    
    def __str__(self):
        return self.name

#added c9 to add attributes to User model
class UserProfile(models.Model):
        #required line, links to a user modle instance
        user = models.OneToOneField(User, on_delete=models.PROTECT)
        
        #additional attributes
        website = models.URLField(blank=True)
        picture = models.ImageField(upload_to='profile_images', blank=True)
        
        #overrride __unicode__() method to return something else
        def __str__(self):
            return self.user.username
