#!/usr/bin/python

# Libraries.
import os
import os.path
import time
from datetime import datetime

#Import elements needed for the database.
from pages.models import New

class newsParser():

	## 
	# Method that is called when the object is created.
	##
	def __init__ (self):
		
		# General variables.
		self.DEBUG = False

		self.newsfolder = 'news'

		self.filepath = os.path.abspath(__file__)
		self.rootpath = "/".join(self.filepath.split("/")[0:-1])
		self.newspath = self.rootpath + "/" + self.newsfolder

		# Print information
		if self.DEBUG:
			print("The absolute path for news is " + self.newspath)


	##
	# Thethos thar parse the news.
	##
	def parseNews(self):
		self.parseFolder(self.newspath)

	##
	# Method that list the content of the folder.
	##
	def parseFolder(self, path):

		# List files in root.
		filesList = os.listdir(path)

		# Check if is a file or a directory
		for file in filesList:
			abspath = path + "/" + file

			if (os.path.isdir(abspath) == True):
				self.parseFolder(abspath)
			else:
				self.parseFile(abspath)

	##
	# Method that parse one file.
	##
	def parseFile(self, path):

		if self.DEBUG:
			# Print information.
			print("Parsing file : " + path)

		# News structure.
		sg_ver='0.0.0'            # Shogun version.
		sg_bver='0.0.0'           #
		libshogun_ver='0.0'       # Libshogun version.
		data_ver='0.0'            # Data version.
		param_ver='0.0'           # Parameter version
		updated_date='00.00.0000' # Date
		content=''                # Content

		# Tags.
		stop_tag_ul=''
		stop_tag_li=''
		news_start=False

		for l in file(path).readlines():
			if news_start:
				if l=='\n':
					break
				s=l.lstrip().rstrip()
				if s.startswith('* This'):
					content+=''+s.lstrip('* ')+'\n<ul>\n'
				elif s.startswith('* '):
					content+=stop_tag_li + stop_tag_ul
					content+='<li><h5>'+s.lstrip('* ')+'</h5>\n<ul>'
					stop_tag_li=''
					stop_tag_ul='</ul></li>\n'
				elif s.startswith('-'):
					content+=stop_tag_li
					content+='<li>'+s.lstrip('- ')
					stop_tag_li='</li>\n'
				else:
					content+=' ' +s.lstrip()
			else:
				if l.startswith("20"):
					updated_date='%s.%s.%s' % (l[8:10],l[5:7],l[0:4])
				elif l.find("* SHOGUN")!=-1:
					i=l.find("* SHOGUN")
					v=l[i+2:].split()
					sg_ver=v[3]
					sg_bver='.'.join(sg_ver.split('.')[0:2])
					libshogun_ver=v[5][:-1]
					data_ver=v[7][:-1]
					param_ver=v[9][:-1]
					news_start=True

		content+=stop_tag_li + stop_tag_ul + '</ul>\n' + '\n'

		# Save the new in DB.
		current_date = datetime.strftime(datetime.now(),'%d.%m.%Y');

		try:
			record = New.objects.get(updated_date=updated_date)
			record.stored_date = current_date
			record.sg_ver = sg_ver
			record.sg_bver = sg_bver
			record.libshogun_ver = libshogun_ver
			record.data_ver = data_ver
			record.param_ver = param_ver
			record.updated_date = updated_date
			record.content = content
			record.save()

		except New.DoesNotExist:
			record = New(stored_date=current_date, sg_ver=sg_ver, sg_bver=sg_bver, libshogun_ver=libshogun_ver, data_ver=data_ver, param_ver=param_ver, updated_date=updated_date, content=content)
			record.save()

			if self.DEBUG:
				print ("adding ...")
				print ("date:" + updated_date)
				print ("libshogun_ver:" + libshogun_ver) 
				print ("data_ver:" + data_ver)
				print ("param_ver:" + param_ver)
				print ("sg_ver:" + sg_ver)
				print ("sg_bver:" + sg_bver)
				print ("")