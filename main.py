import os
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

url = 'https://www.bukalapak.com/c/elektronik/home-theater'
html_doc = requests.get(url)
soup = BeautifulSoup(html_doc.text, 'html.parser')

main_area = soup.find('div', 'bl-flex-container flex-wrap is-gutter-16')
page_area = soup.find('ul', 'bl-ghostblock-pagination__list')

page_list = []
for p in page_area:
    if(p.text.strip().isdigit()):
        page_list.append(int(p.text.strip()))

item_area = main_area.find_all('div', 'bl-flex-item mb-8')

item_list = []
item_dict = {}

for each_item in item_area:
    name = ''
    thumbnail = ''
    temp_sc_r = ''

    try:
        name = each_item.find('a', 'bl-link').text.strip()
    except:
        name = 'No Name'

    try:
        temp_sc_r = each_item.find('div', 'bl-product-card__description-rating-and-sold').text.strip()
    except:
        temp_sc_r = 'No Sold Count or Rating'

    try:
        thumbnail = each_item.find('img', 'bl-thumbnail--img').get('src')
    except:
        thumbnail = 'No Thumbnail'

    if(name != 'No Name'):
        item_dict = {
            'name' : name,
            'price' : int(each_item.find('div', 'bl-product-card__description-price').text.strip()[2:].replace('.', '')),
            'rating' : float(temp_sc_r[0:3].strip()),
            'sold_count' : int(temp_sc_r[temp_sc_r.find('Terjual ')+8:].strip()),
            'location' : each_item.find('span', 'mr-4').text.strip(),
            'thumbnail' : thumbnail
        }
        item_list.append(item_dict)

print(item_list)
print('.')

# print(item_area[0].find('img', 'bl-thumbnail--img').get('src'))