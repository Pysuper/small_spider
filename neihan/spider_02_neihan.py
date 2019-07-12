import re
import urllib
from urllib import request

import requests


class NeiHanSpider():
    def __init__(self):
        self.base_url = "https://www.neihan8.com/e/action/ListInfo/?classid=1&page={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
        }
        self.max_page = 100

        # 我想在这里使用全局变量, 定义一个num, 让它在后面的循环相加中可以使用
        self.num = 0

    def page_list_url(self):
        return [self.base_url.format(page) for page in range(self.max_page)]

    def parse_page_info(self, page_list_response):
        pattern = re.compile(r'<div class="pic-column-item box box-390 mr10">.*?<h3>.*?<a href="(.*?)" title=', re.S)
        results = pattern.findall(page_list_response)
        for result in results:
            detail_url = "https://www.neihan8.com" + result
            yield detail_url

    def parse_detail(self, detail_response):
        pattern = re.compile(r'</div>.*?<p>.*?<a href=.*?><img src="(.*?)" alt="', re.S)
        result = pattern.findall(detail_response)
        return result[0]

    def save_image(self, image_url, image_num):
        print("正在下载:", image_url)
        # request.urlretrieve(image_url, './images/{}.gif'.format(image_num))
        # 使用上面这种方式保存图片的时候, 会报错无法访问 ==> 没有headers
        response = urllib.request.Request(url=image_url, headers=self.headers)
        try:
        # 有些图片无法保存,打不开,异常处理
            with open('./images/{}.gif'.format(image_num), 'wb') as f:
                f.write(urllib.request.urlopen(response).read())
        except:
            pass

    def run(self):
        for page_list_url in self.page_list_url():
            page_list_response = requests.get(page_list_url, headers=self.headers)
            # print(page_list_response.content.decode())

            for detail_url in self.parse_page_info(page_list_response.content.decode()):
                detail_response = requests.get(detail_url, headers=self.headers)
                image_url = self.parse_detail(detail_response.content.decode())
                self.num += 1
                self.save_image(image_url, self.num)
                break
            # break


if __name__ == '__main__':
    nei_han = NeiHanSpider()
    nei_han.run()
