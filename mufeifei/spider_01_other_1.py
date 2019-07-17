from urllib.request import Request, urlopen

import requests
from lxml import etree


class FeiAngel():
    def __init__(self):
        self.base_url = "http://jq.9duw.com/yiyuele/news/78279"

    def get_url_list(self):
        url_list = []
        for page in range(1, 24):
            if page == 1:
                url = self.base_url + ".html"
            else:
                url = self.base_url + "_" + str(page) + ".html"
            url_list.append(url)
        return url_list

    def get_html(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
        return None

    def get_image_url(self, html):
        x_html = etree.HTML(html)
        image_url = x_html.xpath('//div[@id="mainNewsContent"]/p/img/@src')[0]
        return "http://jq.9duw.com" + image_url

    def save_image(self, image_url):
        request = Request(url=image_url)
        content = urlopen(request).read()
        with open("/home/spider-spider/Pictures/feiangel/%s" % image_url[-21:], 'wb') as f:
            f.write(content)
            print(image_url[-21:], "下载完成...")

    def run(self):
        url_list = self.get_url_list()
        print(len(url_list))
        for url in url_list:
            html = self.get_html(url)
            image_url = self.get_image_url(html)
            self.save_image(image_url)


fei_angel = FeiAngel()
fei_angel.run()
