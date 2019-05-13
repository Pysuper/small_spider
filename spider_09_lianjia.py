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

    #             self.url_queue = JoinableQueue()
    #         self.html_queue = JoinableQueue()
    #         self.item_queue = JoinableQueue()

    def get_url_list(self):
        return [self.base_url.format(page) for page in range(1, 101)]

    def get_html(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.text

    #
    def get_item(self, html):
        html_xpath = etree.HTML(html)
        info_list = html_xpath.xpath('//div[@class="content__list--item"]/div')
        for info in info_list:
            print(info)
            item = {
                "title": info.xpath('/p[1]/@href'),
            }
            yield item

    def parse_item(self, item):
        pprint(item)

    def run(self):
        for url in self.get_url_list():
            html = self.get_html(url)
            for item in self.get_item(html):
                self.parse_item(item)

                break
            break


if __name__ == '__main__':
    lian_jia = LianJiaSpider()
    lian_jia.run()
