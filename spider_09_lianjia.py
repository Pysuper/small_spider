import json

import requests
from lxml import etree
from pprint import pprint
from multiprocessing import Process, JoinableQueue


class LianJiaSpider():
    def __init__(self):
        self.base_url = "https://sh.lianjia.com/zufang/pg{}/#contentList"
        self.headers = {
            "Referer": "https://sh.lianjia.com/zufang/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        self.url_queue = JoinableQueue()
        self.html_queue = JoinableQueue()
        self.item_queue = JoinableQueue()

    def get_url_list(self):
        for page in range(1, 101):
            url = self.base_url.format(page)
            self.url_queue.put(url)

    def get_html(self):
        while True:
            url = self.url_queue.get()
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                self.html_queue.put(response.text)
                self.url_queue.task_done()

    def get_item(self):
        while True:
            html = self.html_queue.get()
            html_xpath = etree.HTML(html)
            title_list = html_xpath.xpath('//div[@class="content__list"]/div/div/p[1]/a/text()')
            href_list = html_xpath.xpath('//div[@class="content__list"]/div/div/p[1]/a/@href')
            location_1_list = html_xpath.xpath('//div[@class="content__list"]/div/div/p[2]/a[1]/text()')
            location_2_list = html_xpath.xpath('//div[@class="content__list"]/div/div/p[2]/a[2]/text()')
            location_3_list = html_xpath.xpath('//div[@class="content__list"]/div/div/p[2]/text()')
            date_list = html_xpath.xpath('//div[@class="content__list"]/div/div/p[4]/text()')
            money_list = html_xpath.xpath('//div[@class="content__list"]/div/div/span/em/text()')

            a = 0  # 为列表拆分 ==> a += 7
            for title, href, location_1, location_2, info, date, money in \
                    zip(title_list, href_list, location_1_list, location_2_list, location_3_list, date_list,
                        money_list):
                if a > 203:
                    break
                location_info_list = location_3_list[a:a + 7]  # 通过遍历拆分列表
                area = location_info_list[3].replace("\n", '').replace(" ", '')
                path = location_info_list[4].replace(" ", '')
                structure = location_info_list[5].replace("\n", '').replace(" ", '')

                item = {
                    "标题": title.replace("\n", '').replace(" ", ''),
                    "链接": "https://sh.lianjia.com" + href,
                    "位置": location_1 + "-" + location_2,
                    "面积": area,
                    "朝向": path,
                    "房型": structure,
                    "发布": date.replace("\n", '').replace(" ", ''),
                    "租金": money + "元/月"
                }

                a += 7
                self.item_queue.put(item)
            self.html_queue.task_done()

    def parse_item(self):
        while True:
            item = self.item_queue.get()
            # with open('./lianjia.txt', 'a', encoding='utf-8') as f:
            #         item_info = json.dumps(item)
            #         f.write(item_info + "\n")    # 这里的item是字典, 要转换成字符串写入
            #         pprint(item)
            pprint(item)
            self.item_queue.task_done()

    def run(self):
        tasks = []

        get_url_list_task = Process(target=self.get_url_list)  # 这里只能传引用
        tasks.append(get_url_list_task)

        for num in range(5):  # 调整这里的数字, 尽量让第一个处理的队列中没有数据存着 ==> 这里的线程数多一些
            get_html_task = Process(target=self.get_html)
            tasks.append(get_html_task)

        for num in range(10):
            get_item_task = Process(target=self.get_item)
            tasks.append(get_item_task)

        parse_item_task = Process(target=self.parse_item)
        tasks.append(parse_item_task)

        for task in tasks:
            # 设置守护进程
            task.daemon = True
            task.start()

        # !!!退出条件!!!
        for q in [self.url_queue, self.html_queue, self.item_queue]:
            q.join()

        # 上面的退出条件就是这个意思
        # self.url_queue.join()
        # self.html_queue.join()
        # self.item_queue.join()


if __name__ == '__main__':
    lian_jia = LianJiaSpider()
    lian_jia.run()
