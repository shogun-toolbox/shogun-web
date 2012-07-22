from django.db import models

# Page class.
class Page (models.Model):
	path = models.CharField(max_length=20);
	title = models.CharField(max_length=20);
	order = models.IntegerField();
	defaultSubpagePath = models.CharField(max_length=20)

	def __unicode__(self):
		return str(self.title) + " (" + str(self.path) + ")"

# Subpage class.
class Subpage(models.Model):
	rootpage = models.ForeignKey(Page);
	path = models.CharField(max_length=20);
	title = models.CharField(max_length=20);
	order = models.IntegerField();
	description = models.TextField(max_length=200);

	def __unicode__(self):
		return "(" + str(self.rootpage.path) + "/" + str(self.path) + ") - " + str(self.title)

# Articles class.
class Article (models.Model):
	rootsubpage = models.ForeignKey(Subpage, blank=True, null=True);
	order = models.IntegerField();
	date = models.DateField();
	time = models.TimeField();
	title = models.CharField(max_length=100);
	author = models.CharField(max_length=20);
	content = models.TextField();
	
	def __unicode__(self):
		return str(self.rootsubpage.rootpage.path) + "/" + str(self.rootsubpage.path) + " - " + str(self.title)

# New class.
class New (models.Model):
	stored_date = models.DateTimeField(max_length=20)
	sg_ver = models.CharField(max_length=20);          # Shogun version.
	sg_bver = models.CharField(max_length=20);         # Shogun bversion.
	libshogun_ver = models.CharField(max_length=20);   # Libshogun version.
	libshogunui = models.CharField(max_length=20);	   # Libshogun UI.
	data_ver = models.CharField(max_length=20);        # Data version.
	param_ver = models.CharField(max_length=20);       # Parameter version
	updated_date = models.DateField(max_length=20, unique=True);  # Date
	author = models.CharField(max_length=20);          # Author
	mail = models.CharField(max_length=50);            # Mail

	ftp_source_code = models.CharField(max_length=500);     
	ftp_md5sum = models.CharField(max_length=500); 
	ftp_PGP_signature = models.CharField(max_length=500); 
	http_source_code = models.CharField(max_length=500); 
	http_md5sum = models.CharField(max_length=500); 
	http_PGP_signature = models.CharField(max_length=500); 

	content = models.TextField();                      # Content

	def __unicode__(self):
		return str(self.updated_date) + ' - shogun ' + str(self.sg_ver)