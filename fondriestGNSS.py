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

    # This header makes it so the website doesn't realize this is a web scrapper. There is an article with more tricks like this: https://pknerd.medium.com/5-strategies-to-write-unblock-able-web-scrapers-in-python-5e40c147bdaf
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

    URL = f"https://www.fondriest.com/products/wireless-data/gps-receivers.htm"
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    itemsGeneral = soup.findAll('li', attrs={'class': 'item'})

    print(f"itemsGeneral: {itemsGeneral}")

    for generalItem in itemsGeneral:

        productURL = generalItem.find('a', href=True)['href']
        r = requests.get(productURL, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        modelNumbers = soup.findAll('td', attrs={'class': 'product-list-table-sku'})
        titles= soup.findAll('td', attrs={'class': 'product-list-table-description'})
        prices = soup.findAll('td', attrs={'class': 'product-list-table-price'})

        for i in range(len(modelNumbers)):
            title = titles[1].replace(',', '')
            link = productURL
            model_number = modelNumbers[1]
            description = "fondriest.com doesn't have a description with their listings"
            price = prices[1].replace(',', '')

            file.write(f"{title}, {description}, {price}, {SOURCE_WEBSITE}, {link}, {DATE_ACCESSED}, {model_number}\n")
            item_count += 1

    print(f"----> FINISHED: Web scraping Fondriest.com for GNSS \nThe number of items saved to the file is {item_count}.")

    file.close()
    return file_string



fondriestGNSS()
