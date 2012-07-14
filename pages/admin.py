
# Import objetts.
from pages.models import Article
from pages.models import Subpage
from pages.models import Page
from pages.models import New

from django.contrib import admin

# HTML Editor
class ArticleOptions(admin.ModelAdmin):
	class Media:
		js = ('../static/js/tiny_mce/tiny_mce.js',
			  '../static/js/editors/textfield.js')


# Objects editable by admin.
admin.site.register(Article, ArticleOptions)
admin.site.register(Subpage)
admin.site.register(Page)
admin.site.register(New)

