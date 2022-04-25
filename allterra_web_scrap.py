import requests
from bs4 import BeautifulSoup
from datetime import date


def allterra_web_scrap():
    print("----> STARTING: web scraping of Allterra.com")
    item_count = 0
    SOURCE_WEBSITE = 'allterra'
    DATE_ACCESSED = str(date.today())

    file_string = f"web_scrap_{SOURCE_WEBSITE}_{DATE_ACCESSED}.csv"
    file = open(file_string, "w")
    file.write("Title, Description, Price, Web_source, Link, Date_Accessed, Model #\n")

    # This header makes it so the website doesn't realize this is a web scrapper. There is a create article with more tricks like this: https://pknerd.medium.com/5-strategies-to-write-unblock-able-web-scrapers-in-python-5e40c147bdaf
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

    URL = f"https://allterracentral.com/products.html/mapping-gis/handhelds.html"
    r = requests.get(URL, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    items = soup.findAll('li', attrs={'class': 'item product product-item'})

    for item in items:
        title = 'None'
        description = 'None'
        price = 'None'
        link = 'None'
        title_object = item.find('a', attrs={'class': 'product-item-link'})
        if title_object:
            title = title_object['title'].replace(',', '')
            link = title_object['href']
        model_number = 'Not Implemented'
        description = "allterra.com doesn't have a description with their listings"
        price_object = item.find('span', attrs={'class': 'price'})
        if price_object:
            price = price_object.text.replace(',', '')
        file.write(f"{title}, {description}, {price}, {SOURCE_WEBSITE}, {link}, {DATE_ACCESSED}, {model_number}\n")
        item_count += 1


    print(f"----> FINISHED: Web scraping Allterra.com \nThe number of items saved to the file is {item_count}.")

    file.close()
    return file_string



# allterra_web_scrap()
