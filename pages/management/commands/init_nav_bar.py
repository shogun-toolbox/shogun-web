from django.core.management.base import NoArgsCommand
from pages.models import NavBar

class Command(NoArgsCommand):
  def handle_noargs(self, **options):
    nav = NavBar()

    nav.html = """
    <ul class="nav nav-tabs">
      <li><a href="/page/home/"><span>Home</span></a></li>
      <li class="dropdown">
        <a class="dropdown-toggle" data-toggle="dropdown" href="#">About<span class="caret"></span></a>
        <ul class="dropdown-menu">
          <li><a href="/page/about/information">Information</a></li>
          <li><a href="/page/about/ourteam">Our Team</a></li>
          <li><a href="/page/about/license">License</a></li>
          <li><a href="/page/about/contributions">Contributions</a></li>
          <li><a href="/page/about/examples">Examples</a></li>
<<<<<<< HEAD
          <li><a href="/page/about/related/">Related Projects</a></li>
=======
          <li><a href="/page/aboutrelated/">Related Projects</a></li>
>>>>>>> moved navbar to the db
        </ul>
      </li>
      <li><a href="/page/features/"><span>Features</span></a></li>
      <li class="dropdown">
        <a class="dropdown-toggle" data-toggle="dropdown" href="#">Documentation<span class="caret"></span></a>
        <ul class="dropdown-menu">
          <li><a href="/page/documentation/information"><span>Information</span></a></li>
          <li><a href="/page/documentation/dev"><span>Developer</span></a></li>
            <li><a href="/page/documentation/contribute"><span> * Contribute</span></a></li>
            <li><a href="/page/documentation/resources"><span> * Resources</span></a></li>
          <li><a href="/page/documentation/faq"><span>FAQ</span></a></li>
          <li><a href="/page/documentation/notebook"><span>Notebook</span></a></li>
          <li><a href="/page/documentation/demo"><span>Demo</span></a></li>
        </ul>
      </li>
      <li><a href="/page/contact/contacts"><span>Contact</span></a></li>
      <li><a href="/page/planet/shogun"><span>Planet</span></a></li>
      <li class="dropdown">
        <a class="dropdown-toggle" data-toggle="dropdown" href="#">News<span class="caret"></span></a>
        <ul class="dropdown-menu">
          <li><a href="/page/news/onenew"><span>New</span></a></li>
          <li><a href="/page/news/2012"><span>2012</span></a></li>
          <li><a href="/page/news/2011"><span>2011</span></a></li>
          <li><a href="/page/news/2010"><span>2010</span></a></li>
          <li><a href="/page/news/2009"><span>2009</span></a></li>
          <li><a href="/page/news/2008"><span>2008</span></a></li>
          <li><a href="/page/news/2007"><span>2007</span></a></li>
          <li><a href="/page/news/2006"><span>2006</span></a></li>
          <li><a href="/page/news/newslist"><span>All News</span></a></li>
        </ul>
      </li>
      <li class="dropdown">
        <a class="dropdown-toggle" data-toggle="dropdown" href="#">Events<span class="caret"></span></a>
        <ul class="dropdown-menu">
          <li><a href="/page/Events/workshop2013"><span>Workshop 2013</span></a></li>
            <li><a href="/page/Events/worskhop13_follow_up"><span> * Follow-Up</span></a></li>
            <li><a href="/page/Events/workshop2013_videos"><span> * Videos</span></a></li>
            <li><a href="/page/Events/workshop2013_program"><span> * Program</span></a></li>
            <li><a href="/page/Events/registration"><span> * Registration</span></a></li>
          <li><a href="/page/Events/gsoc2013"><span>GSoC2013</span></a></li>
            <li><a href="/page/Events/gsoc2013_ideas"><span> * Ideas</span></a></li>
          <li><a href="/page/Events/gsoc2012"><span>GSoC2012</span></a></li>
            <li><a href="/page/Events/gsoc2012_follow_up"><span> * Follow-Up</span></a></li>
            <li><a href="/page/Events/gsoc2012_ideas"><span> * Ideas</span></a></li>
          <li><a href="/page/Events/gsoc2012"><span>GSoC2011</span></a></li>
            <li><a href="/page/Events/gsoc2011_follow_up"><span> * Follow-Up</span></a></li>
            <li><a href="/page/Events/gsoc2011_ideas"><span> * Ideas</span></a></li>
        </ul>
      </li>
    </ul>
    """

    nav.save()

