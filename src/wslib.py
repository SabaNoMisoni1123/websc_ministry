import requests
from bs4 import BeautifulSoup


def test():
    url = "https://www.soumu.go.jp/news.rdf"
    response = requests.get(url)
    response.encoding = "shift_jis"
    print(response.text)


if __name__ == "__main__":
    test()
