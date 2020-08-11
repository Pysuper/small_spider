import re
import requests
from bs4 import BeautifulSoup


class Runoob():
    def __init__(self):
        self.base_url = 'http://www.runoob.com/'

    def get_html(self):
        response = requests.get(self.base_url)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text

    def get_item(self, html):
        html_soup = BeautifulSoup(html, 'lxml')
        title_list = html_soup.find("div", class_="col middle-column-home").find_all("a", class_="item-top item-1")
        href = re.findall(r'-1" href="(.*?)">', html, re.S)
        for title, src in zip(title_list, href):
            print({"title": title.h4.text, "src": "http:" + src})

    def parse_item(self, title):
        # 这里可以增加一步处理title
        pass

    def run(self):
        html = self.get_html()
        self.get_item(html)


runoob = Runoob()
runoob.run()
