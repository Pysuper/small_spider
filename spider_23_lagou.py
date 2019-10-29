from pprint import pprint

import requests
from lxml import etree


class LaGou():
    def __init__(self):
        self.url = "https://www.lagou.com/jobs/positionAjax.json?px=new&city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false"
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'Connection': 'keep-alive',
            'Cookie': '_ga=GA1.2.759756292.1572002144; _gid=GA1.2.1024774356.1572002144; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1572002144; user_trace_token=20191025191854-3af2cb8b-f719-11e9-a08c-525400f775ce; PRE_UTM=; PRE_HOST=cn.bing.com; PRE_SITE=https%3A%2F%2Fcn.bing.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGUID=20191025191854-3af2ce76-f719-11e9-a08c-525400f775ce; LGSID=20191025191854-3af2ccf6-f719-11e9-a08c-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; _gat=1; LGRID=20191025192516-1eb14395-f71a-11e9-a607-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1572002526; X_HTTP_TOKEN=7f3a7ebf1bb8dfc4987200275129b8d1ec41735636'
        }

    def get_html(self):
        response = requests.get(url=self.url, headers=self.header)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        return None

    def parse_detail_href(self, html):
        print(html)
        job_list = html["content"]["positionResult"]["result"]
        for job_info in job_list:
            pprint(job_info)

    def run(self):
        html = self.get_html()
        self.parse_detail_href(html)


la_gou = LaGou()
la_gou.run()
