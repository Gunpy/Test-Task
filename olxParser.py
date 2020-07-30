import  requests
from bs4 import BeautifulSoup
import csv
import time

#URL = 'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/arenda-kvartir-komnat/odessa/'
HEADERS = {'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Mobile Safari/537.36', 'accept':'*/*'}
FILE = 'input.csv'

def get_html(url, params = None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def clean(text):
    return text.replace('\t', '').replace('\n', '').strip()

def get_pg_count(html):
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'lxml')
    pageination = soup.find_all('span', class_='item')
    if pageination:
        return int(pageination[-1].get_text())
    else:
        return 1


def get_content(html):
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('div', class_ ='offer-wrapper')
    rows = soup.find_all('tr',class_ ='wrap')
    result = []
    for row in rows:
        bottom = row.find('td', {'valign': 'bottom'})
        result.append({
            # url = row.find('h3').find('a').get('href')
            'title': clean(row.find('div', class_='space').get_text(strip=True)),
            'link' : clean(row.find('h3').find('a').get('href')),
            'price': clean(row.find('p',class_='price').get_text()),
            'address': clean(bottom.find('small', {'class': 'breadcrumb x-normal'}).text)

        })
    return  result

def save_list(items, path):
    with open(path, 'w', newline='', encoding='utf8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Title', 'Link', 'Price', 'Address'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price'], item['address']])



def parse():
    html = get_html(URL)
    if html.status_code == 200:
        house = []
        pg_count = get_pg_count(html.text)
        for page in range(1, pg_count + 1):
            print(f'Scraping {page} from {pg_count}')
            html = get_html(URL, params={'page': page})
            house.extend(get_content(html.text))
            time.sleep(1)
        save_list(house, FILE)
        print(f'Grab {len(house)} Item ')
    else:
        print("Fail connection")


URL = input('Please Input URL: ')
URL = URL.strip()
parse()
