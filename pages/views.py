# Create your views here.

from django.http import HttpResponse,HttpResponseNotFound
from django.http import HttpResponseRedirect,HttpResponseNotAllowed

# HTML rendering libraries.
from django.template.loader import get_template
from django.template import Context

# Data Base libraries.
from pages.models import Page
from pages.models import Subpage 
from pages.models import Article 

# News downloads library.
import httplib

# ----------------------------------------------------------------------
#                                HOME
# ----------------------------------------------------------------------
# To render correctly the main view (home).
def home(request):

	# choose the template.
	template = get_template("home.html")

	try:
		# Get all the pages.
		allpages = Page.objects.all()
		
		# Get the last five news (articles).
		news = Article.objects.order_by('-date')[:5]  

	except (NameError, ValueError):
		print(NameError + " - " + ValueError)

	return HttpResponse(template.render(Context({'current_page_path' : "home",
												 'all_pages' : allpages,
												 'news' : news})))  


# ----------------------------------------------------------------------
#                             PAGE HANDLER
# ----------------------------------------------------------------------
# To render correctly the other views (about,documentation,contact,...)
def pageHandler(request,page,subpage):
	
	# Choose the template.
	try:
		template = get_template(page + ".html")
	except (ValueError):
		print(ValueError)

	# Find the pages.
	try:
		# Get all the pages.
		allpages = Page.objects.order_by('order')

		# Get default subpages.
		defaultsubpages = Subpage.objects.filter(order=1)

		# Get all the subpages.
		allsubpages = Subpage.objects.filter(rootpage__path__exact=page).order_by('order')

		# Get the articles that are in page/subpage.
		articles = Article.objects.filter(rootsubpage__rootpage__path__exact=page, rootsubpage__path__exact=subpage)

		# Get the last 5 articles modified.
		news = Article.objects.order_by('-date')[:5]  

	except (NameError, ValueError):
		print(NameError + " - " + ValueError)

	return HttpResponse(template.render(Context({'current_page_path' : page,
												 'current_subpage_path' : subpage,
												 'default_subpages' : defaultsubpages,
												 'all_pages' : allpages,
												 'all_subpages' : allsubpages,
												 'articles' : articles,
		                                         'news' : news})))  


