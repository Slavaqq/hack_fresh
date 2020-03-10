import requests
import bs4

URL = "http://freshpoint.freshserver.cz/frontend/web/index.php?r=device%2Fview&id=60"

def main():
    r = requests.get(URL)
    # print(r.content)
    soup = bs4.BeautifulSoup(r.content, "html.parser")
    tables = soup.find_all("tbody")
    for table in tables:
        goods = {}
        for row in table.find_all("tr"):
            good = row.find_all("td")[0].text
            quantity = row.find_all("td")[1].text
            goods[good] = quantity

    print(goods)

main()
