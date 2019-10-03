import ssl
import urllib2
import requests
from bs4 import BeautifulSoup

'''
# get page with list of monthly listings
url_base = "https://access.tarrantcounty.com"
url = url_base + "/en/constables/constable-3/delinquent-tax-sales/monthly-tax-sales-listings.html"
response = response = requests.post(url, verify=False)
'''

# get page with list of monthly listings
url_base = "https://access.tarrantcounty.com"
url = url_base + "/en/constables/constable-3/delinquent-tax-sales/monthly-tax-sales-listings.html"
context = ssl._create_unverified_context()
response = urllib2.urlopen(url, context=context)

# format for readability & utility
soup = BeautifulSoup(response.read(), "html.parser")

listDates = []  # declare list to hold dates and urls

# get all rows of dates
for node in soup.find_all(class_="parbase link-list section col-md-10"):
    # make list of date and url (after url_base)
    dictTemp = {}  # declare dictionary with date and URL
    dictTemp["Date"] = node.get_text("|", strip=True)
    dictTemp["Url"] = url_base + node.a.get('href')

    # add tempList to end of list
    listDates.append(dictTemp)

with open('temp.txt', 'w') as myFile:
    myFile.write(str(soup))

for elem in listDates:
    print (elem)