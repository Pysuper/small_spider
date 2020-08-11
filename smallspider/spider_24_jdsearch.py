import re

import requests
from lxml import etree
from urllib.parse import urlencode


class JDSearch():
    def __init__(self):
        self.base_url = "https://search.jd.com/Search?" + urlencode({
            "keyword": "手机",
            "enc": "utf - 8",
            "qrst": 1,
            "rt": 1,
            "stop": 1,
            "vt": 2,
            "wq": "手机",
            "page": 1,
            "s": 55,
            "click": 0,
        })
        self.header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}

    def get_html(self, url):
        response = requests.get(url, headers=self.header)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text

    def parse_html(self, html):
        xpath_html = etree.HTML(html)
        goods_list = xpath_html.xpath('//ul[@class="gl-warp clearfix"]/li/div/div[1]//@href')
        for goods in goods_list:
            detail_url = "https:" + re.search(r'//(.*\.html)', goods).group()
            yield detail_url

    def parse_detail(self, detail_html):
        xpath_html = etree.HTML(detail_html)
        sku_name = xpath_html.xpath('//div[@class="sku-name"]/text()')[0].strip()
        # sku_price = xpath_html.xpath('//span[@class="p-price"]/span[2]/text()')
        item = {
            "sku_name": sku_name,
            # "sku_price": sku_price
        }
        return item

    def run(self):
        html = self.get_html(self.base_url)
        for detail_url in self.parse_html(html):
            detail_html = self.get_html(detail_url)
            item = self.parse_detail(detail_html)
            print(item)


jd = JDSearch()
jd.run()
