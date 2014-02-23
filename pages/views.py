# Create your views here.

from django.template.response import TemplateResponse

import shogun.settings as settings
import util.notebook
import util.demo
import util.matrix

from django.http import HttpResponse,Http404

# HTML rendering libraries.
from django.template.loader import get_template
from django.template import Context,TemplateDoesNotExist

# Data Base libraries.
from pages.models import NavBar
from pages.models import ShogunPage
from pages.models import Article
from pages.models import New

# Import the parser.
import os
import os.path
import parserHTML
import datetime
import calendar
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

def get_navbar():
	navbar = NavBar.objects.get()
	return navbar

class fake_page:
		def __init__(self, path):
				self.path = path

# ----------------------------------------------------------------------
#                                HOME
# ----------------------------------------------------------------------
# To render correctly the main view (home).
def home(request):
	try:
		navbar = get_navbar()
	except ValueError, err:
		error(err)

	all_entries=[]
	try:
		all_entries=util.demo.get_demos(False)
	except OSError:
		pass

	try:
		all_entries.extend(util.notebook.get_notebooks(False))
	except OSError:
		pass

	notebooks=[]
	for i in xrange(0,len(all_entries),4):
		notebooks.append(all_entries[i:(i+4)])

	# choose the template.
	template = get_template("home.html")

	try:
		# Parse the news.
		newsParser.parseNews()
		news,lastnew=get_news()
	except ValueError, err:
		error(err)

	return HttpResponse(template.render(Context({'current_page' : fake_page('home'),
																							 'navbar' : navbar,
																							 'news' : news,
																							 'notebooks' : notebooks,
																							 'lastnew' : lastnew})))


# ----------------------------------------------------------------------
#                             SHOW NEW
# ----------------------------------------------------------------------
# To render correctly the other views (about,documentation,contact,...)
def showNew(request,newID):
	try:
		navbar = get_navbar()
	except ValueError, err:
		error(err)

	# Choose the template.
	template = get_template("news.html")

	# Find the pages.
	try:
		# The new selected.
		articles = New.objects.get(pk=newID)
		news = get_news()[0]

	except ValueError, err:
		error(err)

	return HttpResponse(template.render(Context({'current_page' : fake_page('news/onenew'),
																							 'navbar' : navbar,
																							 'articles' : [articles],
													                     'news' : news})))

# ----------------------------------------------------------------------
#                             SHOW BIG PICTURE
# ----------------------------------------------------------------------
# To render correctly the other views (about,documentation,contact,...)
def showPicture(request,pictureName):
	try:
		navbar = get_navbar()
	except ValueError, err:
		error(err)

	# Choose the template.
	template = get_template("bigpicture.html")

	# Find the pages.
	try:
		# Get picture url.
		picture_url = "/static/figures/" + pictureName

	except ValueError, err:
		error(err)

	return HttpResponse(template.render(Context({'current_page' : fake_page('bigpicture'),
												 'navbar' : navbar,
												 'picture_name' : pictureName,
												 'picture_url' : picture_url})))


