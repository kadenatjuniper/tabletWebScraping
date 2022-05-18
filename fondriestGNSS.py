import requests
from bs4 import BeautifulSoup
from datetime import date


def fondriestGNSS():
    print("----> STARTING: web scraping of Fondriest.com for GNSS")
    item_count = 0
    SOURCE_WEBSITE = 'fondriestGNSS'
    DATE_ACCESSED = str(date.today())

    file_string = f"web_scrap_{SOURCE_WEBSITE}_{DATE_ACCESSED}.csv"
    file = open(file_string, "w")
    file.write("Title, Description, Price, Web_source, Link, Date_Accessed, Model #\n")

    # This header makes it so the website doesn't realize this is a web scrapper. There is a create article with more tricks like this: https://pknerd.medium.com/5-strategies-to-write-unblock-able-web-scrapers-in-python-5e40c147bdaf
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

    URL = f"https://www.fondriest.com/products/wireless-data/gps-receivers.htm"
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    itemsGeneral = soup.findAll('li', attrs={'class': 'item'})

    for generalItem in itemsGeneral:

        productURL = generalItem.find('a', href=True)['href']
        r = requests.get(productURL, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        productTable = soup.findAll('table', attrs={'class': 'product-list-table '})
        itemsProduct = productTable.tbody.findall('tr')

        for item in itemsProduct:
            title = 'None'
            description = 'None'
            price = 'None'
            link = 'None'
            title_object = item.find('a', attrs={'class': 'product-item-link'})
            if title_object:
                title = title_object['title'].replace(',', '')
                link = title_object['href']
            model_number = ''
            description = "allterra.com doesn't have a description with their listings"
            price_object = item.find('span', attrs={'class': 'price'})
            if price_object:
                price = price_object.text.replace(',', '')
            file.write(f"{title}, {description}, {price}, {SOURCE_WEBSITE}, {link}, {DATE_ACCESSED}, {model_number}\n")
            item_count += 1

    print(f"----> FINISHED: Web scraping Fondriest.com for GNSS \nThe number of items saved to the file is {item_count}.")

    file.close()
    return file_string



fondriestGNSS()
