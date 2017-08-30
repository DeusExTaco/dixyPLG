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
hdr_soup = bs4.BeautifulSoup(r.data, 'lxml', parse_only=onlyHdr)

# Extracts title info
titleInfo = table_soup.text
print(titleInfo)

# Extracts cheat codes
cheatData = cheat_soup.prettify()
cheatData_soup = bs4.BeautifulSoup(cheatData, 'lxml')
d_2 = cheatData_soup.text.splitlines()
for cheatCodes in d_2:
    print(cheatCodes)

# Extracts cheat code descriptions
cheatDesc = hdr_soup.find_all('a')
i = 0
while i < 20:
    z = str(cheatDesc[i])
    p = re.search("(?<=>)(.*)(?=<)", z)
    print("\n" + p.group())
    i += 2

print("\n Woo-----------------------Hoo!")