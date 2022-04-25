import requests
from bs4 import BeautifulSoup
from datetime import date
from math import ceil


def cdw_web_scrap():
    print("----> STARTING: web scraping of CDW.com")
    item_count = 0
    page_count = 0
    SOURCE_WEBSITE = 'cdw'
    DATE_ACCESSED = str(date.today())

    file_string = f"web_scrap_{SOURCE_WEBSITE}_{DATE_ACCESSED}.csv"
    file = open(file_string, "w")
    file.write("Title, Description, Price, Web_source, Link, Date_Accessed, Model #\n")

    total_pages = get_total_pages()

    while page_count < total_pages:
        URL = f"https://www.cdw.com/search/computers/tablets/?key=&w=CC&ln=0&pcurrent={page_count + 1}.htm"
        print(f"Pulling webpage {page_count}...")
        page_count += 1
        r = requests.get(URL)

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
            model_number = 'test'
            description = "cdw.com doesn't have a description with their listings"
            price_object = item.find('div', attrs={'class': 'price-type-price'})
            if price_object:
                price = price_object.text.replace(',', '')
            file.write(f"{title}, {description}, {price}, {SOURCE_WEBSITE}, {link}, {DATE_ACCESSED}, {model_number}\n")
            item_count += 1


    print(f"----> FINISHED: Web scraping CDW.com \nThe number of items saved to the file is {item_count}.")

    file.close()
    return file_string


def get_total_pages():
    first_URL = "https://www.cdw.com/search/computers/tablets/?key=&w=CC&ln=0&pcurrent=1"
    r = requests.get(first_URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    pages = soup.find('div', attrs={'class': 'search-scope-pagination-range'}).text
    number_items = int(pages.split(" ")[-1])
    items_per_page = int(soup.find('select', attrs={'class': 'search-view-by-dropdown'}).option['value'])
    total_pages = ceil(number_items / items_per_page)
    return total_pages


# cdw_web_scrap()
