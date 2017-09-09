import re

import bs4
import urllib3


# Can be iterated to return url of next page containing cheat codes
def getnexturl(base_url, page_num):
    nexturl = base_url + '?search=&sort=dates&p=' + str(page_num)
    return nexturl


# Return the total number of pages, with cheats, for each title as an integer
def getpagecount(page_request):
    page_strain = bs4.SoupStrainer(onchange="$(this).closest('form').submit();")
    page_soup = bs4.BeautifulSoup(page_request.data, 'lxml', parse_only=page_strain).find_all("option")
    pagecount = int(len(page_soup) - 1)
    return pagecount


# Returns title info as a | delimited string
def gettitleinfo(page_request):
    table_strain = bs4.SoupStrainer(style="width:753px;")
    table_soup = bs4.BeautifulSoup(page_request.data, 'lxml', parse_only=table_strain)
    titleinfo = table_soup.text \
        .replace("Publisher: ", "|") \
        .replace("Title ID: ", "|") \
        .replace("Serial: ", "|") \
        .replace("\n", "") \
        .strip()
    return titleinfo


# Returns cheat codes as a | delimited string
def getcheatcodes(page_request):
    cheat_strain = bs4.SoupStrainer(class_="arcode-float")
    cheat_soup = bs4.BeautifulSoup(page_request.data, 'lxml', parse_only=cheat_strain)
    cheatcodes = str(cheat_soup) \
        .replace("<!DOCTYPE HTML>", "") \
        .replace("</div>", "") \
        .replace('<div class="arcode-float">', "") \
        .replace("<textarea readonly=\"\">", "") \
        .replace("</textarea>", "|") \
        .replace("\r", "") \
        .replace("\n", " ") \
        .rstrip("|") \
        .strip()
    return cheatcodes


# Returns cheat code descriptions as a | delimited string
def getcheatdesc(page_request):
    hdr_strain = bs4.SoupStrainer(class_="arcode-header")
    hdr_soup = bs4.BeautifulSoup(page_request.data, 'lxml', parse_only=hdr_strain).find_all('a')
    i = 0
    q = ""
    while i < len(hdr_soup):
        p = re.search("(?<=>)(.*)(?=<)", str(hdr_soup[i]))
        q += str(p.group()) + "|"
        i += 2
    cheatdesc = q.rstrip("|")
    return cheatdesc


# Returns a single | delimited string with multiple ^ delimited segments
# containing 'cheat description' + ^ + 'cheat code'
def getallcheatinfo(page_request):
    cd_strain = bs4.SoupStrainer(class_="arcode-header")
    cheat_strain = bs4.SoupStrainer(class_="arcode-float")
    cd_soup = bs4.BeautifulSoup(page_request.data, 'lxml', parse_only=cd_strain).find_all('a')
    cheat_soup = bs4.BeautifulSoup(page_request.data, 'lxml', parse_only=cheat_strain)

    # Creates | delimited string containing all cheat codes
    cheatcodes = str(cheat_soup) \
        .replace("<!DOCTYPE HTML>", "") \
        .replace("</div>", "") \
        .replace('<div class="arcode-float">', "") \
        .replace("<textarea readonly=\"\">", "") \
        .replace("</textarea>", "|") \
        .replace("\r", "") \
        .replace("\n", " ") \
        .rstrip("|") \
        .strip()

    i = 0
    q = ""
    y = 0
    while i < len(cd_soup):
        p = re.search("(?<=>)(.*)(?=<)", str(cd_soup[i]))
        q += str(p.group()) + "^" + cheatcodes.split("|")[y] + "|"
        i += 2
        y += 1
    allcheatinfo = (q.rstrip("|"))
    return allcheatinfo


http = urllib3.PoolManager()
baseURL = 'http://www.fort42.com/gateshark/game1333/'  # Assumes valid URL

r = http.request('GET', baseURL)

print(gettitleinfo(r))

o = ""
if getpagecount(r) != 0:
    pagenum = 1
    while pagenum <= getpagecount(r):
        o += getallcheatinfo(http.request('GET', getnexturl(baseURL, pagenum))) + "|"
        pagenum += 1
    print(o.rstrip("|"))
