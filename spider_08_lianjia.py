import requests
from lxml import etree


class LianJiaSpider():
    def __init__(self):
        self.base_url = "https://sh.lianjia.com/zufang/pg{}/#contentList"
        self.headers = {
            "Referer": "https://sh.lianjia.com/zufang/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        pass

    def get_page_list(self):
        return [self.base_url.format(page) for page in range(1, 101)]

    def run(self):
        info_list = self.get_page_list()
        for page_info_url in info_list:
            page_response = requests.get(page_info_url, headers=self.headers)

            page_html = etree.HTML(page_response.text)
            house_info = page_html.xpath('//div[@class="content__list--item"]/div/p[1]/a/text()')
            # for i in house_info:
            #     print(i)

            areas_info1 = page_html.xpath('//div[@class="content__list--item"]/div/p[2]/a[1]/text()')
            areas_info2 = page_html.xpath('//div[@class="content__list--item"]/div/p[2]/a[2]/text()')
            for a, b in zip(areas_info1, areas_info2):
                print(a + b)

            areas_info_list = page_html.xpath('//div[@class="content__list--item"]/div/p[5]/i//text()')

            money_list = page_html.xpath('//div[@class="content__list--item"]/div/span/em/text()')
            for i in money_list:
                print(i.strip() + "元/月")

            print(money_list)
            for house, areas in zip(house_info, areas_info_list):
                print(house, areas)
            # break


if __name__ == '__main__':
    lian_jia = LianJiaSpider()
    lian_jia.run()
