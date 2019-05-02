# from multiprocessing.dummy import Pool
# from queue import Queue
from multiprocessing import Pool
from multiprocessing import JoinableQueue as Queue
import requests
from lxml import etree


class QiuShiSpider():
    def __init__(self):
        self.base_url = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        self.url_queue = Queue()
        # 构建线程池
        self.pool = Pool()

    def get_url_list(self):
        for page in range(1, 14):
            page_url = self.base_url.format(page)
            self.url_queue.put(page_url)

    def exec_task(self):
        """
        这里从url_queue里面拿到任务, 处理整个url
        :return: 处理url的结果
        """
        # 发送请求, 获取数据
        req_url = self.url_queue.get()
        response = requests.get(req_url, headers=self.headers).text

        # 提取数据
        select = etree.HTML(response)
        title = select.xpath('//a[@class="recmd-content"]/text()')
        for title_info in title:
            # 保存数据
            # yield title_info
            print(title_info)

        # 一个url操作完成后, task_done()
        self.url_queue.task_done()

    def exec_task_finish(self, result):
        # for title in result:
        #     print(title)

        # 设置回调函数
        self.pool.apply_async(self.exec_task, callback=self.exec_task_finish)

    def run(self):
        self.get_url_list()

        # 使用线程池执行
        for i in range(5):
            self.pool.apply_async(self.exec_task, callback=self.exec_task_finish)

        # 任务退出的条件:
        self.url_queue.join()


if __name__ == '__main__':
    qiu_shi_spider = QiuShiSpider()
    qiu_shi_spider.run()
