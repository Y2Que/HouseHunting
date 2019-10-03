from bs4 import BeautifulSoup

listing = []

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