import requests
from lxml import etree
from urllib.parse import urlencode


class WeiXin():
    def __init__(self):
        self.base_url = "https://weixin.sogou.com/weixin?"
        self.key_word = input("请输入搜索的文章主题:")
        self.header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Cookie": "Cookie: ABTEST=6|1557819752|v1; IPLOC=CN3100; SUID=E9D268DF3E18960A000000005CDA7168; SUID=E9D268DF2D18960A000000005CDA7169; weixinIndexVisited=1; SNUID=142F9523FDF97528D24A07C2FD49EAC1; PHPSESSID=pjg9a3movbomudf0sqpe1hag21; SUV=00AB6A0FDF68D2E95CDA71863A063822; sct=1; JSESSIONID=aaa2SbDP5veZ64u4Wj1Qw",
            "Referer": "Referer: https://weixin.sogou.com/weixin?type=2&query=python&ie=utf8&s_from=input&_sug_=y&_sug_type_=&w=01019900&sut=809&sst0=1557819955000&lkt=7%2C1557819954078%2C1557819954898"
        }

    def get_url_list(self):
        for page in range(1, 3, 1):
            data = {
                "query": self.key_word,
                "page": 2,
                "sut": 809,
                "s_from": "input",
                "_sug_": "y",
                "type": 2,
                "sst0": 1557819955000,
                "ie": "utf8",
            }

            url = self.base_url + urlencode(data)

            yield url

    def get_html(self, url):
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            return response.text

    def get_detail_url(self, html):
        html_xpath = etree.HTML(html)
        cate_href_list = html_xpath.xpath('//ul[@class="news-list"]/li/div[2]/h3/a/@data-share')
        for cate_href in cate_href_list:
            yield cate_href  # 返回显示的标题详情页链接

    def get_item(self, detail_html, detail_url):
        detail_html_xpath = etree.HTML(detail_html)
        title = detail_html_xpath.xpath('//h2[@class="rich_media_title"]/text()')[0].replace(" ", '').replace("\n",'')  # OK!
        content = detail_html_xpath.xpath('//div[@id="img-content"]/div[2]/p/span/text()')
        print(title, detail_url)
        for i in content:
            print(i)

    def run(self):
        for url in self.get_url_list():
            html = self.get_html(url)
            for detail_url in self.get_detail_url(html):
                detail_html = self.get_html(detail_url)
                self.get_item(detail_html, detail_url)
                # break
            break


if __name__ == '__main__':
    wei_xin = WeiXin()
    wei_xin.run()
