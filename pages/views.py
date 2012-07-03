# Create your views here.

from django.http import HttpResponse,HttpResponseNotFound
from django.http import HttpResponseRedirect,HttpResponseNotAllowed

# Librerias para renderizar los html.
from django.template.loader import get_template
from django.template import Context

# Data Base libraries.
from pages.models import Article 

# ----------------------------------------------------------------------
#                                HOME
# ----------------------------------------------------------------------
# To render correctly the main view (home).
def home(request):

	# choose the template.
	template = get_template("home.html")

	# Find the news (last articles updated)
	try:
		news = Article.objects.order_by('-date')[:5]
	except (NameError, ValueError):
		print(NameError + " - " + ValueError)

	return HttpResponse(template.render(Context({'news' : news})))  


# ----------------------------------------------------------------------
#                             PAGE HANDLER
# ----------------------------------------------------------------------
# To render correctly the other views (about,documentation,contact,...)
def pageHandler(request,page,subpage):
	
	# Choose the template.
	template = get_template(page + ".html")

	# Find the articles.
	try:
		articles = Article.objects.filter(page=page, category=subpage).order_by('order')
	except (NameError, ValueError):
		print(NameError + " - " + ValueError) 

	# Find the news (last articles updated)
	try:
		news = Article.objects.order_by('-date')[:5]
	except (NameError, ValueError):
		print(NameError + " - " + ValueError)

	return HttpResponse(template.render(Context({'articles' : articles,
		                                         'news' : news,
					     					     'page' : page,
					    						 'category' : subpage})))  


