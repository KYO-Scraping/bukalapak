import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')

def home():
    return render_template('input.html')

@app.route('/page1')
def page_1():
    url = 'https://www.bukalapak.com/c/elektronik/home-theater'
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    main_area = soup.find('div', 'bl-flex-container flex-wrap is-gutter-16')
    item_area = main_area.find_all('div', 'bl-flex-item mb-8')

    item_list = []
    item_dict = {}

    for each_item in item_area:
        name = ''
        link = ''
        thumbnail = ''
        temp_sc_r = ''

        try:
            name = each_item.find('a', 'bl-link').text.strip()
            link = each_item.find('a', 'bl-link')['href']
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
        # print(each_item.find('img', 'bl-thumbnail--img').get('src'))

        if (name != 'No Name'):
            item_dict = {
                'name': name,
                'price': 'Rp ' + each_item.find('div', 'bl-product-card__description-price').text.strip()[2:],
                'rating': int(round(float(temp_sc_r[0:3].strip()))),
                'sold_count': int(temp_sc_r[temp_sc_r.find('Terjual ') + 8:].strip()),
                'location': each_item.find('span', 'mr-4').text.strip(),
                'thumbnail': thumbnail,
                'link': link
            }
            item_list.append(item_dict)
            print('')

    return render_template('input.html', item_list=item_list)

if __name__ == '__main__':
    app.run(debug=True)
