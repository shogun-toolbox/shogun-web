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

# Global variables.
releasePathDataFTP = "ftp://shogun-toolbox.org/shogun/data/"
releasePathDataHTTP = "http://shogun-toolbox.org/archives/shogun/data/"
releasePathFTP = "ftp://shogun-toolbox.org/shogun/releases/"
releasePathHTTP = "http://shogun-toolbox.org/archives/shogun/releases/"

class myContentHandler(ContentHandler):

    ## 
    # Method that is called when the object is created.
    ##
    def __init__ (self):

        #General variables.
        self.DEBUG = False

        # Create the sax parser.
        self.theParser = make_parser()
        self.theParser.setContentHandler(self)

        # Folder where the news are stored.
        self.newsfolder = 'news'

        # Last day we stored the news.
        try:
            lastStoredDate = New.objects.order_by('-stored_date')[0].stored_date
        except:
            lastStoredDate = datetime(2000, 1, 1, 10, 10, 10)

        self.lastStoredDate = lastStoredDate.timetuple()

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

        #In 'new' variable.
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

            #If now value in new should be 0.0.
            if self.sg_ver == '':
                self.sg_ver = '0.0.0'
            if self.sg_bver == '':
                self.sg_bver = '0.0.0'
            if self.libshogun_ver == '':
                self.libshogun_ver = '0.0'
            if self.data_ver == '':
                self.data_ver = '0.0'
            if self.param_ver == '':
                self.param_ver = '0.0'
            if self.libshogunui == '':
                self.libshogunui = '0.0'
      
            # Add the new to the database.
            self.addNew()

            #Reset the values.
            self.sg_ver = ""                # Shogun version.
            self.sg_bver = ""               # Shogun bversion.
            self.libshogun_ver = ""         # Libshogun version.
            self.data_ver = ""              # Data version.
            self.param_ver = ""             # Param version.
            self.libshogunui = ""           # Libshogunui version.
            self.updated_date = ""          # Updated date. 
            self.content = ""               # Content.
            self.mail = ""
            self.author = ""

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
                self.in_author = False
            elif name == "mail":
                self.in_mail = False
            elif name == "libshogunui":
                self.in_libshogunui = False
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

        if self.DEBUG:
            print ("Last stored date : " + time.strftime("%Y-%m-%d %H:%M:%S", self.lastStoredDate))
        
        # Parse forlder recursively.
        self.parseFolder(self.newspath)

        # Set the last stored date to the actual date (Solve the
        # problem of loading news and not reset the server, note
        # that we need at least one second of difference).
        time.sleep(1)
        self.lastStoredDate = datetime.now().timetuple()

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

        #Tuples of date.
        timestamp = os.path.getmtime(path)
        mdate = time.localtime(timestamp)

        #Information.
        if self.DEBUG:
            print(path + " -> " + time.strftime("%Y-%m-%d %H:%M:%S", mdate))

        #If the modified date is more recent than the last stored date.
        if (mdate>self.lastStoredDate):

            # Change the modify and access time tu current time. (Solve problems 
            # of reloading news all the times if times in computer are not equals).
            os.utime(path,None)

            self.theParser.parse(path)

    ##
    # Add html to the content.
    ##
    def addHTMLContent(self):

        auxcontent = self.content.split("\n")
            
        self.content = ""
        stop_tag_ul=''
        stop_tag_li=''
        first = True

        for l in auxcontent:
            s = l.lstrip().rstrip()
            if s.startswith('* This') and first:
                self.content+=''+s.lstrip('* ')+'\n<ul>\n'
                first = False
            elif s.startswith('* ') and first:
                self.content+='<ul><li><h5>'+s.lstrip('* ')+'</h5>\n<ul>'
                stop_tag_li=''
                stop_tag_ul='</ul></li>\n'
                first = False
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


    ##
    # Add new
    ##
    def addNew(self):

        # Updated date in same format that database updated_date.
        updated_date = datetime.strptime(self.updated_date, "%Y-%m-%d")

        # The root version (0.5.1 -> 0.5)
        version = ".".join(self.sg_ver.split(".")[0:-1])

        # Create the path.
        ftpPath = releasePathFTP + version + "/sources/shogun-" + self.sg_ver
        httpPath = releasePathHTTP + version + "/sources/shogun-" + self.sg_ver
        ftpDataPath = releasePathDataFTP + "shogun-data-" + self.data_ver
        httpDataPath = releasePathDataHTTP + "shogun-data-" + self.data_ver

        try:
            record = New.objects.get(updated_date=updated_date)
            record.stored_date = datetime.now()
            record.sg_ver = self.sg_ver
            record.sg_bver = self.sg_bver
            record.libshogun_ver = self.libshogun_ver
            record.data_ver = self.data_ver
            record.param_ver = self.param_ver
            record.libshogunui = self.libshogunui
            record.author = self.author
            record.mail = self.mail
            record.content = str(self.content)
            record.ftp_data=ftpDataPath + ".tar.bz2"
            record.http_data=httpDataPath + ".tar.bz2"
            record.ftp_source_code=ftpPath + ".tar.bz2"
            record.http_source_code=httpPath + ".tar.bz2"
            record.ftp_md5sum=ftpPath + ".md5sum"
            record.http_md5sum=httpPath + ".md5sum"
            record.ftp_PGP_signature=ftpPath + ".tar.bz2.gpg"
            record.http_PGP_signature=httpPath + ".tar.bz2.gpg"

            # Add release download links.
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
                         libshogunui=self.libshogunui,
                         updated_date=updated_date, \
                         author=self.author, \
                         mail=self.mail, \
                         content=self.content, \
                         ftp_data=ftpDataPath + ".tar.bz2", \
                         http_data=httpDataPath + ".tar.bz2", \
                         ftp_source_code=ftpPath + ".tar.bz2", \
                         http_source_code=httpPath + ".tar.bz2", \
                         ftp_md5sum=ftpPath + ".md5sum", \
                         http_md5sum=httpPath + ".md5sum", \
                         ftp_PGP_signature=ftpPath + ".tar.bz2.gpg", \
                         http_PGP_signature=httpPath + ".tar.bz2.gpg")
            record.save()


            if self.DEBUG:
                print ("New added!")

    ##
    # Add related release
    ##
    def addRelatedRelease(self):

        try:
            record = Release.objects.get(sg_ver = self.sg_ver)

            if self.DEBUG:
                print ("Release " + self.sg_ver + " already exists.")
            
        except Release.DoesNotExist:

            # The root version (0.5.1 -> 0.5)
            version = ".".join(self.sg_ver.split(".")[0:-1])

            # Create the path.
            ftpPath = releasePathFTP + version + "/sources/shogun-" + self.sg_ver
            httpPath = releasePathHTTP + version + "/sources/shogun-" + self.sg_ver

            record = Release(sg_ver=self.sg_ver, \
                             ftp_source_code=ftpPath + ".tar.bz2", \
                             http_source_code=httpPath + ".tar.bz2", \
                             ftp_md5sum=ftpPath + ".md5sum", \
                             http_md5sum=httpPath + ".md5sum", \
                             ftp_PGP_signature=ftpPath + ".tar.bz2.gpg", \
                             http_PGP_signature=httpPath + ".tar.bz2.gpg")
            record.save()

            if self.DEBUG:
                print ("Release " + self.sg_ver + " added.")
