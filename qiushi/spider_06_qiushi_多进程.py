import requests
from lxml import etree
from multiprocessing import Process # 只是更改设置守护进程
from multiprocessing import JoinableQueue # 底层使用进程间通信, 上层接口和Queue一样

class QiuShi():
    def __init__(self):
        self.base_url = "https://www.qiushibaike.com/8hr/page/{}/"
        self.url_queue = JoinableQueue()
        self.html_queue = JoinableQueue()
        self.item_queue = JoinableQueue()

    def get_utl_list(self):
        # 生成url, 把url放入到url队列中
        for page in range(1, 14, 1):
            self.url_queue.put(self.base_url.format(page))

    def get_html(self):
        # 从url队列中取出url, 使用url发送请求,把html放入到html队列中
        while True:
            url = self.url_queue.get()
            response = requests.get(url)
            if response.status_code == 200:
                self.html_queue.put(response.text)
                self.url_queue.task_done()  # 在put之后,只有一个get并不能把队列中的内容完全清理掉 ==>

    def get_items(self):
        # 从html队列中取出html, 在html中提取item, 把item放入item队列
        while True:
            html = self.html_queue.get()
            xpath_html = etree.HTML(html)
            titles = xpath_html.xpath('//div[@class="recmd-right"]/a/text()')
            for item in titles:
                self.item_queue.put(item)
            self.html_queue.task_done()

    def parse_items(self):
        # 从item队列中取出item, 处理item
        while True:
            item = self.item_queue.get()
            print(item)
            self.item_queue.task_done()

    def run(self):

        tasks = []

        get_url_list_task = Process(target=self.get_utl_list)    # 这里只能传引用
        tasks.append(get_url_list_task)

        for num in range(13):    # 调整这里的数字, 尽量让第一个处理的队列中没有数据存着 ==> 这里的线程数多一些
            get_html_task = Process(target=self.get_html)
            tasks.append(get_html_task)

        for num in range(20):
            get_item_task = Process(target=self.get_items)
            tasks.append(get_item_task)

        parse_item_task = Process(target=self.parse_items)
        tasks.append(parse_item_task)

        for task in tasks:
            # 设置守护进程
            task.daemon = True
            task.start()

        # !!!退出条件!!!
        # for q in [self.url_queue, self.html_queue, self.item_queue]:
        #     q.join()

        # 上面的退出条件就是这个意思
        self.url_queue.join()
        self.html_queue.join()
        self.item_queue.join()


if __name__ == '__main__':
    qiu_shi = QiuShi()
    qiu_shi.run()
