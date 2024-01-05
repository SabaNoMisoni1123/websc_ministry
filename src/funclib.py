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


# ID: digitalNews
def get_digital_news(url, arg_dict):
    ret_list = []

    for i in range(arg_dict["nPage"]):
        url_sub = url + f"page={i}"
        response = requests.get(url_sub)
        soup = BeautifulSoup(response.content, "html.parser")
        for card in soup.select("section.card"):
            category = (
                card.select_one("span.card__category")
                .get_text()
                .replace(" ", "")
                .replace("\n", "")
            )
            if category in arg_dict["notWatchCategory"]:
                continue

            ret_list.append(
                {
                    "url": arg_dict["baseURL"] + card.select_one("a").get("href"),
                    "title": f"（{category}） {card.select_one('.card__title > span').get_text()}",
                    "epoch": int(
                        dt.datetime.strptime(
                            card.select_one(".card__date > time").get("datetime"),
                            arg_dict["dateFormat"],
                        ).timestamp()
                    ),
                    "org": "デジタル庁",
                }
            )

    return ret_list


# ID: mlitNews
def get_mlit_news(url, arg_dict):
    today = dt.datetime.now()
    last_month = dt.datetime.today() + relativedelta(months=-1)
    urls = [
        url + f"/houdou{today.strftime('%Y%m')}.html",
        url + f"/houdou{last_month.strftime('%Y%m')}.html",
    ]
    ret_list = []

    for u in urls:
        response = requests.get(u)
        soup = BeautifulSoup(response.content, "html.parser")

        data = soup.select_one(arg_dict["dataListPath"])

        epoch = 0
        for c_tag in data.children:
            if c_tag.name == "dt":
                epoch = int(
                    dt.datetime.strptime(
                        c_tag.get_text(), arg_dict["dateFormat"]
                    ).timestamp()
                )
            elif c_tag.name == "dd":
                ret_list.append(
                    {
                        "epoch": epoch,
                        "title": c_tag.a.get_text(),
                        "url": arg_dict["baseURL"] + c_tag.a.get("href"),
                        "org": "国交省新着情報",
                    }
                )
            else:
                continue

    return ret_list
