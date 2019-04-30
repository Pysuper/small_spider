import requests
from urllib.parse import urlencode


class ZhiTong():
    """
    使用多进程和多线程
    """
    def __init__(self):
        # 初始化类属性
        self.base_url = "http://www.job5156.com/s/result/ajax.json?"
        self.data = {
            'keyword': input("请输入工作名称："),
            'keywordType': 0,
            'locationList': 14010000,
            'pageNo': 1
        }

    def get_url_list(self):
        return self.base_url + urlencode(self.data)

    def get_html(self, url):
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text

    def get_item(self, html):
        # 在这里使用标签选择的方法，提取出item
        return ""

    def save_items(self, items):
        # 在这里存储数据， 返回数据保存状态
        return "OK!"

    def run(self):
        for url in self.get_url_list():
            html = self.get_html(url)
            item = self.get_item(html)
            self.save_items(item)


zhitong = ZhiTong()
zhitong.run()