import requests
from bs4 import BeautifulSoup
from datetime import date


def dell():
    print("----> STARTING: web scraping of Dell.com")
    item_count = 0
    SOURCE_WEBSITE = 'dell'
    DATE_ACCESSED = str(date.today())

    file_string = f"web_scrap_{SOURCE_WEBSITE}_{DATE_ACCESSED}.csv"
    file = open(file_string, "w", encoding="utf-8")
    file.write("Title, Description, Price, Web_source, Link, Date_Accessed, Model #\n")

    # This header makes it so the website doesn't realize this is a web scrapper. There is a create article with more tricks like this: https://pknerd.medium.com/5-strategies-to-write-unblock-able-web-scrapers-in-python-5e40c147bdaf
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

    URL = f"https://www.dell.com/en-us/shop/scc/sr/laptops/rugged-laptops"
    r = requests.get(URL, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    items = soup.findAll('article', attrs={'class': 'stack-system ps-stack'})

    for item in items:
        title = 'None'
        description = 'None'
        price = 'None'
        link = 'None'
        title_object = item.find('h3', attrs={'class': 'ps-title'}).a
        if title_object:
            title = title_object.text.replace(',', '').replace('\n', '')
            link = title_object['href']
        model_number = item['id']
        description = item.find('div', attrs={'class': 'ps-iconography-container'}).text.replace(',', '').replace('\n', ' ')
        price_string = item.find('div', attrs={'class': 'ps-dell-price ps-simplified'}).text
        if price_string:
            price = ''.join(c for c in price_string if c.isnumeric() or c == '.')
        file.write(f"{title}, {description}, {price}, {SOURCE_WEBSITE}, {link}, {DATE_ACCESSED}, {model_number}\n")
        item_count += 1


    print(f"----> FINISHED: Web scraping Dell.com \nThe number of items saved to the file is {item_count}.")

    file.close()
    return file_string



dell()
