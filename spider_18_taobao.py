import requests


class TaoBao():
    def __init__(self):
        self.base_url = "https://s.taobao.com/search?q=macbookpro&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306"
        self.header = {
            # "Cookie":""
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }

    def get_url_list(self):
        return []

    def get_html(self, url):
        response = requests.get(url, self.header)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        return response.text

    def parse_html(self, html):
        print(html)

    def run(self):
        for url in self.get_url_list():
            html = self.get_html(url)
            self.parse_html(html)


if __name__ == '__main__':
    search = TaoBao()
    search.run()
