# Create your views here.

import shogun.settings as settings

from django.http import HttpResponse,Http404

# HTML rendering libraries.
from django.template.loader import get_template
from django.template import Context,TemplateDoesNotExist

# Data Base libraries.
from pages.models import Page
from pages.models import Subpage
from pages.models import Article
from pages.models import New

# Import the parser.
import os
import os.path
import parserHTML
import datetime
import calendar
import importlib
from BeautifulSoup import BeautifulSoup

# Parse news object.
newsParser = parserHTML.myContentHandler();


def error(err):
	if  settings.DEBUG:
		print(err)
	raise Http404


def get_news():
	# Get the last 5 articles modified.
	news = New.objects.order_by('-updated_date')[:7]

	# Latest news
	latest=None
	if len(news)>0:
		latest= news[0]

	return news,latest

# ----------------------------------------------------------------------
#                                HOME
# ----------------------------------------------------------------------
# To render correctly the main view (home).
def home(request):

	# choose the template.
	template = get_template("home.html")

	try:
		# Get all the pages.
		allpages = Page.objects.order_by('sort_order')

		# Parse the news.
		newsParser.parseNews()
		news,lastnew=get_news()
	except ValueError, err:
		error(err)

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
	template = get_template("news.html")

	# Find the pages.
	try:
		# Get all the pages.
		allpages = Page.objects.order_by('sort_order')

		# Get default subpages.
		defaultsubpages = Subpage.objects.filter(sort_order=1)

		# Get all the subpages.
		allsubpages = Subpage.objects.filter(rootpage__path__exact="news").order_by('sort_order')

		# The new selected.
		articles = New.objects.get(pk=newID)
		news = get_news()[0]

	except ValueError, err:
		error(err)

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
	template = get_template("bigpicture.html")

	# Find the pages.
	try:
		# Get all the pages.
		allpages = Page.objects.order_by('sort_order')

		# Get picture url.
		picture_url = "/static/figures/" + pictureName

	except ValueError, err:
		error(err)

	return HttpResponse(template.render(Context({'current_page_path' : 'bigpicture',
												 'current_subpage_path' : 'bigpicture',
												 'all_pages' : allpages,
												 'picture_name' : pictureName,
												 'picture_url' : picture_url})))


def irclog(request, year, month, day):
	fname = '%s/#shogun.%s-%s-%s.log.html'  % (settings.SHOGUN_IRCLOGS, year, month, day)
	try:
		template = get_template("irclogs.html")

		# Get all the pages.
		allpages = Page.objects.order_by('sort_order')

		news = get_news()[0]
		html=file(fname).read()
		soup = BeautifulSoup(html)
		logfile=str(soup.body.table)
	except Exception, err:
		error(err)

	return HttpResponse(template.render(Context({'current_page_path' : 'contact',
												 'current_subpage_path' : 'irc / irclogs',
												 'all_pages' : allpages,
												 'all_subpages' : ['irclogs'],
												 'logfile' : logfile,
		                                         'news' : news})))


def get_calendar_logs(logfiles):
	logfiles_set=set(logfiles)
	cal = calendar.Calendar()
	start_entry=logfiles[0]
	end_entry=logfiles[-1]
	start_year=int(start_entry[:4])
	start_month=int(start_entry[5:7])
	end_year=int(end_entry[:4])
	end_month=int(end_entry[5:7])

	all_entries=[]
	for year in xrange(start_year,end_year+1):
		cur_start_month=1
		cur_end_month=12

		if year == start_year:
			cur_start_month=start_month
		if year == end_year:
			cur_end_month=end_month

		year_entries=[]
		for month in xrange(cur_start_month, cur_end_month+1):
			month_entries=[]

			weeks_entries=[]
			week_entries=[]
			weekday=0
			for day in cal.itermonthdays(year, month):
				weekday+=1
				entry=["","", ""]
				if day>0:
					key='%04d-%02d-%02d' % (year,month,day)
					entry=[day, "", ""]
					if key in logfiles_set:
						entry[1:3]=key, os.path.getsize(settings.SHOGUN_IRCLOGS + '/' + '#shogun.%s.log.html' % key)/1024
				week_entries.append(entry)
				if (weekday>0) and (weekday % 7 == 0):
					weeks_entries.append(week_entries)
					week_entries=[]

			if len(week_entries)>0:
				weeks_entries.append(week_entries)
			month_entries=[weeks_entries]
			year_entries.append((calendar.month_name[month], month_entries))
		all_entries.append((year, year_entries[::-1]))

	return all_entries[::-1]


