import json
import requests


class Epidemic(object):
    def __init__(self):
        self.cities = []
        self.url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'

    def get_html(self, url):
        requests.adapters.DEFAULT_RETRIES = 5
        response = requests.get(url, timeout=500)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        return None

    def parse_html(self, html):
        if html == None:
            return None
        print(html)
        # data = html.json()["data"]
        # items = json.loads(data)

    def run(self):
        html = self.get_html(self.url)
        self.parse_html(html)
