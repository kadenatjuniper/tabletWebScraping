import requests
from bs4 import BeautifulSoup

item_dictionary = {}
price_cart_encountered = 0
discountinued_encountered = 0
page_count = 0

while discountinued_encountered < 1:
    URL = f"https://www.barcodegiant.com/cats/tablets/page/{page_count + 1}.htm"
    page_count += 1
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html.parser')

    items = soup.findAll('div', attrs={'class': 'item-area clearfix'})

    i = 0
    for item in items:
        if_price_cart = item.find('button', attrs={'title': 'See price in cart'})
        if_discontinued = item.find('button', attrs={'title': 'Discontinued - Need Assistance'})
        if not if_price_cart and not if_discontinued:
            title = 'None'
            description = 'None'
            price = 'None'
            title_object = item.find('h2', attrs={'class': 'product-name'}).a
            if title_object:
                title = title_object.text
            description_object = item.find('div', attrs={'class': 'details-area'}).div
            if description_object:
                description = description_object.text
            price_object = item.find('span', attrs={'class': 'price'})
            if price_object:
                price = price_object.text
            item_features = {'Title': title,
                             'Description': description,
                             'price': price, }
            item_dictionary[i] = item_features
        else:
            if if_price_cart:
                print("Price in chart encountered")
                price_cart_encountered += 1
            elif if_discontinued:
                print("Discontinued item encountered")
                discountinued_encountered += 1
        print(f"Page {i} has been processed...")
        i += 1

print(f"The length of dict is {len(item_dictionary)}.\n Price in cart was encountered {price_cart_encountered} times.\n Discontinued Iteam was encountered {discountinued_encountered} times.")

    