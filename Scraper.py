import requests
import bs4

# url = input ( "Enter a website to extract the URL's from: " )
# page = requests.get ( "http://" + url )

page = requests.get("http://www.fort42.com/gateshark/game1719/")
# onlyTable = bs4.SoupStrainer(style="text-decoration:underline;")
onlyTable = bs4.SoupStrainer('div', style="width:753px;")
# onlyTable = bs4.SoupStrainer(id="ar3ds-gamedisplay")
table_soup = bs4.BeautifulSoup(page.content, 'lxml', parse_only=onlyTable)
data = table_soup.text
data_soup = bs4.BeautifulSoup(data, 'lxml')
abc = data_soup.text.splitlines()
for gameName in abc:
    print(gameName)
