import json
from typing import Optional

import requests
import bs4

URL = "http://freshpoint.freshserver.cz/frontend/web/index.php?r=device%2Fview&id=60"
ITEMS_JSON = "items.json"


def get_content(url: str) -> Optional[str]:
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.content


def cook_soup(content: str) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(content, "html.parser")


def get_items(soup: bs4.BeautifulSoup) -> dict:
    items_table = soup.find_all("tbody")[-1]
    return {get_item(tr): get_quantity(tr) for tr in items_table.find_all("tr")}


def is_on_sale(soup: bs4.BeautifulSoup) -> bool:
    for h2 in soup.find_all("h2"):
        if "On Sale" in h2.text:
            return True
    return False


def get_sale_items(soup: bs4.BeautifulSoup) -> dict:
    items_table = soup.find("tbody")
    return {get_item(tr): get_sale(tr) for tr in items_table.find_all("tr")}


def get_quantity(tr) -> int:
    return int(tr.find_all("td")[1].text)


def get_item(tr) -> str:    
    return tr.find_all("td")[0].text


def get_sale(tr) -> str:
    return tr.find_all("td")[2].text


def save_json(obj, file_path):
    with open(file_path, "w") as f:
        json.dump(obj, f)


def open_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def items_diff(current: dict, previous: dict):
    current_set = set(current)
    previous_set = set(previous)
    intersection = current_set & previous_set
    diff = {}
    # 1. je v nabídce a počet se zvýšil
    diff["increase"] = {item: current[item] - previous[item] for item in intersection if current[item] > previous[item]} 
    # 2. je v nabídce a počet se snížil
    diff["decrease"] = {item: previous[item] - current[item] for item in intersection if current[item] < previous[item]}
    # 3. byl v nabídce a už není, vyprodano
    diff["out_of_stock"] = previous_set - current_set
    # 4. nebyl v nabídce a už je, naskladněno
    diff["new_in_stock"] = current_set - previous_set
    return diff


def changes_and_sales(soup: bs4.BeautifulSoup) -> dict:
    current_items = get_items(soup)
    previous_items = open_json(ITEMS_JSON)
    save_json(current_items, ITEMS_JSON)
    result = {"changes": {}, "sales": {}}
    result["changes"] = items_diff(current_items, previous_items)
    if is_on_sale(soup):
        result["sales"] = get_sale_items(soup)
    return result


def main():
    content = get_content(URL)
    if content is not None:
        soup = cook_soup(content)
        x = changes_and_sales(soup)
        print(x)


if __name__ == "__main__":
    main()
