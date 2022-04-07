import requests
from bs4 import BeautifulSoup
from datetime import date
from math import ceil


def cdw_web_scrap():
    print("----> STARTING: web scraping of BarcodesInc.com")
    item_count = 0
    page_count = 0
    SOURCE_WEBSITE = 'barcodes_inc'
    DATE_ACCESSED = str(date.today())

    file_string = f"web_scrap_{SOURCE_WEBSITE}_{DATE_ACCESSED}.csv"
    file = open(file_string, "w")
    file.write("Title, Description, Price, Web_source, Link, Date_Accessed, Part/Item #, MFG #, SKU, CDW #\n")

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'referrer': 'https://google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Pragma': 'no-cache',
    }

    total_pages = get_total_pages(headers)

    while page_count < total_pages:
        URL = f"https://www.cdw.com/search/computers/tablets/?key=&w=CC&ln=0&pcurrent={page_count + 1}.htm"
        print(f"Pulling webpage {page_count}...")
        page_count += 1
        r = requests.get(URL, headers=headers)

        soup = BeautifulSoup(r.content, 'html.parser')

        items = soup.findAll('div', attrs={'class': 'search-result coupon-check'})

        for item in items:
            title = 'None'
            description = 'None'
            price = 'None'
            link = 'None'
            title_object = item.find('a', attrs={'class': 'search-result-product-url'})
            if title_object:
                title = title_object.text.replace(',', '')
                link = "cdw.com" + title_object['href']
            description = "cdw.com doesn't have a description with their listings"
            price_object = item.find('div', attrs={'class': 'price-type-price'})
            if price_object:
                price = price_object.text.replace(',', '')
            file.write(f"{title}, {description}, {price}, {SOURCE_WEBSITE}, {link}, {DATE_ACCESSED}\n")
            item_count += 1


    print(f"----> FINISHED: Web scraping BarcodesInc.com \nThe number of items saved to the file is {item_count}.")

    file.close()
    return file_string


def get_total_pages(headers):
    first_URL = "https://www.barcodesinc.com/cats/tablets/rugged.htm"
    r = requests.get(first_URL, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    print(soup.prettify())
    items_string = soup.find('td', attrs={'class': 'hitcount'}).div.text
    number_items = int(items_string.split(" ")[-1])
    print(f"Number of items: {number_items}")
    items_per_page = int(items_string[0].split("-")[1])
    print(f"Items per page: {items_per_page}")
    total_pages = ceil(number_items / items_per_page)
    print(total_pages)
    return total_pages


# cdw_web_scrap()
