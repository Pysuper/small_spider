import json
import requests
from urllib.parse import urlencode


class ZhiTong():
    """
    使用多进程和多线程 ==> 队列 ==> 生产消费模式
    """

    def __init__(self):
        # 初始化类属性
        self.base_url = "http://www.job5156.com/s/result/ajax.json?"
        self.num = int(input("请输入抓取页数： "))
        self.keyword = input("请输入工作名称： ")   # 这里的城市可以通过GET城市代码，让用户选择城市


    def get_url_list(self):
        for page in range(1, self.num):
            data = {
                'keyword': self.keyword,
                'keywordType': 0,
                'locationList': 14010000,
                'pageNo': page
            }
            yield self.base_url + urlencode(data)

    def get_html(self, url):
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text

    def get_item(self, html):
        # 在这里使用标签选择的方法，提取出item
        # 这里直接获取当前网页源码， 获取的是字符串， 需要使用json转换成字典格式
        html_dict = json.loads(html)
        items = html_dict["page"]["items"]
        for info in items:
            item = {
                "name": info["posName"].replace("<em>", '').replace("</em>", ''),
                "work_location": info["workLocationList"][0]["provName"]
                                 + info["workLocationList"][0]['cityName']
                                 + info["workLocationList"][0]["townName"],
                "com_name": info["comName"],
                "other": ",".join(info["taoLabelList"]),  # 这个方法很实用 ==> 直接把列表变成了字符串
                "money": info["salaryStrByThousandMonth"]
            }
            yield item

    def save_items(self, item):
        # 在这里存储数据， 返回数据保存状态
        print(item)

    def run(self):
        for url in self.get_url_list():
            html = self.get_html(url)
            for item in self.get_item(html):
                self.save_items(item)


if __name__ == '__main__':
    zhi_tong = ZhiTong()
    zhi_tong.run()
