from typing import Dict, List, Union

import requests
import bs4

URL = "https://my.freshpoint.cz/device/product-list/60"
NO_SALE = "0%"


def get_content(url: str) -> bytes:
    """Return content from URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def cook_soup(content: bytes) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(content, "html.parser")


def get_items(soup: bs4.BeautifulSoup) -> List[Dict[str, Union[str, int]]]:
    items_table = soup.find_all("tbody")[-1]
    return [get_item(tr) for tr in items_table.find_all("tr")]


def get_item(tr: bs4.element.Tag) -> Dict[str, Union[str, int]]:
    return {
        "item": get_name(tr),
        "quantity": get_quantity(tr),
        "price": get_price(tr),
        "sale": get_sale(tr),
    }


def get_quantity(tr: bs4.element.Tag) -> int:
    return int(tr.find_all("td")[1].text)


def get_name(tr: bs4.element.Tag) -> str:
    return tr.find_all("td")[0].text


def get_price(tr: bs4.element.Tag) -> str:
    try:
        return tr.find_all("td")[4].text
    except IndexError:
        return tr.find_all("td")[2].text


def get_sale(tr: bs4.element.Tag) -> str:
    try:
        return tr.find_all("td")[3].text
    except IndexError:
        return NO_SALE


def scrap(url: str) -> List[Dict[str, Union[str, int]]]:
    content = get_content(url)
    soup = cook_soup(content)
    current_items = get_items(soup)
    return current_items


def main() -> None:
    print(scrap(URL))


if __name__ == "__main__":
    main()
