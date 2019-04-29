import requests


class Job():
    """
    使用BeautifulSoup、Xpath、Selenium、Scrapy完成项目
    """
    def __init__(self):
        # 初始化项目中用到的变量
        self.base_url = ""

    def get_url_list(self):
        # 通过base_url获得url_list
        url_list = []

    def get_html_text(self, url):
        # 通过url获取当前页面中的html文本 ==>
        response = requests.get(url)
        response.status_code = requests.exceptions
        if response.status_code == 200:
            return response.text

    def parse_page_info(self, html):
        # 使用BeautifulSoup、Xpath、Selenium、Scrapy完成数据匹配
        return []

    def save_info(self, item):
        # 使用Redis，MySQL，MongoDB存储
        pass

    def run(self):
        # 入口函数
        for url in self.get_html_text(self.base_url):
            html = self.get_html_text(url)
            for item in self.parse_page_info(html):
                self.save_info(item)


job = Job()
job.run()