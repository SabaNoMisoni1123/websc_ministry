import datetime as dt

import feedparser
import requests
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta


# ID: micNEWS
def get_mic_news(url, arg_dict):
    response = requests.get(url)
    response.encoding = "shift-jis"

    soup = BeautifulSoup(response.content, "html.parser")
    table_row = soup.find_all("tr")[1:]

    ret_list = []
    for r in table_row:
        cols = r.find_all("td")

        ret_list.append(
            {
                "epoch": int(
                    dt.datetime.strptime(
                        cols[0].string, arg_dict["dateFormat"]
                    ).timestamp()
                ),
                "title": cols[1].string,
                "url": arg_dict["baseURL"] + cols[1].a.get("href"),
                "org": cols[2].string,
            }
        )

    last_month = dt.datetime.today() + relativedelta(months=-1)
    url_last_month = (
        f"https://www.soumu.go.jp/menu_news/s-news/{last_month.strftime('%y%m')}m.html"
    )
    print(url_last_month)
    response = requests.get(url_last_month)
    response.encoding = "shift-jis"
    soup = BeautifulSoup(response.content, "html.parser")
    table_row = soup.find_all("tr")[1:]

    for r in table_row:
        cols = r.find_all("td")

        ret_list.append(
            {
                "epoch": int(
                    dt.datetime.strptime(
                        cols[0].string, arg_dict["dateFormat"]
                    ).timestamp()
                ),
                "title": cols[1].string,
                "url": arg_dict["baseURL"] + cols[1].a.get("href"),
                "org": cols[2].string,
            }
        )

    return ret_list
