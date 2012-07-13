from django.db import models

# Page class.
class Page (models.Model):
	path = models.CharField(max_length=20);
	title = models.CharField(max_length=20);
	order = models.IntegerField();
	defaultSubpagePath = models.CharField(max_length=20)

	def __unicode__(self):
		return self.title + " (" + self.path + ")"

# Subpage class.
class Subpage(models.Model):
	rootpage = models.ForeignKey(Page);
	path = models.CharField(max_length=20);
	title = models.CharField(max_length=20);
	order = models.IntegerField();
	description = models.TextField(max_length=200);

	def __unicode__(self):
		return "(" + self.rootpage.path + "/" + self.path + ") - " + self.title

# Articles class.
class Article (models.Model):
	rootsubpage = models.ForeignKey(Subpage, blank=True, null=True);
	order = models.IntegerField();
	date = models.DateField();
	time = models.TimeField();
	#image = models.ImageField();
	title = models.CharField(max_length=100);
	author = models.CharField(max_length=20);
	content = models.TextField();
	
	def __unicode__(self):
		return self.rootsubpage.rootpage.path + "/" + self.rootsubpage.path + " - " + self.title

# New class.
class New (models.Model):
	stored_date = models.CharField(max_length=20)
	sg_ver = models.CharField(max_length=20);          # Shogun version.
	sg_bver = models.CharField(max_length=20);         # Shogun bversion.
	libshogun_ver = models.CharField(max_length=20);   # Libshogun version.
	data_ver = models.CharField(max_length=20);        # Data version.
	param_ver = models.CharField(max_length=20);       # Parameter version
	updated_date = models.CharField(max_length=20, unique=True);  # Date
	content = models.TextField();                      # Content

	def __unicode__(self):
		return self.updated_date + ' - shogun ' + self.sg_ver

