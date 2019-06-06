# Python 2.7

import csv
import ssl
import urllib2  
from bs4 import BeautifulSoup

# get page with list of monthly listings
url = 'https://access.tarrantcounty.com/en/constables/constable-3/delinquent-tax-sales/monthly-tax-sales-listings.html'

# SSL certificate bypass
context = ssl._create_unverified_context()
response = urllib2.urlopen(url, context=context)
html = response.read()

# format for readability & utility
soup = BeautifulSoup(html, "html.parser")

# get all rows of dates
for node in soup.find_all(class_="parbase link-list section col-md-10"):
    print(node.get_text("|", strip=True))
    print(node.a.get('href'))  # not sure why this isn't giving full URL