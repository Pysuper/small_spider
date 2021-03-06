import requests
from lxml import etree


class XiCi():
    def __init__(self):
        self.base_url = "http://www.xicidaili.com/nn/{}"
        self.num = int(input("请输入抓取页数： "))
        self.header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/69.0.3497.81 Chrome/69.0.3497.81 Safari/537.36"}
        # self.proxy = {"http": "122.193.244.238:9999"} # 可以使用

    def get_url_list(self):
        return [self.base_url.format(page) for page in range(1, self.num)]

    def get_html(self, url):
        response = requests.get(url, headers=self.header)  # proxies = self.proxy
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        print(response.status_code, "无法访问")

    def get_item(self, html):
        soup_html = etree.HTML(html)
        ip_list = soup_html.xpath("//*[@id='ip_list']/tr/td[2]")
        port_list = soup_html.xpath("//*[@id='ip_list']/tr/td[3]")
        # anonymous_list = soup_html.xpath("//*[@id='ip_list']/tbody/tr/td[5]") 匿名

        return ip_list, port_list

    def parse_items(self, ip_list, port_list):
        for ip, port in zip(ip_list, port_list):
            print(ip.text + ":" + port.text)
            # 在这里可以在判断当前这个ip使用情况，再有选择性的输出 ==> 随便访问一个网站

    def run(self):
        for url in self.get_url_list():
            html = self.get_html(url)
            ip_list, port_list = self.get_item(html)
            self.parse_items(ip_list, port_list)


if __name__ == '__main__':
    xi_ci = XiCi()
    xi_ci.run()
