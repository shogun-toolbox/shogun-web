from django.db import models

class NavBar(models.Model):
	html = models.TextField();

	def __unicode__(self):
	  return str("NavBar")


class ShogunPage(models.Model):
	title = models.CharField(max_length=20);
	path = models.CharField(max_length=40);
	nav_tab = models.CharField(max_length=20);
	description = models.TextField(max_length=200);

	def __unicode__(self):
		return str(self.title) + " (" + str(self.path) + ")" + "  >> " + self.nav_tab


class Article (models.Model):
	rootsubpage = models.IntegerField(blank=True, null=True);
	shogunpage = models.ForeignKey(ShogunPage, blank=True, null=True);
	sort_order = models.IntegerField();
	date = models.DateField();
	time = models.TimeField();
	title = models.CharField(max_length=100);
	author = models.CharField(max_length=20);
	content = models.TextField();

	def __unicode__(self):
		return str(self.shogunpage.path) + " - " + str(self.title)


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

	ftp_data = models.CharField(max_length=500, null=True);
	ftp_source_code = models.CharField(max_length=500);
	ftp_md5sum = models.CharField(max_length=500);
	ftp_PGP_signature = models.CharField(max_length=500);
	http_data = models.CharField(max_length=500, null=True);
	http_source_code = models.CharField(max_length=500);
	http_md5sum = models.CharField(max_length=500);
	http_PGP_signature = models.CharField(max_length=500);

	content = models.TextField();                      # Content

	class Meta:
		ordering = ['-updated_date']

	def __unicode__(self):
		return str(self.updated_date) + ' - shogun ' + str(self.sg_ver)
