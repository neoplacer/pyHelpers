

#!/usr/bin/python
"""
 sitemap_html.py -- sythesize a site map from meta-description data

 This script is a port of Eric Raymond's sitemap script, which 
 was written in Perl.  Any cleverness was probably lifted directly
 from his original script.  In particular, I the indsort method 
 and the multilanguage support are based on corresponding elements 
 in Raymond's original sitemap.

 The config file should now be a file of Python statements.
 It should assign to a dictionary named 'configuration.'  
 For example, the following statement would change the homepage URL:
 configuration['homepage'] = 'http://www.python.org'
 The directories to exclude should be a tuple of strings corresponding 
 to directory names.  For example, 
 configuration['exclude'] = ('test', 'personal', 'jokes')

 The only "data structure" used in the code is the lightweight class PageInfo.
 The program builds a list of PageInfo instances.
 Each PageInfo instance looks like a dictionary with the keys, 
  'file', 'title', and 'desc'.

 Version 1.0.0  Initial revision

 By Thomas A. Bryan.  Copyright 1999.  Use and redistribute freely.
"""

import os
import re   # of course, we're translating from Perl ;)
import string  # to avoid unnecessary regexen
from UserDict import UserDict

__author__ = 'Tom Bryan   tbryan@python.net'
__version__ = (1,0,0)

############################################################
# Default "constants"
############################################################

# Author of sitemap.py
sitemap_author = 'Tom Bryan \
                  <tbryan AT python.net>'

# default configuration; this can be overridden with a config file
configuration = {'hometitle': "Tom's Home Page",
		 'indextitle': "Map of Tom's Starship Python Pages", 
		 'fullname': "Tom Bryan",
		 'mailaddr': "tbryan@python.net",
		 'homepage': "http://starship.python.net/~tbryan", 
		 'exclude': ("Test","test","oldstuff"),
		 'language': "english",
		 'icondirs': "",
		 'icontext': "",
		 'body': '<BODY BGCOLOR="#FFFFFF">' }

