import re
import requests
import six.moves
from lxml import etree
from urllib.parse import quote


class Job():
    """
    使用BeautifulSoup、Xpath、Selenium、Scrapy完成项目
    """

    def __init__(self):
        # 初始化项目中用到的变量
        self.keyword = input("请输入工作名称：")
        self.base_url = "https://search.51job.com/list/020000,000000,0000,00,9,99,{},2,{}.html?"

    def get_url_list(self):
        # 通过base_url获得url_list(列表推导式, url编码)
        return [self.base_url.format(quote(quote(self.keyword)), page) for page in range(1, 2)]

    def get_response(self, url):
        # 通过url获取当前页面中的html文本
        response = requests.get(url)
        response.encoding = response.apparent_encoding  # 编码
        if response.status_code == 200:
            return response.text

    def get_items(self, html):
        # 使用BeautifulSoup、Xpath、Selenium、Scrapy完成数据匹配
        work_name_list = []
        com_name_list = []
        work_place_list = []
        work_money_list = []
        print_day_list = []
        html = etree.HTML(html)

        # //*[@id="resultList"]/div[5]/p/span/a
        title_list = html.xpath('//*[@id="resultList"]/div/p/span/a/text()')[1:]
        comply_list = html.xpath('//*[@id="resultList"]/div/span[1]/a/@title')[1:]
        place_list = html.xpath('//*[@id="resultList"]/div/span[2]/text()')[1:]
        money_list = html.xpath('//*[@id="resultList"]/div/span[3]')[1:]
        day_list = html.xpath('//*[@id="resultList"]/div/span[4]/text()')[1:]

        for i in money_list:
            if i.text != None:
                work_money_list.append(i.text)
            else:
                work_money_list.append("暂无")

        for title, comply, place, money, day in six.moves.zip(title_list, comply_list, place_list, money_list, day_list):
            work_name = re.sub('\W', '', title)
            com_name = re.sub('\W', '', comply)
            work_place = re.sub('\W', '', place)
            print_day = re.sub('\W', '', day)

            work_name_list.append(work_name)
            com_name_list.append(com_name)
            work_place_list.append(work_place)
            print_day_list.append(print_day)
        return work_name_list, com_name_list, work_place_list, work_money_list, print_day_list

    def save_items(self, work_name_list, com_name_list, work_place_list, work_money_list, print_day_list):
        # 使用Redis，MySQL，MongoDB存储
        for work_name, com_name, work_place, work_money, print_day in six.moves.zip(work_name_list, com_name_list, work_place_list, work_money_list, print_day_list):
            print(work_name, com_name, work_place, work_money, print_day + "day")

    def run(self):
        # 入口函数
        for url in self.get_url_list():
            html = self.get_response(url)
            work_name_list, com_name_list, work_place_list, work_money_list, print_day_list = self.get_items(html)
            if len(work_money_list) > 0:
                print(url)
                self.save_items(work_name_list, com_name_list, work_place_list, work_money_list, print_day_list)
            else:
                break
            # break


job = Job()
job.run()