def irclogs(request):
	logfiles = [ f.replace('#shogun.','').replace('.log.html','') for f in os.listdir(settings.SHOGUN_IRCLOGS) if f.startswith('#shogun') ]
	logfiles.sort()


	try:
		template = get_template("irclogs.html")

		# Get all the pages.
		allpages = Page.objects.order_by('sort_order')
		allsubpages=[]
		news = get_news()[0]
		all_entries = get_calendar_logs(logfiles)

	except IOError, err:
		error(err)

	return HttpResponse(template.render(Context({'current_page_path' : 'contact',
												 'current_subpage_path' : 'irc / irclogs',
												 'all_pages' : allpages,
												 'all_subpages' : allsubpages,
												 'irclogfiles' : all_entries,
		                                         'news' : news})))


def planet(request):
	try:
		template = get_template("planet.html")

		# Get all the pages.
		allpages = Page.objects.order_by('sort_order')

		news = get_news()[0]

		html=file(settings.SHOGUN_PLANET).read()
		soup = BeautifulSoup(html)
		items=soup.body.findAll("div", { "class" : "daygroup" })
		articles=[]
		for article in soup.body.findAll("div", { "class" : "daygroup" }):
			polished='<dt><h1>' + article.h2.string + '</h1></dt>'
			articles.append(polished + unicode(article.div.div).replace('class="content"',"").replace('{tex}','\[').replace('{/tex}','\]'))


	except Exception, err:
		error(err)

	return HttpResponse(template.render(Context({'current_page_path' : 'planet',
												 'current_subpage_path' : 'shogun',
												 'all_pages' : allpages,
												 'all_subpages' : ['planet'],
												 'articles' : articles,
		                                         'news' : news})))

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

	# choose the news template.
	template = get_template(page + ".html")

	defaultsubpages=[]
	all_pages=[]
	all_subpages=[]
	articles=[]
	news=[]
	lastnew=[]

	try:
		# Get all the pages.
		allpages = Page.objects.order_by('sort_order')

		# Get default subpages.
		defaultsubpages = Subpage.objects.filter(sort_order=1)

		# Get all the subpages.
		allsubpages = Subpage.objects.filter(rootpage__path__exact=page).order_by('sort_order')

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

		news,lastnew=get_news()

	except ValueError, err:
		error(err)

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
	except (TemplateDoesNotExist,ValueError), err:
		try:
			template = get_template("default.html")
		except (TemplateDoesNotExist,ValueError), err:
			error(err)

	# Find the pages.
	try:
		# Get all the pages.
		allpages = Page.objects.order_by('sort_order')

		# Get default subpages.
		defaultsubpages = Subpage.objects.filter(sort_order=1)

		# Get all the top subpages.
		parent_subpages = Subpage.objects.filter(rootpage__path__exact=page, is_top=True).order_by('sort_order')

		# Get the current parent subpage (which may or may not be the current subpage, i.e. if the current is a child)
		# Assume that the path formed by page/subpage is unique for every subpage
		current_subpage = Subpage.objects.filter(rootpage__path__exact=page, path__exact=subpage)[0]
		if current_subpage.is_top == True:
			current_parent = current_subpage
		else:
			for parent in parent_subpages:
				# Assume every child subpage only has one parent
				if current_subpage in parent.children.all():
					current_parent = parent

		if subpage=="downloads":
			# Get all the releases.
			articles = New.objects.order_by('-sg_ver')
		else :
			# Get the articles that are in page/subpage.
			articles = Article.objects.filter(rootsubpage__rootpage__path__exact=page, rootsubpage__path__exact=subpage)

		news, lastnew=get_news()
	except (IndexError,ValueError) as err:
		error(err)

	return HttpResponse(template.render(Context({'current_page_path' : page,
												 'current_subpage_path' : subpage,
												 'default_subpages' : defaultsubpages,
												 'all_pages' : allpages,
												 'parent_subpages' : parent_subpages,
												 'current_parent' : current_parent,
												 'articles' : articles,
		                                         'news' : news,
		                                         'lastnew' : lastnew})))
