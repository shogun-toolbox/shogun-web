#!/usr/bin/python
from xml.sax.handler import ContentHandler
from xml.sax import make_parser

#Import libraries.
from email.utils import parsedate
from datetime import datetime
from datetime import timedelta
import os
import time

#Import elements needed for the database.
from pages.models import New

class myContentHandler(ContentHandler):

    ## 
    # Method that is called when the object is created.
    ##
    def __init__ (self, lastStoredDate):

        #General variables.
        self.DEBUG = True

        # Create the sax parser.
        self.theParser = make_parser()
        self.theParser.setContentHandler(self)

        # Folder where the news are stored.
        self.newsfolder = 'news'

        # Last day we stored the news.
        self.lastStoredDate = lastStoredDate

        # Getting paths.
        self.filepath = os.path.abspath(__file__)
        self.rootpath = "/".join(self.filepath.split("/")[0:-1])
        self.newspath = self.rootpath + "/" + self.newsfolder

        # Print information
        if self.DEBUG:
            print("The absolute path for news is " + self.newspath)

        #New's Variables.
        self.sg_ver = ""                # Shogun version.
        self.in_sg_ver = False

        self.sg_bver = ""               # Shogun bversion.
        self.in_sg_bver = False

        self.libshogun_ver = ""         # Libshogun version.
        self.in_libshogun_ver = False

        self.data_ver = ""              # Data version.
        self.in_data_ver = False

        self.param_ver = ""             # Param version.
        self.in_param_ver = False

        self.updated_date = ""          # Updated date. 
        self.in_updated_date = False

        self.author = ""                # Updated date. 
        self.in_author = False

        self.mail= ""                   # Updated date. 
        self.in_mail = False

        self.libshogunui= ""            # Libshogun ui.
        self.in_libshogunui = False

        self.content = ""               # Content.
        self.in_content = False

        #In new variable.
        self.in_New = False
        
    ##
    # Method called when a element starts.
    ##
    def startElement (self, name, attrs):
        if name == 'new':
            self.in_New = True
        elif self.in_New:
            if name == 'sg_ver':
                self.in_sg_ver = True
            elif name == 'sg_bver': 
                self.in_sg_bver = True
            elif name == "libshogun_ver":
                self.in_libshogun_ver = True
            elif name == "data_ver":
                self.in_data_ver = True
            elif name == "param_ver":
                self.in_param_ver = True
            elif name == "updated_date":
                self.in_updated_date = True
            elif name == "author":
                self.in_author = True
            elif name == "mail":
                self.in_mail = True
            elif name == "libshogunui":
                self.in_libshogunui = True       
            elif name == "content":
                self.in_content = True
           
    ##
    # Method called when a element ends.
    ##
    def endElement (self, name):
        if name == 'new':
            self.in_New = False

            # New structure.
            # <new>
            #   <sg_ver> 0.0.0 </sg_ver>
            #   <sg_bver> 0.0.0 </sg_bver>
            #   <libshogun_ver> 0.0 </libshogun_ver>
            #   <data_ver> 0.0 </data_ver>
            #   <param_ver> 0.0 </param_ver>
            #   <updated_date> 00.00.0000 </updated_date>
            #   <content>
            #       * This release contains several enhancements, cleanups and bugfixes:
            #       * Features:
            #           - Implement set_linear_classifier for static interfaces.
            #           - Implement Polynomial DotFeatures.
            #       * Bugfixes:
            #           - Fix one class MKL for static interfaces.
            #   </content>
            # <new>

            #Give format to the content.
            self.content = self.content.encode('utf8','replace')

            #Add html code.
            self.addHTMLContent()

            #Save in DB.
            updated_date = datetime.strptime(self.updated_date, "%Y-%m-%d")

            try:
                record = New.objects.get(updated_date=updated_date)
                record.stored_date = datetime.now()
                record.sg_ver = self.sg_ver
                record.sg_bver = self.sg_bver
                record.libshogun_ver = self.libshogun_ver
                record.data_ver = self.data_ver
                record.param_ver = self.param_ver
                record.updated_date = updated_date
                record.author = self.author
                record.mail = self.mail
                record.content = str(self.content)
                record.save()

                if self.DEBUG:
                    print ("New modified!")


            except New.DoesNotExist:
                record = New(stored_date=datetime.now(), \
                            sg_ver=self.sg_ver, \
                            sg_bver=self.sg_bver, \
                            libshogun_ver=self.libshogun_ver, \
                            data_ver=self.data_ver, \
                            param_ver=self.param_ver, \
                            updated_date=updated_date, \
                            author=self.author, \
                            mail=self.mail, \
                            content=self.content)
                record.save()


                if self.DEBUG:
                    print ("New added!")

            #Reset the values.
            self.sg_ver = ""                # Shogun version.
            self.sg_bver = ""               # Shogun bversion.
            self.libshogun_ver = ""         # Libshogun version.
            self.data_ver = ""              # Data version.
            self.param_ver = ""             # Param version.
            self.updated_date = ""          # Updated date. 
            self.content = ""               # Content.

        elif self.in_New:
            if name == 'sg_ver':
                self.in_sg_ver = False  
            elif name == 'sg_bver': 
                self.in_sg_bver = False
            elif name == "libshogun_ver":
                self.in_libshogun_ver = False
            elif name == "data_ver":
                self.in_data_ver = False
            elif name == "param_ver":
                self.in_param_ver = False
            elif name == "updated_date":
                self.in_updated_date = False
            elif name == "author":
                self.in_updated_date = False
            elif name == "mail":
                self.in_updated_date = False
            elif name == "libshogunui":
                self.in_linshogunui = False
            elif name == "content":
                self.in_content = False         

    ##
    # Method called when we are inside an element.
    ##
    def characters (self, chars):
        if self.in_sg_ver:
            self.sg_ver = self.sg_ver + chars

        if self.in_sg_bver:
            self.sg_bver = self.sg_bver + chars
 
        if self.in_libshogun_ver:
            self.libshogun_ver = self.libshogun_ver + chars

        if self.in_data_ver:
            self.data_ver = self.data_ver + chars

        if self.in_param_ver:
            self.param_ver = self.param_ver + chars

        if self.in_updated_date:
            self.updated_date = self.updated_date + chars

        if self.in_author:
            self.author = self.author + chars

        if self.in_mail:
            self.mail = self.mail + chars

        if self.in_libshogunui:
            self.libshogunui = self.libshogunui + chars

        if self.in_content:
            self.content = self.content + chars

    ##
    # Method that parse the news.
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

        print(path)

        #Tuples of date.
        timestamp = os.path.getmtime(path)
        mdate = time.gmtime(timestamp)
        ldate = self.lastStoredDate.timetuple()

        #If the modified date is more recent
        if (mdate>ldate):
            self.theParser.parse(path)

    ##
    # Add html to the content.
    ##
    def addHTMLContent(self):

        auxcontent = self.content.split("\n")
            
        self.content = ""
        stop_tag_ul=''
        stop_tag_li=''
        for l in auxcontent:
            s = l.lstrip().rstrip()
            if s.startswith('* This'):
                self.content+=''+s.lstrip('* ')+'\n<ul>\n'
            elif s.startswith('* '):
                self.content+=stop_tag_li + stop_tag_ul
                self.content+='<li><h5>'+s.lstrip('* ')+'</h5>\n<ul>'
                stop_tag_li=''
                stop_tag_ul='</ul></li>\n'
            elif s.startswith('-'):
                self.content+=stop_tag_li
                self.content+='<li>'+s.lstrip('- ')
                stop_tag_li='</li>\n'
            else:
                self.content+=' ' +s.lstrip()

        self.content+=stop_tag_li + stop_tag_ul + '</ul>\n' + '\n'