import ssl
import urllib2
import requests
from bs4 import BeautifulSoup
import bs4
import csv

# get page with list of monthly listings
url_base = "https://access.tarrantcounty.com"
url = url_base + "/en/constables/constable-3/delinquent-tax-sales/monthly-tax-sales-listings.html"
context = ssl._create_unverified_context()
response = urllib2.urlopen(url, context=context)

# format for readability & utility
soup = BeautifulSoup(response.read(), "html.parser")

listDates = [] # declare list to hold dates and urls

# get all rows of dates
for node in soup.find_all(class_="parbase link-list section col-md-10"):
    # make list of date and url (after url_base)
    dictTemp = {}  # declare dictionary with date and URL
    dictTemp["Date"] = node.get_text("|", strip=True)
    dictTemp["Url" ] = url_base + node.a.get('href')
    
    # add tempList to end of list
    listDates.append(dictTemp)

print ("======= LIST OF DATES =======")
for elem in listDates:
    print (elem)

listData = [] # declare list to hold dates and urls

# loop thru months with listings
for listing in listDates:
    # get page with listing for a single month
    url = listing.get("Url")

    context = ssl._create_unverified_context()
    response = urllib2.urlopen(url, context=context)

    # format for readability & utility
    soup = BeautifulSoup(response.read(), "html.parser")

    # flag for 1st iteration of loop
    colInfoFound = False
    colIndex = 0
    colInfo1 = -1
    colInfo2 = -1
    colInfo3 = -1

    # loop through columns to find data
    for row in soup.findAll("tr"):
        # if data is found
        if colInfoFound:
            if row.contents[3].get_text().strip().isnumeric():
                dictResults = {} # add dictionary with date and URL
                dictResults["CaseNo"   ] = row.contents[colInfo1].get_text().strip()
                dictResults["AccountNo"] = row.contents[colInfo2].get_text().strip()
                dictResults["Status"   ] = row.contents[colInfo3].get_text().strip()

                if dictResults["Status"] == "For Sale":
                    # add tempList to end of main list
                    listData.append(dictResults)
        else: # on 1st iteration find column info
            # check if column is blank
            for column in row.contents:
                # only check columns of type Tag that are not blank
                if isinstance(column, bs4.element.Tag) and not column.get_text().strip() == "":
                    if colInfo1 == -1:
                        colInfo1 = colIndex
                    elif colInfo2 == -1:
                        colInfo2 = colIndex
                    elif colInfo3 == -1:
                        colInfo3 = colIndex
                        colInfoFound = True
                        break
                # increment column counter
                colIndex += 1

# debug
print ("======= LIST OF RESULTS =======")
for elem in listData:
    print (elem)

print("1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
# open output file
outFile = open("./houses.csv", "wb")
# create writer to write CSV file
writer = csv.writer(outFile)
print("222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222")
for listing in listData:

    # get search results for a single account
    url = "https://www.tad.org/property-search-results/"
    data = {"tpaspin":listing["AccountNo"],"tpas":"Search"}
    response = requests.post(url, data)

    # format for readability & utility
    soup = BeautifulSoup(response.content, "html.parser")

    # set inital value in case of failure to retrieve values
    listing["Address"] = ""
    listing["City"   ] = ""
    listing["Owner"  ] = ""
    listing["Value"  ] = ""
    listing["IsPrimAddress"   ] = ""
    listing["PrimOwnerAddress"] = ""

    # get results and store in dictionary
    try:
        listing["Address"] = soup.find("td", attrs={"data-label":"Property Address"  }).get_text().strip()
        listing["City"   ] = soup.find("td", attrs={"data-label":"Property City"     }).get_text().strip()
        listing["Owner"  ] = soup.find("td", attrs={"data-label":"Primary Owner Name"}).get_text().strip()
        listing["Value"  ] = soup.find("td", attrs={"data-label":"Market Value"      }).get_text().strip()

        primaryAddress = soup.find("div", attrs={"class":"primaryOwnerAddress"}).get_text().strip().split(":",2)[1].strip()
        listing["PrimOwnerAddress"] = primaryAddress.split("\n",2)[0].strip()

        if  listing["PrimOwnerAddress"] == listing["Address"]:
            listing["IsPrimAddress"] = "Yes"
        else:
            listing["IsPrimAddress"] = "No"
    except:
        pass

    print("333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333")
    # write results to .csv file
    writer.writerow([listing["AccountNo"],"","","",listing["Address"],"",listing["Owner"],listing["IsPrimAddress"],"","","","",listing["Value"],"","","","",listing["PrimOwnerAddress"]])
    #writer.writerow([listing["AccountNo"],"","","","E address","","G owner","H prim residence","","","","","M estimated value","","","","","R prim resident address"])
    print("44444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444")

    print(listing)

print("FIN")