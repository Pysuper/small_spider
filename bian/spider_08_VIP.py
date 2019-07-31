import os
import requests
from lxml import etree
from urllib.request import urlopen, Request


class BiAnImage():
    def __init__(self):
        self.base_url = "http://pic.netbian.com"
        self.header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}

    def get_html(self, url):
        response = requests.get(url, self.header)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
        return None

    def get_url_1_list(self, html_1):
        url_1_items = []
        title_1_items = []
        x_html = etree.HTML(html_1)
        url_list = x_html.xpath('//div[@id="main"]/div[2]/a/@href')
        title_list = x_html.xpath('//div[@id="main"]/div[2]/a/text()')
        for url, title in zip(url_list, title_list):
            url_1_items.append(self.base_url + url)
            title_1_items.append(title)
        return title_1_items, url_1_items

    def get_url_2_list(self, html_2):
        url_2_items = []
        title_2_items = []
        x_html = etree.HTML(html_2)
        url_list = x_html.xpath('//ul[@class="clearfix"]/li/a/@href')
        title_list = x_html.xpath('//ul[@class="clearfix"]/li/a/b/text()')
        last_page = x_html.xpath('//a[text()="下一页"]/preceding-sibling::a[1]/text()')  # 直接查找下一页 => 上一个元素
        for url, title in zip(url_list, title_list):
            url_2_items.append(self.base_url + url)
            title_2_items.append(title)
        return url_2_items, title_2_items, last_page

    def get_image_url(self, image_html):
        # TODO: 怎么在图片详情页获取到当前这个图片的下载链接
        x_image_html = etree.HTML(image_html)
        image_url = x_image_html.xpath('//a[@id="img"]/img/@src')
        return self.base_url + image_url[0]

    def save_image(self, save_path, image_name, image_url):
        req = Request(url=image_url, headers=self.header)
        content = urlopen(req).read()
        img_name = image_name.replace(' ', '') + image_url[-4:]
        with open(save_path + img_name, 'wb') as f:
            f.write(content)
            print(img_name, "下载完成...")

    def run(self):
        # 获取所有分类标题, 链接
        html = self.get_html(self.base_url)
        title_1_items, url_1_items = self.get_url_1_list(html)
        for title_1, url_1 in zip(title_1_items, url_1_items):
            # if title_1 == "4K风景": TODO: 这里加一个判断就可以下载指定分类下的图片
            html_2 = self.get_html(url_1)
            url_2_items, title_2_items, last_page = self.get_url_2_list(html_2)

            # 通过拿到分类页面中的last_page, 获取该分类下所有页面链接
            for page in range(1, int(last_page[0])):
                if page == 1:
                    more_url_1 = url_1  # more_url_1 是每个分类下每一页的链接
                else:
                    more_url_1 = url_1 + "index_{}.html".format(page)
                detail_html = self.get_html(more_url_1)
                url_2_items, title_2_items, last_page = self.get_url_2_list(detail_html)

                # 获取当前页面中所有图片链接
                for url_2, title_2 in zip(url_2_items, title_2_items):
                    # print(title_1, url_1, last_page[0], more_url_1, title_2, url_2)
                    pictures = "/home/pysuper/Pictures/彼岸图网/"

                    # 在这里对下载的文件进行分类, 如果文件不存在, 就直接新建一个文件夹
                    if os.path.exists(pictures + title_1) is False:
                        os.makedirs(pictures + title_1)
                    save_path = pictures + title_1 + "/"
                    image_html = self.get_html(url_2)
                    img_url = self.get_image_url(image_html)
                    self.save_image(save_path, title_2, img_url)

                    break  # 跳出一个页面中所有图片链接
                break  # 跳出一个分类的所有页面
            break  # 跳出所有分类


bi_an = BiAnImage()
bi_an.run()
