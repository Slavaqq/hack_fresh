import requests

def main():
    r = requests.get("http://freshpoint.freshserver.cz/frontend/web/index.php?r=device%2Fview&id=60")
    print(r.text)

main()
