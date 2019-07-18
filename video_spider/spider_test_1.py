"""
抓取网站视屏链接
"""
import json
from pprint import pprint
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import requests
from lxml import etree


class GetVideo():
    def __init__(self):
        self.base_url = "http://www.auto-mooc.com/api/v3/class/gettask"
        self.token = {
            "class_id": "EC209CF2D6F8EEFD06FCE3CFE8C20AEB",
            "major_id": "SQ180902A",
            "is_user": "0"
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Cookie": "Cookie: PHPSESSID=d0e41177e56eef9f8b05268a5bf17d96; _csrf=d-1AQiEzrTDJo_orXSsSj2nieTuIInLE; Hm_lvt_2c14f7c311b0de811807e6dbf0d97ee5=1560480230; Hm_lvt_a0969c8c5a4e76ff3e3bd17cdb2b38ca=1560480230; Hm_lvt_edecf4c5e2c06ea8ac4604445cfe4d1a=1560480230; Hm_lpvt_2c14f7c311b0de811807e6dbf0d97ee5=1560480267; Hm_lpvt_edecf4c5e2c06ea8ac4604445cfe4d1a=1560480267; uniqueVisitorId=ee6afc3e-18e4-d3e0-3bb1-0501662fc61b; Hm_lpvt_a0969c8c5a4e76ff3e3bd17cdb2b38ca=1560489779"
        }
        self.data = {
            "class_id": "EC209CF2D6F8EEFD06FCE3CFE8C20AEB",
            "item_id": "75D00602162CE0FD2A42706D424E0C62",
            "major_id": "SQ180902A"
        }

        # https://cd15-c120-1.play.bokecc.com/flvs/cb/QxEm3/hMa2QUbBjs-1.pcf?t=1560488416&key=03B0B1027F1666A288B7243591D230AB&tpl=10&tpt=111&upid=3242431560481216390&pt=0&pi=1&time_random=1560481218530_723598

    def get_url_html(self):
        # 加载token发送POST请求
        data = urlencode(self.token).encode()
        request = Request(url=self.base_url, data=data)
        response = urlopen(request)
        html = response.read().decode()
        return html

    def parse_html(self, html):
        # 这里的源码是字符串,需要转换成字典
        html_dict = json.loads(html)
        items = html_dict["data"]["list"]
        for item in items:
            # print(item["package_name"], len(item["itemList"]))  # 第一章 Python基础 26
            detail_items = item["itemList"]
            for detail_item in detail_items:
                yield {
                    "name": item["package_name"] + detail_item["item_name"],
                    "url": "http://www.auto-mooc.com" + detail_item["link_pc"]
                }

    def get_detail_html(self, item):
        # 在这里处理每个详情页面的链接
        response = requests.get(item["url"]+urlencode(self.data), headers=self.headers)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            print(response.text)

    def get_video_url(self, html):
        print(html)
        xpath_html = etree.HTML(html)
        pass

    def save_video(self, video_url):
        pass

    def run(self):
        html = self.get_url_html()
        for item in self.parse_html(html):
            self.get_detail_html(item)

            break


get_video = GetVideo()
get_video.run()
