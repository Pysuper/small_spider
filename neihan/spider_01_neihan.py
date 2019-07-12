import re
from queue import Queue
from threading import Thread
from urllib import request

import requests


class NeiHanSpider():
    def __init__(self):
        self.base_url = "https://www.neihan8.com/e/action/ListInfo/?classid=1&page={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
        }
        self.proxies = {'http': '117.68.194.141:808'}
        self.max_page = 100

        # 我想在这里使用全局变量, 定义一个num, 让它在后面的循环相加中可以使用
        self.num = 0

        self.page_queue = Queue()
        self.detail_queue = Queue()
        self.image_queue = Queue()

    def page_list_url(self):
        # return [self.base_url.format(page) for page in range(self.max_page)]
        for page in range(self.max_page):
            # yield self.base_url.format(page)
            self.page_queue.put(self.base_url.format(page))

    def parse_page_info(self):
        """
        取出page_url, 处理后, 将结果放入detail_queue中
        :param page_url: 页面访问的链接
        """
        while True:
            page_url = self.page_queue.get()
            print(page_url)
            page_list_response = requests.get(page_url, headers=self.headers, proxies=self.proxies).text
            pattern = re.compile(r'<div class="pic-column-item box box-390 mr10">.*?<h3>.*?<a href="(.*?)" title=',
                                 re.S)
            results = pattern.findall(page_list_response)
            for result in results:
                detail_url = "https://www.neihan8.com" + result
                # yield detail_url
                self.detail_queue.put(detail_url)
            self.page_queue.task_done()

    def parse_detail(self):
        """
        将detail_url从队列中取出, 再将解析后的image_url放入image_queue中
        :param detail_url:页面访问的链接
        """
        while True:
            try:
                detail_url = self.detail_queue.get()
                detail_response = requests.get(detail_url, headers=self.headers, proxies=self.proxies).text
                pattern = re.compile(r'</div>.*?<p>.*?<a href=.*?><img src="(.*?)" alt="', re.S)
                image_url = pattern.findall(detail_response)[0]
                # image_name = image_url[-20:]
                # return image_url
                self.image_queue.put(image_url)
                self.detail_queue.task_done()
            except:
                continue

    def save_image(self):
        while True:
            image_url = self.image_queue.get()
            image_name = image_url[-20:]
            print("正在下载:", image_url)
            request.urlretrieve(image_url, './images/{}'.format(image_name))

    def run(self):
        task_list = []
        page_url_task = Thread(target=self.page_list_url)
        task_list.append(page_url_task)

        parse_page_task = Thread(target=self.parse_page_info)
        task_list.append(parse_page_task)

        parse_detail_task = Thread(target=self.parse_detail)
        task_list.append(parse_detail_task)

        for i in range(10):
            save_image_task = Thread(target=self.save_image)
            task_list.append(save_image_task)

        for task in task_list:
            task.setDaemon(True)
            task.start()

        for queue in [self.page_queue, self.detail_queue, self.image_queue]:
            queue.join()


if __name__ == '__main__':
    nei_han = NeiHanSpider()
    nei_han.run()
