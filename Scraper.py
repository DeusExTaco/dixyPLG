import urllib3
import bs4
import re

http = urllib3.PoolManager()
r = http.request('GET', 'http://www.fort42.com/gateshark/game1719/')

# Soup filters
onlyTable = bs4.SoupStrainer(style="width:753px;")
onlyCheat = bs4.SoupStrainer(class_="arcode-float")
onlyHdr = bs4.SoupStrainer(class_="arcode-header")

# Initial soup creation
table_soup = bs4.BeautifulSoup(r.data, 'lxml', parse_only=onlyTable)
cheat_soup = bs4.BeautifulSoup(r.data, 'lxml', parse_only=onlyCheat)
hdr_soup = bs4.BeautifulSoup(r.data, 'lxml', parse_only=onlyHdr).find_all('a')

# Extracts title info into a | delimited string
titleInfo = table_soup.text \
    .replace("Publisher: ","|") \
    .replace("Title ID: ","|") \
    .replace("Serial: ","|") \
    .replace("\n", "") \
    .strip()
print(titleInfo)

# Extracts cheat codes into a | delimited string
cheatData = str(cheat_soup) \
    .replace ( "<!DOCTYPE HTML>", "" )\
    .replace ("</div>", "" ) \
    .replace ( '<div class="arcode-float">', "" ) \
    .replace ( "<textarea readonly=\"\">", "" ) \
    .replace ( "</textarea>", "|") \
    .replace ( "\r","") \
    .replace ( "\n", " ") \
    .rstrip ( "|" ) \
    .strip()
print(cheatData)

# Extracts cheat code descriptions into a | delimited string
i = 0
q = ""
while i < 20:
    z = str(hdr_soup[i])
    p = re.search("(?<=>)(.*)(?=<)", z)
    q += str(p.group()) + "|"
    i += 2
print(q.rstrip("|"))
