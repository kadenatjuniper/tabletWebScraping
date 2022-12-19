import requests
from bs4 import BeautifulSoup
from datetime import date


def waypointtech():
    print("----> STARTING: web scraping of Allterra.com")
    item_count = 0
    SOURCE_WEBSITE = 'waypointtech'
    DATE_ACCESSED = str(date.today())

    file_string = f"web_scrap_{SOURCE_WEBSITE}_{DATE_ACCESSED}.csv"
    file = open(file_string, "w")
    file.write("Title, Description, Price, Web_source, Link, Date_Accessed, Model #\n")

    # This header makes it so the website doesn't realize this is a web scrapper. There is a create article with more tricks like this: https://pknerd.medium.com/5-strategies-to-write-unblock-able-web-scrapers-in-python-5e40c147bdaf
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

    URL = f"https://www.waypointtech.com/geospatial/trimble-t100-mwy8r-r76kl"
    r = requests.get(URL, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    title = soup.find('h1', attrs={'class': 'product-title'}).text.replace(',', '').replace('\n', '')
    description = soup.find('div', attrs={'class': 'product-excerpt'}).text.replace(',', '').replace('\n', '')
    price = soup.find('div', attrs={'class': 'product-price'}).text.replace(',', '').replace('\n', '')
    link = 'https://www.waypointtech.com/geospatial/trimble-t100-mwy8r-r76kl'
    model_number = ''

    file.write(f"{title}, {description}, {price}, {SOURCE_WEBSITE}, {link}, {DATE_ACCESSED}, {model_number}\n")
    item_count += 1


    print(f"----> FINISHED: Web scraping Waypointtech.com \nThe number of items saved to the file is {item_count}.")

    file.close()
    return file_string



# waypointtech()
