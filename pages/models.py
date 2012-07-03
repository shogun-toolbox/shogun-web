from django.db import models

# Page class.
class Page (models.Model):
	page = models.TextField(primary_key=True);
	subpage = models.TextField();
	url = models.TextField();
	content = models.TextField();

# Photo class.
class Photo (models.Model):
	title = models.TextField(primary_key=True);
	url = models.TextField();
	width = models.IntegerField();
	height = models.IntegerField();
	POSITION = (
        ('center', 'center'),
        ('left', 'left'),
        ('rigth', 'right'),
    )
	position = models.CharField(max_length=6, choices=POSITION);

# Articles class.
class Article (models.Model):
	order = models.IntegerField();
	page = models.CharField(max_length=20);
	category = models.CharField(max_length=20);
	date = models.DateField();
	author = models.CharField(max_length=20);
	title = models.CharField(max_length=100);
	content = models.TextField();
	
	def __unicode__(self):
		return self.page + "/" + self.category + " - " + self.title
