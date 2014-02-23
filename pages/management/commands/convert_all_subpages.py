from django.core.management.base import NoArgsCommand
from pages.models import Subpage, Page, ShogunPage, Article

class Command(NoArgsCommand):
  def handle_noargs(self, **options):
    for subpage in Subpage.objects.filter():

      sp = ShogunPage()
      sp.title = subpage.title
      sp.path = subpage.rootpage.path + '/' + subpage.path
      sp.nav_tab = subpage.rootpage.path.capitalize()
      sp.description = subpage.description

      sp.save()

      for article in Article.objects.filter(rootsubpage__rootpage__path__exact=subpage.rootpage.path, rootsubpage__path__exact=subpage.path):
        article.shogunpage_id = sp.id
        article.save()

