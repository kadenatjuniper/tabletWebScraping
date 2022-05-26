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
    products = soup.find('div', attrs={'class': 'products wrapper grid products-grid products-grid-partitioned category-products-grid centered equal-height pos-'})
    itemsGeneral = products.findAll('li', attrs={'class': 'item'})


    for page_count, generalItem in enumerate(itemsGeneral):

        print(f"Pulling webpage {page_count}...")

        productURL = generalItem.find('a', href=True)['href']
        r = requests.get(productURL, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        productListTable = soup.find("table", attrs={'class': 'product-list-table'})
        modelNumbers = productListTable.findAll('td', attrs={'class': 'product-list-table-sku'})
        titles = productListTable.findAll('td', attrs={'class': 'product-list-table-description'})
        prices = productListTable.findAll('td', attrs={'class': 'product-list-table-price'})
        description = soup.find('div', attrs={'class': 'value', 'itemprop': 'description'}).text.replace(',', '-')

        for i in range(len(modelNumbers)):
            modelNumbers[i] = modelNumbers[i].text.replace(' ', '')
        for i in range(len(titles)):
            titles[i] = titles[i].text.replace('\n', '')
        for i in range(len(prices)):
            prices[i] = prices[i].text.replace(',', '')


        for i in range(len(modelNumbers)):
            title = titles[i].replace(',', '')
            link = productURL
            model_number = modelNumbers[i]
            # description = "Fondriest.com doesn't have a description with their listings"
            price = prices[i].replace(',', '')

            file.write(f"{title}, {description}, {price}, {SOURCE_WEBSITE}, {link}, {DATE_ACCESSED}, {model_number}\n")
            item_count += 1

    print(f"----> FINISHED: Web scraping Fondriest.com for GNSS \nThe number of items saved to the file is {item_count}.")

    file.close()
    return file_string



# fondriestGNSS()
