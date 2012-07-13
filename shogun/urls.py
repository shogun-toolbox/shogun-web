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
    # Subpages.
    url(r'^home', 'pages.views.home'),
    url(r'^page/(?P<page>[\w|\d]+)/(?P<subpage>[\w|\d]+)', 'pages.views.pageHandler'),

    # News:
    url(r'^new/(?P<newID>[\w|\d]+)', 'pages.views.showNew'),

    # Main page.
    (r'^', 'pages.views.home'),
)
