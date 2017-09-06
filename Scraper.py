import re

import bs4
import urllib3

http = urllib3.PoolManager()
r = http.request('GET', 'http://www.fort42.com/gateshark/game1333/')


# Extracts title info into a | delimited string
def gettitleinfo(x):
    onlyTable = bs4.SoupStrainer(style="width:753px;")
    table_soup = bs4.BeautifulSoup(x.data, 'lxml', parse_only=onlyTable)
    titleInfo = table_soup.text \
        .replace("Publisher: ", "|") \
        .replace("Title ID: ", "|") \
        .replace("Serial: ", "|") \
        .replace("\n", "") \
        .strip()
    o = titleInfo
    return o


# Extracts cheat codes into a | delimited string
def getcheatcodes(x):
    onlyCheat = bs4.SoupStrainer(class_="arcode-float")
    cheat_soup = bs4.BeautifulSoup(x.data, 'lxml', parse_only=onlyCheat)
    cheatData = str(cheat_soup) \
        .replace("<!DOCTYPE HTML>", "") \
        .replace("</div>", "") \
        .replace('<div class="arcode-float">', "") \
        .replace("<textarea readonly=\"\">", "") \
        .replace("</textarea>", "|") \
        .replace("\r", "") \
        .replace("\n", " ") \
        .rstrip("|") \
        .strip()
    o = cheatData
    return o


# Extracts cheat code descriptions into a | delimited string
def getcheatdesc(x):
    onlyHdr = bs4.SoupStrainer(class_="arcode-header")
    hdr_soup = bs4.BeautifulSoup(x.data, 'lxml', parse_only=onlyHdr).find_all('a')
    i = 0
    q = ""
    while i < 20:
        z = str(hdr_soup[i])
        p = re.search("(?<=>)(.*)(?=<)", z)
        q += str(p.group()) + "|"
        i += 2
    o = q.rstrip("|")
    return o
