import re

import bs4
import urllib3


# Can be iterated to return next page containing cheat codes
def getnexturl(x, y):
    url = x + '?search=&sort=dates&p='
    o = url + str(y)
    return o


# Return the total number of pages, with cheats, for each title as an integer
def getpagecount(x):
    page_strain = bs4.SoupStrainer(onchange="$(this).closest('form').submit();")
    page_soup = bs4.BeautifulSoup(x.data, 'lxml', parse_only=page_strain).find_all("option")
    l = len(page_soup)
    o = int(l - 1)
    return o


# Returns title info as a | delimited string
def gettitleinfo(x):
    onlytable = bs4.SoupStrainer(style="width:753px;")
    table_soup = bs4.BeautifulSoup(x.data, 'lxml', parse_only=onlytable)
    titleinfo = table_soup.text \
        .replace("Publisher: ", "|") \
        .replace("Title ID: ", "|") \
        .replace("Serial: ", "|") \
        .replace("\n", "") \
        .strip()
    o = titleinfo
    return o


# Returns cheat codes as a | delimited string
def getcheatcodes(x):
    onlycheat = bs4.SoupStrainer(class_="arcode-float")
    cheat_soup = bs4.BeautifulSoup(x.data, 'lxml', parse_only=onlycheat)
    cheatdata = str(cheat_soup) \
        .replace("<!DOCTYPE HTML>", "") \
        .replace("</div>", "") \
        .replace('<div class="arcode-float">', "") \
        .replace("<textarea readonly=\"\">", "") \
        .replace("</textarea>", "|") \
        .replace("\r", "") \
        .replace("\n", " ") \
        .rstrip("|") \
        .strip()
    o = cheatdata
    return o


# Returns cheat code descriptions as a | delimited string
def getcheatdesc(x):
    onlyhdr = bs4.SoupStrainer(class_="arcode-header")
    hdr_soup = bs4.BeautifulSoup(x.data, 'lxml', parse_only=onlyhdr).find_all('a')
    i = 0
    sl = len(hdr_soup)
    q = ""
    while i < sl:
        z = str(hdr_soup[i])
        p = re.search("(?<=>)(.*)(?=<)", z)
        q += str(p.group()) + "|"
        i += 2
    o = q.rstrip("|")
    return o


http = urllib3.PoolManager()
baseUrl = 'http://www.fort42.com/gateshark/game1333/'
r = http.request('GET', baseUrl)

print(gettitleinfo(r))
print(getcheatdesc(r))
print(getcheatcodes(r))

f = 2
while f <= getpagecount(r):
    v = getnexturl(baseUrl, f)
    print(getcheatdesc(http.request('GET', v)))
    print(getcheatcodes(http.request('GET', v)))
    f += 1
