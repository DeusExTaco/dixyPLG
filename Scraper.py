import requests
import bs4

# url = input ( "Enter a website to extract the URL's from: " )
# page = requests.get ( "http://" + url )
page = requests.get("http://www.fort42.com/gateshark/game1719/")


onlyTable = bs4.SoupStrainer(style="width:753px;")
onlyCheat = bs4.SoupStrainer(class_="arcode-float")

#print("here: " + str(page.content).strip())

table_soup = bs4.BeautifulSoup(page.content, 'lxml', parse_only=onlyTable)
cheat_soup = bs4.BeautifulSoup(page.content, 'lxml', parse_only=onlyCheat)

data_1 = table_soup.text
data_2 = cheat_soup.prettify()

data_soup_1 = bs4.BeautifulSoup(data_1, 'lxml')
data_soup_2 = bs4.BeautifulSoup(data_2, 'lxml')

x = data_soup_1.text.splitlines()
x_2 = data_soup_2.text.splitlines()

for gameName in x:
    print(gameName)

for gameName_2 in x_2:
    print(gameName_2)

print("Woo Hoo!")