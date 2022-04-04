import requests
from bs4 import BeautifulSoup

item_dictionary = {}

for i in range(2):
    URL = f"https://www.barcodegiant.com/cats/tablets/page/{i + 1}.htm"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html.parser')

    items = soup.findAll('div', attrs={'class': 'item-area clearfix'})

    i = 0
    for item in items:
        if not item.find('button', attrs={'title': 'See price in cart'}):
            item_features = {'Title': item.find('h2', attrs={'class': 'product-name'}).a.text,
                             'Description': item.find('div', attrs={'class': 'details-area'}).div.text,
                             'price': item.find('span', attrs={'class': 'price'}).text, }
            item_dictionary[i] = item_features
            i += 1
        else:
            print("Price in chart encountered")

    for i in range(len(item_dictionary)):
        print(item_dictionary[i]['Title'])

    