def irclog(request, year, month, day):
	try:
		navbar = get_navbar()
	except ValueError, err:
		error(err)

	fname = '%s/#shogun.%s-%s-%s.log.html'  % (settings.SHOGUN_IRCLOGS, year, month, day)
	try:
		template = get_template("irclogs.html")

		news = get_news()[0]
		html=file(fname).read()
		soup = BeautifulSoup(html)
		logfile=str(soup.body.table)
	except Exception, err:
		error(err)

	return HttpResponse(template.render(Context({'current_page' : fake_page('contact/irc/irclogs'),
												 'navbar' : navbar,
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
	try:
		navbar = get_navbar()
	except ValueError, err:
		error(err)

	logfiles = [ f.replace('#shogun.','').replace('.log.html','') for f in os.listdir(settings.SHOGUN_IRCLOGS) if f.startswith('#shogun') ]
	logfiles.sort()

	try:
		template = get_template("irclogs.html")

		# Get all the pages.
		news = get_news()[0]
		all_entries = get_calendar_logs(logfiles)

	except IOError, err:
		error(err)

	return HttpResponse(template.render(Context({'current_page' : fake_page('contact/irc/irclogs'),
												 'navbar' : navbar,
												 'irclogfiles' : all_entries,
		                      'news' : news})))

def matrix(request):
	try:
		navbar = get_navbar()
	except ValueError, err:
		error(err)

	news = get_news()[0]

	details={'current_page' : fake_page('documentation/features'),
			 'navbar' : navbar,
			 'news' : news,
			 'table' : util.matrix.get_matrix(),
			 'related' : util.matrix.get_related_projects()
			 }

	return TemplateResponse(request, 'matrix.html', details)

def demo(request):
	try:
		navbar = get_navbar()
	except ValueError, err:
		error(err)

	try:
		template = get_template("notebooks.html")
		news = get_news()[0]
		all_entries = util.demo.get_demos()

	except IOError, err:
		error(err)

	return HttpResponse(template.render(Context({'current_page' : fake_page('documentation/demo'),
												 'navbar' : navbar,
												 'notebooks' : all_entries,
												 'news' : news})))

def notebook(request):
	try:
		navbar = get_navbar()
	except ValueError, err:
		error(err)

	try:
		template = get_template("notebooks.html")
		news = get_news()[0]
		all_entries = util.notebook.get_notebooks()

	except IOError, err:
		error(err)

	return HttpResponse(template.render(Context({'current_page' : fake_page('documentation/notebook'),
												 'navbar' : navbar,
												 'notebooks' : all_entries,
												 'news' : news})))

def markdown(request, mdfile):
	try:
		navbar = get_navbar()
	except ValueError, err:
		error(err)

	page='documentation'
	markdown_requested=mdfile.replace('.md','')

	try:
		template = get_template("markdown.html")

	except IOError, err:
		error(err)

	return HttpResponse(template.render(Context({'current_page_path' : page,
							'current_subpage_path' : markdown_requested,
							'navbar' : navbar,
							'html_fname' : "md2html/%s.html" % markdown_requested})))

def planet(request):
	try:
		navbar = get_navbar()
	except ValueError, err:
		error(err)

	try:
		template = get_template("planet.html")

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

	return HttpResponse(template.render(Context({'current_page' : fake_page('planet/shogun'),

												 'navbar' : navbar,
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
	try:
		navbar = get_navbar()
	except ValueError, err:
		error(err)

	# Set the page we are.
	page = "news"

	# choose the news template.
	template = get_template(page + ".html")

	articles=[]
	news=[]
	lastnew=[]

	try:
		# Get all the pages.
		allpages = ShogunPage.objects.all()

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

	return HttpResponse(template.render(Context({'current_page' : fake_page(page+'/'+subpage),
												 'navbar' : navbar,
												 'articles' : articles,
		                     'news' : news,
		                     'lastnew' : lastnew})))

# ----------------------------------------------------------------------
#                             PAGE HANDLER
# ----------------------------------------------------------------------
# To render correctly the other views (about,documentation,contact,...)
def pageHandler(request,page,subpage):
	try:
		navbar = get_navbar()
	except ValueError, err:
		error(err)

	# Choose the template.
	try:
		template = get_template(page + ".html")
	except (TemplateDoesNotExist,ValueError), err:
		try:
			template = get_template("default.html")
		except (TemplateDoesNotExist,ValueError), err:
			error(err)

	# Get the page
	try:
		page = ShogunPage.objects.get(path__exact=page+'/'+subpage)

		if subpage=="downloads":
			# Get all the releases.
			articles = New.objects.order_by('-sg_ver')
		else :
			# Get the articles that are in page/subpage.
			articles = Article.objects.filter(shogunpage=page)
		news, lastnew=get_news()

	except(IndexError,ValueError) as err:
		error(err)

	return HttpResponse(template.render(Context({'current_page' : page,
												                       'articles' : articles,
												                       'navbar' : navbar,
		                                           'news' : news,
		                                           'lastnew' : lastnew})))

def docredirect(request, doc):
    from django.http import HttpResponseRedirect
    if not doc.startswith('SG') and not doc.startswith('C'):
        doc="C" + doc
    return HttpResponseRedirect('http://www.shogun-toolbox.org/doc/en/latest/classshogun_1_1%s.html' % doc)
