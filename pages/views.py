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
from pages.models import New

# Import the parser.
import parserHTML
import datetime

# Parse news object.
newsParser = parserHTML.myContentHandler();

# ----------------------------------------------------------------------
#                                HOME
# ----------------------------------------------------------------------
# To render correctly the main view (home).
def home(request):

	# choose the template.
	template = get_template("home.html")

	try:
		# Get all the pages.
		allpages = Page.objects.order_by('order')

		# Parse the news.
		newsParser.parseNews()

		# Get the last five news (articles).
		news = New.objects.order_by('-updated_date')[:7]  

		# Last new.
		lastnew = news[0]

	except (ValueError):
		print(ValueError)

	return HttpResponse(template.render(Context({'current_page_path' : "home",
												 'all_pages' : allpages,
												 'news' : news,
												 'lastnew' : lastnew})))  


# ----------------------------------------------------------------------
#                             SHOW NEW
# ----------------------------------------------------------------------
# To render correctly the other views (about,documentation,contact,...)
def showNew(request,newID):
	
	# Choose the template.
	try:
		template = get_template("news.html")
	except (ValueError):
		print(ValueError)

	# Find the pages.
	try:
		# Get all the pages.
		allpages = Page.objects.order_by('order')

		# Get default subpages.
		defaultsubpages = Subpage.objects.filter(order=1)

		# Get all the subpages.
		allsubpages = Subpage.objects.filter(rootpage__path__exact="news").order_by('order')

		# The new selected.
		articles = New.objects.get(pk=newID)

		# Get the last 5 articles modified.
		news = New.objects.order_by('-updated_date')[:5]  

	except (ValueError):
		print(ValueError)

	return HttpResponse(template.render(Context({'current_page_path' : 'news',
												 'current_subpage_path' : 'onenew',
												 'default_subpages' : defaultsubpages,
												 'all_pages' : allpages,
												 'all_subpages' : allsubpages,
												 'articles' : [articles],
		                                         'news' : news})))  

# ----------------------------------------------------------------------
#                             SHOW BIG PICTURE
# ----------------------------------------------------------------------
# To render correctly the other views (about,documentation,contact,...)
def showPicture(request,pictureName):

	# Choose the template.
	try:
		template = get_template("bigpicture.html")
	except (ValueError):
		print(ValueError)

	# Find the pages.
	try:
		# Get all the pages.
		allpages = Page.objects.order_by('order')

		# Get picture url.
		picture_url = "/static/figures/" + pictureName

		print pictureName

	except (ValueError):
		print(ValueError)

	return HttpResponse(template.render(Context({'current_page_path' : 'bigpicture',
												 'current_subpage_path' : 'bigpicture',
												 'all_pages' : allpages,
												 'picture_name' : pictureName,
												 'picture_url' : picture_url}))) 

# ----------------------------------------------------------------------------------------------------
#                                           NEWS
# ----------------------------------------------------------------------------------------------------
# Method to render correctly the view news, there are three possibilities:
#	- 'onenew' : show the last new.
#   - 'newslist' : show the list with all the news.
#   - Show the news of one year.
def news(request, subpage):

	# Set the page we are.
	page = "news"

	# choose the template.
	template = get_template(page + ".html")

	try:
		# Get all the pages.
		allpages = Page.objects.order_by('order')

		# Get default subpages.
		defaultsubpages = Subpage.objects.filter(order=1)

		# Get all the subpages.
		allsubpages = Subpage.objects.filter(rootpage__path__exact=page).order_by('order')

		# Finding the articles.
		if subpage == 'onenew':
			# Get the last new.
			articles = [New.objects.order_by('-updated_date')[0]]
		elif subpage == 'newslist':
			# Get all news.
			articles = New.objects.order_by('-updated_date')
		else:
			# Get all the news for a year.
			articles = New.objects.filter(updated_date__year=subpage).order_by('-updated_date')

		# Get the last 5 articles modified.
		news = New.objects.order_by('-updated_date')[:5]  

		# Last new
		lastnew = news[0]

	except (ValueError):
		print(ValueError)

	return HttpResponse(template.render(Context({'current_page_path' : page,
												 'current_subpage_path' : subpage,
												 'default_subpages' : defaultsubpages,
												 'all_pages' : allpages,
												 'all_subpages' : allsubpages,
												 'articles' : articles,
		                                         'news' : news,
		                                         'lastnew' : lastnew})))  

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

		if subpage=="downloads":
			# Get all the releases.
			articles = New.objects.order_by('-sg_ver')
		else :
			# Get the articles that are in page/subpage.
			articles = Article.objects.filter(rootsubpage__rootpage__path__exact=page, rootsubpage__path__exact=subpage)

		# Get the last 5 articles modified.
		news = New.objects.order_by('-updated_date')[:5]  

		# Last new
		lastnew = news[0]

	except (ValueError):
		print(ValueError)

	return HttpResponse(template.render(Context({'current_page_path' : page,
												 'current_subpage_path' : subpage,
												 'default_subpages' : defaultsubpages,
												 'all_pages' : allpages,
												 'all_subpages' : allsubpages,
												 'articles' : articles,
		                                         'news' : news,
		                                         'lastnew' : lastnew})))  