# Used by get_lang_msg.
lang_months = {
    'english': (
	'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'),
    'german': (
	'Jan','Feb','Mar','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dez'),
    'norwegian': (
	'Jan','Feb','Mar','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Des'),
    'swedish': ( # I'll have to ask Skot what these should be.
	'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
    }
    


############################################################
# Function declarations
############################################################

def get_lang_msg(lang):
    """get_lang_msg(lang) takes a string indicating one of several languages.
    It returns a dictionary of phrases for the sitemap page in the requested language.
    """
    # get the current UTC time as a Python time tuple
    import time
    (year, month, day, hour, minute, second, mday, yday, tz) = time.gmtime(time.time())
    # To get month abbreviations, we use a dictionary: lang->list of months.
    # We force the dictionary to be referenced from the global namespace just to be sure.
    # Then we create a months list by fetching from the dictionary with a default of
    # 'english'.  We could have also used an if,elif,elif,else...
    global lang_months
    months = lang_months.get(lang,lang_months['english'])    
    if (string.lower(lang) == 'german'):
	return {'sitemap': 'Site Map',
		'back_to': 'Zurueck zu',
		'autogen': 'Dieser Index wurde automatisch generiert aus Meta Tags\
		  aller Seiten. Top-Level-Seiten werden zuerst gelistet.',
		'toolgen': 'Diese Seite wurde generiert von "sitemap.py", \
		  geschrieben von %s.' % sitemap_author,
		'date'   : '%d %s %04d %02d:%02d' % (
		    mday, months[month-1], year,hour,minute)}
    else: # default to english if language is unknown
	return {'sitemap': 'Site Map',
		'back_to': 'Back to', 
		'autogen': 'This is an index automatically generated from meta tags \
		  present in each of the pages.  Top-level pages are listed first.',
		'toolgen': 'This page generated by "sitemap.py", written by %s.<BR> \
		  "sitemap.py" is based on "sitemap" by Eric S. Raymond.' % sitemap_author,
		'date'   : '%d %s %04d, at %d:%02d' % (
		    mday, months[month-1], year, hour, minute)}


def extract_file_desc(xtra,dir,files):
    """This function is used by os.path.walk to extract description information
    from html files.  It appends PageInfo instances to xtra[1].  
    xtra[0] is the list of files/directories to be excluded."""
    # Compile the regexen just once.
    # regex to get the description from a META tag
    desc_re = re.compile(
	r'<META\s*NAME\s?=\s?"DESCRIPTION"\s*CONTENT\s?=\s?"([^"]*)"',
	re.IGNORECASE)
    # regex to get the title from the TITLE tags.
    title_re = re.compile(r'<TITLE>([^<]*)</TITLE>',re.IGNORECASE)
    for file in files:
	title = None
	process_flag = 0
	fullpath = os.path.join(dir,file)
	# Only process files that end in .htm, .html, or .shtml and 
	# that don't have any of the strings from the exclude list, 
	# xtra[0], in their absolute path.
	if fullpath[-5:] in ('.html','shtml') or fullpath[-4:] == '.htm':
	    process_flag = 1
	for entry in xtra[0]:
	    if string.find(fullpath,entry) > -1:
		process_flag = 0
	# For files that we want to process, get the filename, title, and 
	#  description for use on the sitemap page.
	if process_flag:
	    inFile = open(fullpath,'r')
	    input = inFile.read()
	    inFile.close()
	    # replace all newlines with spaces in case tags span multiple lines
	    string.replace(input,'\012',' ') # !!!only works on UNIX?
	    # Find the title and description
	    desc_mo = desc_re.search(input)
	    title_mo = title_re.search(input)
	    # Just in case someone forgot a title
	    if title_mo != None:
		title = title_mo.group(1)
	    else:
		title = "No title"
	    # Don't index files without a 'description' META tag
	    if desc_mo != None:
		# Append a PageInfo instance with the  path 
		# (without the initial './'), the title, and the description
		xtra[1].append( PageInfo(fullpath[2:],title,desc_mo.group(1)) )

	
def indsort(x,y):
    """indsort(x,y)
    a special sorting method for the sitemap website indexing program
    It groups pages first by directory depth, then by directory, 
    and then alphabetically.
    index.html pages are sorted with the parent directory 
    as a representation of the subdirectory.
    x and y are tuples of the form (filename, title, description)."""    
    first = x['file']
    second = y['file']
    # sort index.html entries as the directory name in 
    # the parent directory
    if first[-10:] == 'index.html':
	first = first[:-11]
    if second[-10:] == 'index.html':
	second = second[:-11]
    # This forces grouping by subdirectory depth
    first = `string.count(first,os.sep)` + first
    second = `string.count(second,os.sep)` + second
    # With the preparation above, cmp() now does what we want
    return cmp(first,second)

def get_stem(page):
    """get_stem(page) takes a PageInfo instance and returns the 
    directory to the file.  If the file is an index file, its stem
    is considered to be one directory shallower (that is, it has the
    same stem as files in its parent directory."""
    (stem, filename) = os.path.split(page['file'])
    if (filename[:6] == 'index.'):
	(stem, filename) = os.path.split(stem)
    return stem


def generate_header(configuration, message):
    """generate_header(configuration, message):
    prints the header and first part of the body of the sitemap page.
    Both arguments are dictionaries.  The keys that will be used are:
    configuration:
     indextitle = Title of the sitemap page
     sitemap = "Site Mape" (possibly not in English)
     mailaddr = siteowner's e-mail address
     homepage = home page for this site
     hometitle = Title for the homepage
    message:
     body = the <BODY> tag, including any desired attributes
     back_to = "Back to" (possibly not in English)
     date = Date formatted according to some nationality's standard
     autogen = a message (possibly not in English) explaining how the sitemap was generated
    """
    # assign to locals for convenient interpolation into the return string
    indextitle = configuration['indextitle']
    mailaddr = configuration['mailaddr']
    homepage = configuration['homepage']
    hometitle = configuration['hometitle']
    body = configuration['body']
    sitemap = message['sitemap']
    back_to = message['back_to']
    date = message['date']
    autogen = message['autogen']
    # get a dictionary: localvar -> value
    local_strings = vars()
    return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
    <HTML>
      <HEAD>
        <TITLE>%(indextitle)s</TITLE>
        <META NAME="KEYWORDS" CONTENT="%(sitemap)s"> 
        <LINK REV=MADE HREF="mailto:%(mailaddr)s">
      </HEAD>
      %(body)s
      <TABLE WIDTH="100%%" CELLPADDING=0><TR>
        <TD WIDTH="50%%">%(back_to)s <A HREF="%(homepage)s">%(hometitle)s</A>
        <TD WIDTH="50%%" ALIGN=RIGHT>%(date)s
        </TR></TABLE>
      <HR><P>
      <H1 ALIGN=CENTER>%(sitemap)s</H1>
    
      <P>%(autogen)s
    
      <DL>\n""" % local_strings
    

def generate_footer(configuration, message):
    """generate_footer(configuration, message):
    prints the last part of the body of the sitemap page
    Both arguments are dictionaries.  The keys that will be used are:
    configuration:
     homepage = home page for this site
     hometitle = Title for the homepage
     fullname = siteowner's full name
     mailaddr = siteowner's e-mail address
    message:
     toolgen = a message (possibly not in English) saying what tool created the page
     back_to = "Back to" (possibly not in English)
     date = Date formatted according to some nationality's standard    
    """
    # assign to locals for convenient interpolation into the return string
    homepage = configuration['homepage']
    hometitle = configuration['hometitle']
    fullname = configuration['fullname']
    mailaddr = configuration['mailaddr']
    toolgen = message['toolgen']
    back_to = message['back_to']
    date = message['date']
    # get a dictionary: localvar -> value
    local_strings = vars()
    return """    </DL>
    <P>
    <HR>
    %(toolgen)s
    <HR>
    <TABLE WIDTH="100%%" CELLPADDING=0><TR>
      <TD WIDTH="50%%">%(back_to)s <A HREF="%(homepage)s">%(hometitle)s</A>
      <TD WIDTH="50%%" ALIGN=RIGHT>%(fullname)s
      </TR><TR>
      <TD COLSPAN=2><ADDRESS>
        %(date)s <A HREF="mailto:%(mailaddr)s">
	<%(mailaddr)s></A>
      </ADDRESS>
      </TR>
    </TABLE>
    </BODY>
    </HTML>""" % local_strings
    
############################################################
# Data Structure
############################################################
class PageInfo(UserDict):
    """A lightweight class for holding information about a web page.
    It is just a thin layer over a standard dictionary to ensure that 
    each instance is initialized with all three variables.  See the 
    Library Reference for the UserDict base class."""
    def __init__(self,filename,title,desc):
	UserDict.__init__(self)
	self.data['file'] = filename
	self.data['title'] = title
	self.data['desc'] = desc


############################################################
# Main Program
############################################################
if __name__ == '__main__':
    import sys

    # CONFIGURATION
    # is there a Python way to do getpwuid?
    home_dir = os.environ['HOME'] 
    # The user can override the configuration filename on the commandline
    if len(sys.argv) > 1:
	config_file = sys.argv[1]
    else:
	config_file = os.path.join(home_dir,'.sitemaprc')
	# check that the config file exists and exec it
	if os.path.exists(config_file):
	    # This execfile should be safe since anyone using the
	    # program already has access to Python.
	    execfile(config_file)
	else:
	    if config_file: # it's not equal to '' or None
		sys.stderr.write('Warning: configuration file %s not found.\n' % config_file)
		sys.stderr.write('\tContinuing, using the default configuration.\n')

    if configuration['icondirs'] != '':
	icondirs = '<img src="%s" alt="Dir">' % configuration['icondirs']
    else: icondirs = ''

    if configuration['icontext'] != '':
	icontext = '<img src="%s" alt="Text">' % configuration['icontext']
    else: icontext = ''

    message = get_lang_msg(configuration['language'])

    # MAIN TASK: generate the list of pages to be indexed
    pages = []
    os.path.walk( '.', extract_file_desc, (configuration['exclude'],pages) )
    pages.sort(indsort)

    # GENERATE SITEMAP
    print generate_header(configuration, message)
    oldstem = None 
    for page in pages:
	newstem = get_stem(page)
	#sys.stderr.write("%s + %s + %s + \n" % (page['file'], newstem, oldstem))
	if oldstem != newstem:
	    print '<DT><P ALIGN=RIGHT><HR WIDTH="80%%">\n%s<BR>' % icondirs
	print '<DT>%s\n<a href="%s">%s</a>: <B>%s</B><DD>\n\t%s\n' % \
	      (icontext, page['file'], page['file'], page['title'], page['desc'])
	oldstem = newstem	    
    print generate_footer(configuration,message)

