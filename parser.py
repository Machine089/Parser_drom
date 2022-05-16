import requests
from bs4 import BeautifulSoup
import csv
import subprocess

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (HTML, like Gecko) '
                         'Version/15.0 Safari/605.1.15',
           'accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'}
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_="css-98q0l3")
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_="css-1wltzny")

    cars = []
    for item in items:
        cars.append({
            'title': item.find('span').get_text(),
            'price': item.find('span', class_="css-byj1dh").get_text().replace('\xa0', ''),
            'city': item.find('span', class_="css-1mj3yjd").get_text(),
            'link': item.get('href')
        })

    return cars


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Model', 'Price', 'City', 'Link'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['city'], item['link']])


def parse():
    URL = input('Enter URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Parsing page {page} from {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print(f"Received {len(cars)} cars")
        subprocess.call(['open', FILE])
    else:
        print(f'Error - {html.status_code}')


parse()
