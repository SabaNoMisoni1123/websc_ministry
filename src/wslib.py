import datetime as dt

import feedparser
import requests
from bs4 import BeautifulSoup

import funclib


class MinistrySiteDataGetter:
    def __init__(self):
        # 個別に実装した関数の登録
        self.func_dict = {
            "micNews": funclib.get_mic_news,
            "digitalNews": funclib.get_digital_news,
            "mlitNews": funclib.get_mlit_news,
        }

    def get(self, config: dict):
        self.name = config["name"]
        self.url = config["url"]
        self.use_default_func = config["useDefaultFunc"]
        self.arg = config["arg"]

        if self.use_default_func is True and self.arg["rss"] is True:
            return self._get_w_feedpaser()
        elif self.use_default_func is True:
            return self._get_w_beautifle_soup()
        else:
            return self.func_dict[config["funcID"]](self.url, self.arg)

    def _get_w_beautifle_soup(self):
        response = requests.get(self.url)

        if "encording" in self.arg.keys():
            response.encoding = self.arg["encoding"]

        soup = BeautifulSoup(response.content, "html.parser")
        data = soup.select(self.arg["dataListPath"])[0]

        return self._extract_data_from_soup(data)

    def _extract_data_from_soup(self, data):
        url_list = [
            self.arg["baseURL"] + u.find("a").get("href")
            for u in data.find_all(self.arg["path"]["url"])
        ]
        title_list = [t.get_text() for t in data.find_all(self.arg["path"]["title"])]
        date_list = [
            int(dt.datetime.strptime(d.get_text(), self.arg["dateFormat"]).timestamp())
            for d in data.find_all(self.arg["path"]["date"])
        ]

        if "org" in self.arg["path"].keys():
            org_list = [t.get_text() for t in data.find_all(self.arg["path"]["org"])]
        else:
            org_list = [self.name] * len(url_list)

        ret_list = []
        for u, t, d, o in zip(url_list, title_list, date_list, org_list):
            ret_list.append(
                {
                    "url": u,
                    "title": t,
                    "epoch": d,
                    "org": o,
                }
            )

        return ret_list

    def _get_w_feedpaser(self):
        ret_list = []
        res = feedparser.parse(self.url)
        data = self._move_feedpaser_dict(res, self.arg["dataListPath"])

        for art in data:
            art_dict = {
                "url": self._move_feedpaser_dict(art, self.arg["path"]["url"]),
                "title": self._move_feedpaser_dict(art, self.arg["path"]["title"]),
                "epoch": int(
                    dt.datetime.strptime(
                        art[self.arg["path"]["date"]], self.arg["dateFormat"]
                    ).timestamp(),
                ),
            }
            if "org" in self.arg["path"].keys():
                art_dict["org"] = self._move_feedpaser_dict(
                    art, self.arg["path"]["org"]
                )
            else:
                art_dict["org"] = self.name
            ret_list.append(art_dict)

        return ret_list

    def _move_feedpaser_dict(self, tree_dict, path):
        ret = tree_dict
        if type(path) is list:
            for p in path:
                ret = ret[p]
        else:
            ret = ret[path]

        return ret
