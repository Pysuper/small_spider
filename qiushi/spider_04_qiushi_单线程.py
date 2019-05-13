import requests
from lxml import etree


class QiuShi():
    def __init__(self):
        self.base_url = "https://www.qiushibaike.com/8hr/page/{}/"

    def get_utl_list(self):
        return [self.base_url.format(page) for page in range(1, 14, 1)]

    def get_html(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None

    def get_items(self, html):
        # 获取标题
        xpath_html = etree.HTML(html)
        titles = xpath_html.xpath('//div[@class="recmd-right"]/a/text()')
        return titles

    def parse_items(self, items):
        for title in items:
            print(title)

    def run(self):
        # 获取url_list
        # 获取html
        # 获取item
        # 处理item
        url_list = self.get_utl_list()
        for url in url_list:
            html = self.get_html(url)
            items = self.get_items(html)
            self.parse_items(items)


if __name__ == '__main__':
    qiu_shi = QiuShi()
    qiu_shi.run()
