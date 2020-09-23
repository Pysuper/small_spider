# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Zheng Xingtao
# File : spider_29_track.py
# Datetime : 2020/8/21 下午2:47
import json
from pprint import pprint

import requests


class Track(object):
    def __init__(self):
        self.base_url = "https://t.17track.net/restapi/track"
        self.Hans = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from=en&to=zh-Hans"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36", }
        self.data = {"data": [{"num": "3448428395", "fc": 0, "sc": 0}], "guid": "11327674626d49e68cd8389502e3090a", "timeZoneOffset": 100000000000}

    def get_uid(self, url):
        response = requests.post(url, data=json.dumps(self.data), headers=self.headers)
        pprint(response.text)

    def get_html(self, url):
        data = {"data": [{"num": "3448428395", "fc": 0, "sc": 0}], "guid": "a3ffda8c82124146884e6453519f3d45",
                "timeZoneOffset": -480}
        response = requests.post(url, data=json.dumps(data), headers=self.headers)
        pprint(response.text)
        # if requests.status_codes == 200:
        #     return response.text
        # return None

    def parse_items(self, html):
        ...

    def save_items(self):
        ...

    def run(self):
        self.get_uid(self.base_url)


Track().run()

# data = {
#     "data":
#         [
#             {"num": "3448428395", "fc": 0, "sc": 0},
#             {"num": "8049758990", "fc": 0, "sc": 0},
#             # {"num": "8049828194", "fc": 0, "sc": 0},
#             # {"num": "9462973936", "fc": 0, "sc": 0},
#             # {"num": "5534745252", "fc": 0, "sc": 0},
#             # {"num": "8049757951", "fc": 0, "sc": 0},
#             # {"num": "7141403706", "fc": 0, "sc": 0},
#             # {"num": "3448887120", "fc": 0, "sc": 0}
#         ],
#     "guid": "",
#     "timeZoneOffset": -480
# }
