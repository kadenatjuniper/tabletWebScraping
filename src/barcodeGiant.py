import requests
from bs4 import BeautifulSoup
from datetime import date
import sys


def barcodeGiant():
    print("----> STARTING: web scraping of BarcodeGiant.com")
    item_count = 0
    price_cart_encountered = 0
    discontinued_encountered = 0
    page_count = 0
    SOURCE_WEBSITE = 'barcode_giant'
    DATE_ACCESSED = str(date.today())

    file_string = f"web_scrap_{SOURCE_WEBSITE}_{DATE_ACCESSED}.csv"
    file = open(file_string, "w", encoding="utf-8")
    file.write("Title, Description, Price, Web_source, Link, Date_Accessed, Model #\n")

    while page_count < 698:
        URL = f"https://www.barcodegiant.com/cats/tablets/page/{page_count + 1}/show/25.htm"
        print(f"Pulling webpage {page_count}...")
        sys.stdout.flush()
        page_count += 1

        r = requests.get(URL)

        soup = BeautifulSoup(r.content, 'html.parser')

        items = soup.findAll('div', attrs={'class': 'item-area clearfix'})


        for item in items:
            if_price_cart = item.find('button', attrs={'title': 'See price in cart'})
            if_discontinued = item.find('button', attrs={'title': 'Discontinued - Need Assistance'})
            if not if_price_cart and not if_discontinued:
                title = 'None'
                description = 'None'
                price = 'None'
                link = 'None'
                title_object = item.find('h2', attrs={'class': 'product-name'}).a
                if title_object:
                    title = title_object['title'].strip('\n')
                    link = title_object['href']
                    model_number = title_object.find('span').text.split('|')[0].split(':')[-1].replace(' ', '')
                description_object = item.find('div', attrs={'class': 'details-area'}).div
                if description_object:
                    description = description_object.text.replace(',', '-').strip('\n')
                price_object = item.find('span', attrs={'class': 'price'})
                if price_object:
                    price = price_object.text.replace(',', '')
                file.write(f"{title}, {description}, {price}, {SOURCE_WEBSITE}, {link}, {DATE_ACCESSED}, {model_number}\n")
                item_count += 1
            else:
                if if_price_cart:
                    print("Price in cart encountered")
                    price_cart_encountered += 1
                elif if_discontinued:
                    print("Discontinued item encountered")
                    discontinued_encountered += 1

    print(f"----> FINISHED: Web scraping BarcodeGiant.com \nThe number of items saved to the file is {item_count}. \nPrice in cart was encountered {price_cart_encountered} times. \nDiscontinued Item was encountered {discontinued_encountered} times.")

    file.close()
    return file_string


# barcodeGiant()
