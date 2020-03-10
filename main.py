import json
from typing import Optional

import requests
import bs4

URL = "http://freshpoint.freshserver.cz/frontend/web/index.php?r=device%2Fview&id=60"

def get_content(url: str) -> Optional[str]:
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.content


def get_items(content: str) -> dict:
    soup = bs4.BeautifulSoup(content, "html.parser")
    items_table = soup.find_all("tbody")[-1]
    return {get_item(tr): get_quantity(tr) for tr in items_table.find_all("tr")}


def get_quantity(tr):
    return int(tr.find_all("td")[1].text)


def get_item(tr):    
    return tr.find_all("td")[0].text


def save_json(obj, file_path):
    with open(file_path, "w") as f:
        json.dump(obj, f)

def main():
    content = get_content(URL)
    if content is not None:
        items = get_items(content)
        save_json(items, "items.json")

main()
