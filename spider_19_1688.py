# -*- coding:utf-8 -*-

import json
from pprint import pprint
from urllib.request import Request, urlopen

import jsonpath
import requests


class Json():
    def __init__(self):
        self.url = "http://www.lagou.com/lbs/getAllCitySearchLabels.json"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0)'}

    def get_json(self):
        # 这里使用requests无法获取网页源码
        request = Request(self.url, headers=self.headers)
        response = urlopen(request)
        html = response.read()
        html_dict = json.loads(html)

        # 从字典中获取当前页面中的数据(城市名)
        # pprint(html_dict['content']['data']['allCitySearchLabels'])

        """第一种方法"""
        # 在这里遍历取出当前字典中所有的key
        for key in html_dict['content']['data']['allCitySearchLabels']:
            value_list = html_dict['content']['data']['allCitySearchLabels'][key]
            # 再使用key去遍历对应value的列表
            for i in value_list:
                # 获取当前key对应的value中的每一个值
                print(i['name'])

                # 在拿到一个值,就把他写入到文件中去==>文件追加写入
                with open('name.txt', 'a') as f:
                    f.write(i['name'] + "\n")

        """第二种方法"""
        # 这里是使用jsonpath层级筛选数据 ==> 类似于xpath
        # namelist = jsonpath.jsonpath(jsonobj, '$..name')


#         for name in namelist:
#             pass
#             # print(name)
#
#         # 把列表存储为字符串
#         # nametext = json.dumps(namelist, ensure_ascii=False)
#         # with open('name.txt', 'w') as file:
#         #     file.write(nametext.encode("utf-8"))
#         #     file.close()


#
#
if __name__ == "__main__":
    jsono = Json()
    jsono.get_json()
