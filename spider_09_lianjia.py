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

    def get_url_list(self):
        return [self.base_url.format(page) for page in range(1, 101)]

    def get_html(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.text

    #
    def get_item(self, html):
        html_xpath = etree.HTML(html)
        title_list = html_xpath.xpath('//div[@class="content__list"]/div/div/p[1]/a/text()')
        href_list = html_xpath.xpath('//div[@class="content__list"]/div/div/p[1]/a/@href')
        location_1_list = html_xpath.xpath('//div[@class="content__list"]/div/div/p[2]/a[1]/text()')
        location_2_list = html_xpath.xpath('//div[@class="content__list"]/div/div/p[2]/a[2]/text()')
        location_3_list = html_xpath.xpath('//div[@class="content__list"]/div/div/p[2]/text()')
        date_list = html_xpath.xpath('//div[@class="content__list"]/div/div/p[4]/text()')
        money_list = html_xpath.xpath('//div[@class="content__list"]/div/div/span/em/text()')

        a = 0  # 为列表拆分 ==> a += 7
        for title, href, location_1, location_2, info, date, money in \
                zip(title_list, href_list, location_1_list, location_2_list, location_3_list, date_list, money_list):
            if a > 203:
                break
            location_info_list = location_3_list[a:a + 7]  # 通过遍历拆分列表
            area = location_info_list[3].replace("\n", '').replace(" ", '')
            path = location_info_list[4].replace(" ", '')
            structure = location_info_list[5].replace("\n", '').replace(" ", '')

            item = {
                "标题": title.replace("\n", '').replace(" ", ''),
                "链接": "https://sh.lianjia.com" + href,
                "位置": location_1 + "-" + location_2,
                "面积": area,
                "朝向": path,
                "房型": structure,
                "发布": date,
                "租金": money + "元/月"
            }

            a += 7
            yield item

    def parse_item(self, item):
        pprint(item)

    def run(self):
        for url in self.get_url_list():
            html = self.get_html(url)
            for item in self.get_item(html):
                self.parse_item(item)


if __name__ == '__main__':
    lian_jia = LianJiaSpider()
    lian_jia.run()
