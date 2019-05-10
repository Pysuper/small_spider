import json
import requests
from queue import Queue
from pprint import pprint
from urllib.parse import urlencode


class Tencent():
    def __init__(self):
        self.base_url = "https://careers.tencent.com/tencentcareer/api/post/Query?"
        self.header = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
        self.info_queue = Queue()

    def get_url_list(self):
        for page in range(10):
            data = {
                "pageIndex": page,
                "pageSize": 10
            }
            url = self.base_url + urlencode(data)
            yield url

    def get_html(self, url):
        response = requests.get(url, self.header)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            self.info_queue.put(response.text)  # 把数据放入管道中

    def parse_info(self):
        info = self.info_queue.get()  # 从管道取出数据
        data = json.loads(info)
        items = data["Data"]["Posts"]
        for item in items:
            work_info = {
                "岗位名称": item["RecruitPostName"],
                "标签": item["BGName"],
                "工作地点": item["LocationName"],
                "就业方向": item["CategoryName"],
                "发布日期": item["LastUpdateTime"],
                "职位介绍": item["Responsibility"].replace("\r\n", "").replace("\n", "")
            }
            pprint(work_info)
        self.info_queue.task_done()  # ！！！必须操作，否则容易出错

    def run(self):
        for url in self.get_url_list():
            self.get_html(url)
            self.parse_info()


if __name__ == '__main__':
    Ajax = Tencent()
    Ajax.run()
