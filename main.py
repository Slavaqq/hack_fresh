import json
from typing import Any, Dict

import requests
import bs4

URL = "http://freshpoint.freshserver.cz/frontend/web/index.php?r=device%2Fview&id=60"
ITEMS_JSON = "items.json"


def get_content(url: str) -> bytes:
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def cook_soup(content: bytes) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(content, "html.parser")


def get_items(soup: bs4.BeautifulSoup) -> Dict[str, int]:
    items_table = soup.find_all("tbody")[-1]
    return {get_item(tr): get_quantity(tr) for tr in items_table.find_all("tr")}


def is_on_sale(soup: bs4.BeautifulSoup) -> bool:
    for h2 in soup.find_all("h2"):
        if "On Sale" in h2.text:
            return True
    return False


def get_sale_items(soup: bs4.BeautifulSoup) -> Dict[str, str]:
    if is_on_sale(soup):
        items_table = soup.find("tbody")
        return {get_item(tr): get_sale(tr) for tr in items_table.find_all("tr")}
    return {}


def get_quantity(tr: bs4.element.Tag) -> int:
    return int(tr.find_all("td")[1].text)


def get_item(tr: bs4.element.Tag) -> str:
    return tr.find_all("td")[0].text


def get_sale(tr: bs4.element.Tag) -> str:
    return tr.find_all("td")[2].text


def save_json(obj: Any, file_path: str) -> None:
    with open(file_path, "w") as f:
        json.dump(obj, f, indent=4)


def open_json(file_path: str) -> Any:
    with open(file_path, "r") as f:
        return json.load(f)


def items_diff(current: Dict[str, int], previous: Dict[str, int]) -> Dict[str, int]:
    items_union = set(current) | set(previous)
    return {item: current.get(item, 0) - previous.get(item, 0) for item in items_union}


def main() -> None:
    content = get_content(URL)
    soup = cook_soup(content)
    previous_items = open_json(ITEMS_JSON)
    current_items = get_items(soup)
    save_json(current_items, ITEMS_JSON)
    sales_items = get_sale_items(soup)
    print(sales_items)
    diff_items = items_diff(current_items, previous_items)
    print(diff_items)


if __name__ == "__main__":
    main()
