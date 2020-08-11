import time
import requests
from lxml import etree
from urllib.request import Request, urlopen


class SaveImage():
    def __init__(self):
        self.base_url = "https://cn.best-wallpaper.net"
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "ETag": "594gpnM6qpxwGpEvFYoNJpzY8YE="
        }

    def get_html(self, url):
        # 获取当前链接网页源码
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
        return None

    def get_detail_url_list(self, html):
        # 获取当前页面中指定url
        x_html = etree.HTML(html)
        url_list = x_html.xpath('//div[@id="c_m"]/li/a/@href')
        for url in url_list:
            detail_url = self.base_url + url
            yield detail_url

    def get_image_url_list(self, detail_url, detail_html):
        # 获取当前页面指定url
        x_detail_html = etree.HTML(detail_html)
        last_page = x_detail_html.xpath('//div[@class="pg_pointer"]/a/text()')[-2]
        for page in range(1, int(last_page)):
            image_url = detail_url[:-5] + "/page/" + str(page) + ".html"
            yield image_url

    def parse_image_html(self, image_html):
        # 获取当前页面指定url
        x_image_html = etree.HTML(image_html)
        image_detail_url_list = x_image_html.xpath('//div[@class="img_list"]/div/div/a/@href')
        for detail_url in image_detail_url_list:
            image_detail_url = self.base_url + detail_url
            yield image_detail_url

    def get_image_save_url(self, image_save_html):
        # 获取图片详情页链接
        x_image_save_html = etree.HTML(image_save_html)
        image_save_url = x_image_save_html.xpath('//div[@class="pic_view_tagsinfo"]/div[2]/a/@href')[0]
        return str(image_save_url)

    def save_image_info(self, image_save_url):
        # 这里是一张图片的下载链接 ==> 保存图片
        req = Request(image_save_url, headers=self.header)
        content = urlopen(req).read()

        with open("./images/%s" % image_save_url[-13:], 'wb') as f:
            f.write(content)
            print(image_save_url[-13:], image_save_url, "下载完成...")

    def run(self):
        start_time = time.time()
        html = self.get_html(self.base_url)
        for detail_url in self.get_detail_url_list(html):
            detail_html = self.get_html(detail_url)
            for image_url in self.get_image_url_list(detail_url, detail_html):
                # 在这里拿到所有页面的链接 ==> 解析图片链接
                image_html = self.get_html(image_url)
                for image_detail_url in self.parse_image_html(image_html):
                    image_save_html = self.get_html(image_detail_url)
                    image_save_url = self.get_image_save_url(image_save_html)
                    self.save_image_info(image_save_url)
                    break
                break
            break
        print(time.time() - start_time)


save_image = SaveImage()
save_image.run()
