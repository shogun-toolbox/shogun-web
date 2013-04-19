from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shogun.views.home', name='home'),
    # url(r'^shogun/', include('shogun.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Other urls:

    # News
    url(r'^page/news/(?P<subpage>[\w|\d]+)', 'pages.views.news'),

    # Weblog
    url(r'^page/planet/', 'pages.views.planet'),

    # irclogs
    url(r'^page/contact/irclogs/', 'pages.views.irclogs'),

    # irclog
    url(r'^page/contact/irclog/(?P<year>[\d]+)-(?P<month>[\d]+)-(?P<day>[\d]+)/', 'pages.views.irclog'),

    # Subpages.
    url(r'^page/(?P<page>[\w|\d]+)/(?P<subpage>[\w|\d]+)', 'pages.views.pageHandler'),

    # Big pictures.
    url(r'^bigpicture/(?P<pictureName>.+)', 'pages.views.showPicture'),

    # One new selected (ID):
    url(r'^new/(?P<newID>[\w|\d]+)', 'pages.views.showNew'),

    # Demos
    url(r'^demo/(?P<demo_name>[\w|\d]+)/(?P<function>[\w|\d]+)', 'pages.views.demoHandler'),

    # Main page.
    (r'^', 'pages.views.home'),
)
