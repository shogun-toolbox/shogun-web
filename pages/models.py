from django.db import models

# Page class.
class Page (models.Model):
	path = models.CharField(max_length=20);
	title = models.CharField(max_length=20);
	sort_order = models.IntegerField();
	defaultSubpagePath = models.CharField(max_length=20)

	class Meta:
		ordering = ['sort_order']

	def __unicode__(self):
		return str(self.title) + " (" + str(self.path) + ")"

# Subpage class.
# TODO raise an error if a child subpage is assigned to more than one parent
# TODO raise an error if a subpage with at least one child is assigned as child of a subpage
class Subpage(models.Model):
	rootpage = models.ForeignKey(Page);
	path = models.CharField(max_length=20);
	title = models.CharField(max_length=20);
	sort_order = models.IntegerField();
	description = models.TextField(max_length=200);
	# Children subpages - allows to nest a group of subpages in a parent subpage
	# Non symmetrical because for the relationship parent -> child the direction matters
	# null and blank because no subpage is compulsed to have children
	# Although the model allows it, no subpage should have more than one parent
	children = models.ManyToManyField('self', symmetrical=False, null=True, blank=True)
	# Whether a subpage is to be shown in the top level
	is_top = models.BooleanField('Is top subpage?', default=True)

	class Meta:
		ordering = ['rootpage__sort_order','sort_order']

	def __unicode__(self):
		return "(" + str(self.rootpage.path) + "/" + str(self.path) + ") - " + str(self.title)

# Articles class.
class Article (models.Model):
	rootsubpage = models.ForeignKey(Subpage, blank=True, null=True);
	sort_order = models.IntegerField();
	date = models.DateField();
	time = models.TimeField();
	title = models.CharField(max_length=100);
	author = models.CharField(max_length=20);
	content = models.TextField();
	
	class Meta:
		ordering = ['rootsubpage__rootpage__sort_order','rootsubpage__sort_order','sort_order']

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
