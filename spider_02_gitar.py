import requests


class TieBaSpider():
    def __init__(self, max_page, keyword):
        self.max_page = max_page
        self.keyword = keyword
        self.base_url = "http://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}

    def get_url_list(self):
        # 获取url列表
        # url_list = []
        # for page in range(0, self.max_page, 50):
        #     url = self.base_url.format(self.keyword, page)
        #     url_list.append(url)
        # return url_list

        # 高端写法
        return [self.base_url.format(self.keyword, page) for page in range(0, self.max_page, 50)]

    def get_response(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def get_items(self, content):
        # 打印要解码
        print(content.decode())

    def parse_items(self, content):
        # 保存的时候, 字节直接保存就可以了
        with open("./tie_ba.html", "wb") as f:
            f.write(content)

    def run(self):
        # 获取url列表
        url_list = self.get_url_list()

        # 发送请求, 获取响应
        for url in url_list:
            content = self.get_response(url)
            # 提取数据
            self.get_items(content)
            # 处理数据
            self.parse_items(content)


if __name__ == '__main__':
    spider = TieBaSpider(200, "吉他吧")
    spider.run()