from django.shortcuts import render

#added redirect in c9
from django.http import HttpResponse, HttpResponseRedirect

#c6
from rango.models import Category
from rango.models import Page

#c7   c9 re: user
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from unicodedata import category

# c0 login forms
from django.contrib.auth import authenticate, login, logout
# book gave diff module but .urls in docs
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#c10 cookies / probably need it anyway
from datetime import datetime

# c 10.7
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# second versionk, first 10.6 (client side storage), then updated 10.7 (server side)
def visitor_cookie_handler(request):
    #10.7 server side version
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                                'last visit',
                                                str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
        
    request.session['visits'] = visits
    
    """ old, 10.6 version, cliend side
    # get # of visits to site
    # cookies.get returns integer of visits, if d/n/exist, 1 is default
    visits_cookie = int(request.COOKIES.get('visits', '1')) #str 1 b/c cookies take strings
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    
    # If >1d siince last visit, update count
    if (datetime.now() - last_visit_time).days > 0: # presumably this handles midnight issues 
        visits = visits_cookie + 1
        response.set_cookie('last_visit', str(datetime.now()))
        response.set_cookie('visits', visits)
        # above line needed to be moved to if block from text location (outside, wrong)
        
    #if not, keep same
    else:
        response.set_cookie('last_visit', last_visit_cookie)
    """
    

def index(request):
    #modified c 10 to check cookies
    #request.session.set_test_cookie() # commented out as was corollary in about 
    
    #modified in c6 from crap template to query categories
    #d4 ideas / use dictionary to pass to tempate engine (as template variable?)
    # need to query db for list of all cts, order by likes (Descending), 5
    #place list in context_dict dict to pass to template - moved to beneath page list
    category_list = Category.objects.order_by('-likes')[:5]
    #- indicates descending order, brackets limits to 1st 5
    
    #exercises: add stuff for pages
    page_list = Page.objects.order_by('-views')[:5]
    #moved context dict here after adding page_list 
    context_dict = {'categories': category_list,'pages': page_list}
    
    visitor_cookie_handler(request)
    #return rendered response
    #post-c10 cookie, dif vs in 10.6 and 0.7 client v server side
    
    context_dict['visits'] = request.session['visits']
    
      #c10 obtain response early so as to add cookie info
      # must place after cookie info, context_dict
    return render(request, 'rango/index.html', context_dict)
    
    #old version pre-c10 cookies
    #return render(request, 'rango/index.html', context=context_dict)
    #based on official tutorial simply "context" may be sufficient? see part 3
    
    #return HttpResponse('Rango says hey there partner! You can reach the about page <a href="about">here</a>')
    #from c3, changed in c4    
    #don't know why but seems to just want the additional / after rango ... b/c rango handling all?

def about(request):
    
    #added c10 re test cookie (along w/ set test c @ index p)
    """if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()"""
    
    context_dict = {'boldmessage': 'YO MAMA YO MAMA YO MAMA'}
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context=context_dict)
    
#c 6
def show_category(request, category_name_slug):
    #need a context dict to pass to template rendering engine
    context_dict = {}
    
    try:
        # if d/n exist, will raise exception; otherwise, returns one model
        category = Category.objects.get(slug=category_name_slug)

        # will retun list (even if empty)        
        pages = Page.objects.filter(category=category) #shoudl be category
        
        context_dict['pages'] = pages
        context_dict['category'] = category
        
    except Category.DoesNotExist:
        #error, so do nothing
        context_dict['pages'] = None
        context_dict['category'] = None
        
    # in c6 changed /about to /category and eliminated context= argument
    return render(request, 'rango/category.html', context_dict)


#from c7 for forms
@login_required
#just adding decorator results in redirect to login page 
def add_category(request):
    form = CategoryForm()
    
    #HTTP Post? (that is, did user supply data?)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            # could also give confirmation message if you wanted
            return index(request)
        
        else:
            print(form.errors)
    
    return render(request, 'rango/add_category.html', {'form': form})
# new template created

# taken from p83 may require modifications?
@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    form = PageForm()
    
    #HTTP Post? (that is, did user supply data?)
    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
        
                return show_category(request, category_name_slug)
        
        else:
            print(form.errors)
            
    context_dict ={'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

#c9 for user auth
def register(request):
    #prset reg = false, if user has reg, will --> true
    registered = False
    
    if request.method == 'POST':
        #get info from raw from, uses *BOTH* forms
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            
            #hash the pw
            user.set_password(user.password)
            user.save()
            
            #set commit to false to avoid integrity problems?  
            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            
            registered = True
         
        # if problems, send errors to terminal   
        else:
            print (user_form.errors, profile_form.errors)
     
    #if not a post request, render blank forms       
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render(request,
                'rango/register.html',
                {'user_form': user_form,
                 'profile_form': profile_form,
                 'registered': registered}  )

# more c9, handling login functionality  
def user_login(request):
    
    if request.method == 'POST':
        
        #using () instead of [] b/c () returns "none" if none, as opposed to an exception
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        #using buildt-in framework to auth and return user obj if auth ok
        user = authenticate(username=username, password=password)
        
        # if we have an user object,
        if user:
            
            if user.is_active:
                # login an dsend back to home page
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
                # !!! note use of reverse, which looks up views in urls.py
            
            # if inactive account
            else:
                return HttpResponse("Your Rango account is disabled")
        
        #bad log-in
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid username or password supplied.")
        
    # other than post method -> display form (likely a get method was used)
    else:
        return render(request, 'rango/login.html', {})

#c9 restricting access
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
# also modified settings.py LOGIN_URL to define redirect

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# def changepwform and pwchangedone  ???

# different from book b/c used Google, which gave cut-and-paste script
def search(request):
    return render(request, 'rango/search.html', {})
