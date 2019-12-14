import json
import requests
from bs4 import BeautifulSoup


def get_links_for_db(url: str) -> str:
    data = requests.get(url).content
    soup = BeautifulSoup(data, 'html.parser')
    div = soup.find('table')

    for link in div.find_all('a'):
        yield link['href'][1:]


def create_fake_db(url) -> None:
    db = {}
    for link in get_links_for_db(url):
        db[link] = requests.get(f"{url}{link}").json()

    with open('fake_db.json', 'w') as f:
        json.dump(db, f, indent=2)


def get_db() -> dict:
    with open('fake_db.json', 'r') as f:
        return json.load(f)


def update_db(content) -> None:
    with open('data.json', 'w') as f:
        json.dump(content, f, indent=2)


if __name__ == '__main__':
    create_fake_db('https://jsonplaceholder.typicode.com/')
