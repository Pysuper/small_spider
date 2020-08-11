import time
import requests
from lxml import etree
from fake_useragent import UserAgent


class OpenBlog():
    def __init__(self):
        self.url = "https://www.baidu.com/s?ie=utf-8&wd=郑兴涛"
        self.header = {
            "User-Agent": UserAgent().random,
            "Host": "www.baidu.com",
            "Referer": "https://www.baidu.com/s?wd=%E9%83%91%E5%85%B4%E6%B6%9B&pn=40&oq=%E9%83%91%E5%85%B4%E6%B6%9B&ie=utf-8&usm=1&rsv_pq=a1cb6d540003db7e&rsv_t=206ed2Gvsb7%2FKRy%2BqCIDRq%2BdMkx7IzWoqR5mC19kSyp4JbJ%2BVZPmsbtOyWE",
        }

    def get_url(self, base_url):
        response = requests.get(base_url, headers=self.header)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
        return None

    def run(self, url):
        html = self.get_url(url)
        x_html = etree.HTML(html)
        blog = next = None
        try:
            blog = x_html.xpath('//a[text()="PySuper | Tao的个人博客"]/@href')[0]
        except:
            next = x_html.xpath('//a[text()="下一页>"]/@href')[0]
        if blog is None:
            time.sleep(1)
            self.run("https://www.baidu.com" + next)
        else:
            # 如果blog不为空，点击l
            print(blog)
            requests.get(blog, headers=self.header)
            time.sleep(1)
            return


for i in range(10):
    OpenBlog().run("https://www.baidu.com/s?ie=utf-8&wd=郑兴涛")
