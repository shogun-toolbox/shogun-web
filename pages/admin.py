from pages.models import Article
from pages.models import Subpage
from pages.models import Page
from pages.models import New

from django.contrib import admin

admin.site.register(Article)
admin.site.register(Subpage)
admin.site.register(Page)
admin.site.register(New)