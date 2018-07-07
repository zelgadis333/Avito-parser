import requests
from bs4 import BeautifulSoup
import os
import csv
import time

def load_user_data(page, session, url):

    request = session.get(url)
    return request.text


def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text


def parse_user_datafile_bs(filename):
    resultsanswer = []
    text = open(filename, encoding='utf-8', newline='').read()

    soup = BeautifulSoup(text, "html.parser")
    item_list = soup.find_all('div', {'class': 'item_table-header'})
    i = 0
    for item in item_list:
        
        item_link = item.find('h3', {'class': 'item-description-title'}).find('a').get('href')
        item_title = item.find('h3', {'class': 'item-description-title'}).find('a').get('title')
        try:
            item_price = int(''.join(list(filter(str.isdigit, item.find('span', {'class': 'price'}).text))))
        except:
            item_price = 0
        url = 'https://www.avito.ru' + item_link
        session = requests.Session()
        request = session.get(url)
        site = request.text
        avito_id = item_link.split("_")[-1].split("=")[-1]
        soup = BeautifulSoup(site, "html.parser")
        try:
            item_description = soup.find('div', {'class': 'item-description'}).text
            item_date_add = site[site.find('размещено') + 10: site.find('размещено') + 35]
        except:
            item_description = ""
            item_date_add = ""
        try:
            item_address = soup.find_all('div', {'class': 'seller-info-prop'})[4].find('div', {'class': 'seller-info-value'}).text
        except:
            item_address = ""
        try:
            item_owner = soup.find('div', {'class': 'seller-info js-seller-info'}).find('a').text
        except:
            item_owner = ""
        resultsanswer.append([item_link, item_title, item_price, item_date_add, avito_id, item_description,
                                  item_address, item_owner])
        time.sleep(5)
    return resultsanswer


s = requests.Session()
s.headers.update({
        'Referer': 'http://www.avito.ru',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    })


page = 1
while page < 10:
    # print 'Loading page #%d' % (page)
    data = load_user_data(page, s,  'https://www.avito.ru/moskva/noutbuki?p=%d' % page)

    with open('./user_data/page_%d.html' % page, 'w', encoding='utf8') as output_file:
        output_file.write(data)
        page += 1


results = []
for filename in os.listdir('./user_data/'):
    results.extend(parse_user_datafile_bs('./user_data/' + filename))

fnames = ['item_link', 'item_title', 'item_price', 'item_date_add', 'avito_id', 'item_description', 'item_adress', 'item_owner']
f = open('numbers3.csv', 'w', encoding='utf-16')
writer = csv.DictWriter(f, fieldnames=fnames)
writer.writeheader()
for i in range(0, len(results)):
    writer.writerow({'item_link': results[i][0], 'item_title': results[i][1], 'item_price': results[i][2],
                     'item_date_add': results[i][3], 'avito_id': results[i][4], 'item_description': results[i][5],
                     'item_adress': results[i][6], 'item_owner': results[i][7]})
f.close()
