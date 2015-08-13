#! /usr/bin/env python
""" Index links from a sitemap to a SOLR instance"""

import sys
from BeautifulSoup import BeautifulSoup
import solr
import hashlib
import urllib2
from xml.etree.ElementTree import parse

# How many iterations max?  Enter 0 for no limit.
limit = 0 

# The URL of the solr instance
solrUrl = 'http://localhost:8080/sitemap-indexer-test'

# The xmlns for the sitemap schema
sitemaps_ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'

if len(sys.argv) != 2:
	print 'Usage: ./sitemap-indexer.py path'
	sys.exit(1)

sitemapTree = parse(sys.argv[1])

solrInstance = solr.SolrConnection(solrUrl) # Solr Connection object

counter = 0
numAdded = 0

# Find all of the URLs in the form <url>...<loc>URL</loc>...</url>
for urlElem in sitemapTree.findall('{%s}url/{%s}loc'%(sitemaps_ns,sitemaps_ns)):
	counter = counter + 1 # Increment counter

	if limit > 0 and counter > limit:
		# For testing, if the limit is reached, break
		break;

	url = urlElem.text # Get the url text from the element

	try: # Try to get the page at url
		response = urllib2.urlopen(url)
	except:
		print "Error: Cannot get content from URL: "+url
		continue # Cannot get HTML.  Skip.

	try: # Try to parse the HTML of the page
		soup = BeautifulSoup(response.read())
	except:
		print "Error: Cannot parse HTML from URL: "+url
		continue # Cannot parse HTML.  Skip.

	if soup.html == None: # Check if there is an <html> tag
		print "Error: No HTML tag found at URL: "+url
		continue #No <html> tag.  Skip.

	try: # Try to set the title
		title = soup.html.head.title.string.decode("utf-8")
	except:
		print "Error: Could not parse title tag found at URL: "+url
		continue #Could not parse <title> tag.  Skip.

	try: # Try to set the body
		body = str(soup.html.body).decode("utf-8")
	except:
		print "Error: Could not parse body tag found at URL: "+url
		continue #Could not parse <body> tag.  Skip.

	# Get an md5 hash of the url for the unique id
	url_md5 = hashlib.md5(url).hexdigest()

	try: # Add to the Solr instance
		solrInstance.add(id=url_md5,url_s=url,text=body,title=body)
	except Exception as inst:
		print "Error adding URL: "+url
		print "\tWith Message: "+str(inst)
	else:
		print "Added Page \""+title+"\" with URL "+url
		numAdded = numAdded + 1

try: # Try to commit the additions
	solrInstance.commit()
except:
	print "Could not Commit Changes to Solr Instance - check logs"
else:
	print "Success. "+str(numAdded)+" documents added to index"