from bs4 import BeautifulSoup
from datetime import date
from math import ceil
import cloudscraper


def barcodes_inc_web_scrap():
    print("----> STARTING: web scraping of BarcodesInc.com")
    item_count = 0
    page_count = 0
    SOURCE_WEBSITE = 'barcodes_inc'
    DATE_ACCESSED = str(date.today())

    file_string = f"web_scrap_{SOURCE_WEBSITE}_{DATE_ACCESSED}.csv"
    file = open(file_string, "w")
    file.write("Title, Description, Price, Web_source, Link, Date_Accessed, Model #\n")

    scraper = cloudscraper.create_scraper()
    total_pages = get_total_pages(scraper)

    while page_count < total_pages:
        URL = f"https://www.barcodesinc.com/cats/tablets/rugged.htm?page={page_count + 1}.htm"
        print(f"Pulling webpage {page_count}...")
        page_count += 1

        s = scraper.get(URL)

        soup = BeautifulSoup(s.content, 'html.parser')

        product_table = soup.find('table', attrs={'class': 'table producttable'})
        items = product_table.findAll('tr')

        for item in items:
            title = 'None'
            description = 'None'
            price = 'None'
            link = 'None'
            title_object = item.find('span', attrs={'class': 'modelname'})
            if title_object:
                title = title_object.a.b.text.replace(',', '').replace('\n', '')
                link = "barcodesinc.com" + title_object.a['href']
            model_number = 'Not Implemented'
            description_object = item.find('div', attrs={'class': 'search_result_description'})
            if description_object:
                description = description_object.text.replace(',', '-').replace('\n', '')
            price_object = item.find('span', attrs={'class': 'price'})
            if price_object:
                price = price_object.text.replace(',', '')
            file.write(f"{title}, {description}, {price}, {SOURCE_WEBSITE}, {link}, {DATE_ACCESSED}, {model_number}\n")
            item_count += 1

    print(f"----> FINISHED: Web scraping BarcodesInc.com \nThe number of items saved to the file is {item_count}.")

    file.close()
    return file_string


def get_total_pages(scraper):
    first_URL = "https://www.barcodesinc.com/cats/tablets/rugged.htm"
    s = scraper.get(first_URL)
    soup = BeautifulSoup(s.content, 'html.parser')
    items_string = soup.find('td', attrs={'class': 'hitcount'}).div.text
    number_items = int(items_string.split(" ")[-1].replace('.', '').replace('\n', ''))
    print(f"Number of items: {number_items}")
    items_per_page = 15
    print(f"Items per page: {items_per_page}")
    total_pages = ceil(number_items / items_per_page)
    print(f"Total number of pages: {total_pages}")
    return total_pages


# barcodes_inc_web_scrap()
