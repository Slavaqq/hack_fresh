import json
from typing import Dict, List, Union, Optional

import falcon

import scrap

URL = "https://my.freshpoint.cz/device/product-list/60"
MIN_SALE = 5


class All:
    def on_get(self, request, response):
        search = request.get_param("search")
        response.body = json.dumps(index(URL, search), ensure_ascii=False, indent=2)


class Sale:
    def on_get(self, request, response):
        min_sale = request.get_param("min_sale")
        try:
            min_sale = MIN_SALE if min_sale is None else int(min_sale)
        except ValueError:
            raise falcon.HTTPBadRequest(description=f"Invalid value: '{min_sale}'!")
        response.body = json.dumps(sales(URL, min_sale), ensure_ascii=False, indent=2)


def index(url: str, search: Optional[str]) -> List[Dict[str, Union[str, int]]]:
    items = scrap.scrap(url)
    if search is None:
        return items
    return [item for item in items if search.lower() in item["item"].lower()]


def sales(url: str, min_sale: int) -> List[Dict[str, Union[str, int]]]:
    items = scrap.scrap(url)
    return [item for item in items if int(item["sale"][:-1]) >= min_sale]


app = falcon.API()
app.add_route("/", All())
app.add_route("/sales", Sale())
