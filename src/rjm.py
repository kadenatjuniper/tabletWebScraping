import requests
from bs4 import BeautifulSoup
from datetime import date


def rjm():
    print("----> STARTING: web scraping of RJMPrecision.com")
    item_count = 0
    SOURCE_WEBSITE = 'rjm'
    DATE_ACCESSED = str(date.today())

    file_string = f"web_scrap_{SOURCE_WEBSITE}_{DATE_ACCESSED}.csv"
    file = open(file_string, "w")
    file.write("Title, Description, Price, Web_source, Link, Date_Accessed, Model #\n")

    # This header makes it so the website doesn't realize this is a web scrapper. There is a create article with more tricks like this: https://pknerd.medium.com/5-strategies-to-write-unblock-able-web-scrapers-in-python-5e40c147bdaf
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }
    for pagecount in range(1, 10):
        print(f"Pulling page {pagecount}")
        URL = f"https://shoprjmprecision.com/collections/data-collectors?page={pagecount}"
        r = requests.get(URL, headers=headers)

        soup = BeautifulSoup(r.content, 'html.parser')

        items = soup.findAll('div', attrs={'class': 'product-card product-card-wrapper'})

        for item in items:
            title = 'None'
            description = 'None'
            price = 'None'
            link = 'None'
            title = item.find('span', attrs={'class': 'h4 item__title product-card__title'}).text
            link = item.find('a', attrs={'class': 'list-view-item__link-image product-card__link-image'})['href']
            model_number = ''
            description = item.find('a', attrs={'class': 'product-item__vendor link'}).text
            price_object = item.find('span', attrs={'class': 'price-item price-item--regular'})
            if price_object:
                price = price_object.text.replace(',', '').replace('$', '').strip()
                price = ''.join(c for c in price if c.isnumeric() or c == '.')
            file.write(f"{title}, {description}, {price}, {SOURCE_WEBSITE}, https://shoprjmprecision.com/{link}, {DATE_ACCESSED}, {model_number}\n")
            item_count += 1


    print(f"----> FINISHED: Web scraping RJMPrecision.com \nThe number of items saved to the file is {item_count}.")

    file.close()
    return file_string


# rjm()
