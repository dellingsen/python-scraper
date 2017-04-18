import urllib2
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from urlparse import urljoin

BASE_URL = 'http://minneapolis.craigslist.org/'

def scrape_vehicles():
    """ Scrape all the vehicles by owner from Craigslist """
    
    # A link to Minneapolis craigslist auto section - 10 pages
    urls = ['http://minneapolis.craigslist.org/cto',
            'http://minneapolis.craigslist.org/cto/index100.html',
            'http://minneapolis.craigslist.org/cto/index200.html',
            'http://minneapolis.craigslist.org/cto/index300.html',
            'http://minneapolis.craigslist.org/cto/index400.html',
            'http://minneapolis.craigslist.org/cto/index500.html',
            'http://minneapolis.craigslist.org/cto/index600.html',
            'http://minneapolis.craigslist.org/cto/index700.html',
            'http://minneapolis.craigslist.org/cto/index800.html',
            'http://minneapolis.craigslist.org/cto/index900.html'
            ]

    counter = 0
    
	# Create a results file to store all of our scraping findings
    file = open('scrape_results.json', 'w')
	
    for url_cl in urls:

        # Download the list of vehicles for sale by owner

        # 1. Here were using requests, a python library for accessing the web

        # we add "cto/" to the url to tell requests
        # to get the cars and truck by owner
        # on minneapolis.craigslist.org
        # response = requests.get(BASE_URL + "cto/")
		
		# Just use URL from our list
        response = requests.get(url_cl)

        # 2. Now we parse HTML using Beautiful Soup library
		
        # This returns a `soup` object which gives us convenience methods for parsing html
        soup = BeautifulSoup(response.content, "html.parser")
        #print(soup)

        # Find all the posts in the page.

        # Here we're telling BeautifulSoup to get us every
        # span tag that has a class that equals pl
        # these tags might look something like this:
        # <span class='pl'> {content} </span>
        # auto_links = soup.find_all('span', {'class':'pl'})
		
		# Realized that we need to go after the "result-row" instead
		# that gives us the link row in every page of results
        auto_links = soup.find_all('li', {'class':'result-row'})

		
		# Get all the links to auto pages:
        for auto_link in auto_links:
            
            # for each span list, find the "a" tag which 
            # represents the link to the for sale auto page.
            link = auto_link.find('a').attrs['href']
            
            link_desc = auto_link.find('a')

            print("Auto Page Link:")
            print(link)
            #print("'link_desc = " + link_desc.string)

            #print counter

            # join this relative link with the 
            # BASE_URL to create an absolute link

            url = urljoin(BASE_URL, link)
            
            # pass this url to a function (defined below) to scrape 
            # info about that vehicle on auto page
            scrape_vehicle(url, counter, file)
            counter += 1


def scrape_vehicle(url, counter, file):

    # retrieve the vehicle with requests
    response = requests.get(url)

    # Parse the html of the vehicle post
    soup = BeautifulSoup(response.content)

    # Extract the actual contents of some HTML elements:

    # here were using BeautifulSoup's `text` method for retrieving
    # the plain text within each HTML element.

    # subject = soup.find('h2', {'class':'postingtitle'}).text.strip()
	
    subject = soup.find('span', {'class':'postingtitletext'})
    if soup.find('span', {'class':'postingtitletext'}) is not None:
       subject = soup.find('span', {'class':'postingtitletext'}).text.strip()

    if soup.find('span', {'class':'price'}) is not None:
       price = soup.find('span', {'class':'price'}).text.strip()

    description = soup.find('section', {'id':'postingbody'})
    if soup.find('section', {'id':'postingbody'}) is not None:
       description = soup.find('section', {'id':'postingbody'}).text.strip()
 
    if soup.find('p', {'class':'print-information print-contact'}) is not None:
       contactinfo = soup.find('p', {'class':'print-information print-contact'}).text.strip()
	
    datetime = soup.find('time')
    if datetime is not None:
       datetime = soup.find('time').attrs['datetime']	
	
	# Look for Mazda specific vehicle
    if (subject is not None and subject.lower().find("mazda") >= 0):
       print("Found Mazda match")
	   
       print("Vehicle ad subject: ")
       pprint(subject)
       #print("Vehicle ad price: ")
       #pprint(price)
       #print("Vehicle ad description: ")
	   #pprint(description)
       print("Vehicle ad contactinfo: ")
       pprint(contactinfo)
       file.write(subject)

    data = {
        'source_url': url,
        'subject': subject,
        'body': description,
        'datetime': datetime
    }

	# Look for subaru specific vehicle
    if (subject is not None and subject.lower().find("subaru") >= 0):
        print "Found Subaru match: " + subject
        pprint(data)
        file.write(str(data))
    

if __name__ == '__main__':
    scrape_vehicles()
