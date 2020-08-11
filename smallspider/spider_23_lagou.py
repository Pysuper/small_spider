import urllib
from pprint import pprint
from urllib.parse import urlencode
from urllib.request import Request
import requests
from lxml import etree


class LaGou():
    def __init__(self):
        self.base_url = "https://www.lagou.com/jobs/positionAjax.json?"  # POST 请求
        self.key_world = {
            'city': '上海',
            'needAddtionalResult': 'false',
            'first': 'true',
            'pn': '1',
            'kd': '小游戏开发',
        }
        self.url = self.base_url + urlencode(self.key_world)
        self.header = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Length": "64",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "_ga=GA1.2.1987768877.1573108211; user_trace_token=20191107143011-0d0e0264-0128-11ea-a392-525400f775ce; LGUID=20191107143011-0d0e0503-0128-11ea-a392-525400f775ce; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216e448e818c520-0dc9d1fb48c821-1a201708-2073600-16e448e818dd7a%22%2C%22%24device_id%22%3A%2216e448e818c520-0dc9d1fb48c821-1a201708-2073600-16e448e818dd7a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; JSESSIONID=ABAAABAAAIAACBI485E73310732621FC24604852A4FBB5C; WEBTJ-ID=20191111161747-16e598a52cc5d9-0956b97928d5d6-14291003-2073600-16e598a52cd5c3; _gat=1; _gid=GA1.2.625500515.1573460268; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1573108212,1573460268; LGSID=20191111161748-bf3ed5f2-045b-11ea-a4a1-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; gate_login_token=090da3f9994e495598d0c34bb8595ce77de1be0cf940cba8becca8866ba2fb2a; LG_LOGIN_USER_ID=fa28120816c97ae6f745d6f9073da9163786ba301fe3f72b33605146d9491148; LG_HAS_LOGIN=1; _putrc=4C78B41F32F2D1AD123F89F2B170EADC; login=true; unick=%E9%83%91%E5%85%B4%E6%B6%9B; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=112; privacyPolicyPopup=false; index_location_city=%E4%B8%8A%E6%B5%B7; TG-TRACK-CODE=index_navigation; X_HTTP_TOKEN=2639be6cd687e8e466306437513eb38f16f526b443; LGRID=20191111161926-f9a2ef5a-045b-11ea-a4a1-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1573460367; SEARCH_ID=a5cc90f821124ceeb30bbe6c318285b9",
            "Host": "www.lagou.com",
            "Origin": "https://www.lagou.com",
            "Referer": "https://www.lagou.com/jobs/list_%E5%B0%8F%E6%B8%B8%E6%88%8F%E5%BC%80%E5%8F%91/p-city_3?&cl=false&fromSearch=true&labelWords=&suginput=",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
            "X-Anit-Forge-Code": "0",
            "X-Anit-Forge-Token": "None",
            "X-Requested-With": "XMLHttpRequest",
        }

    def get_html(self):
        # GET
        response = requests.post(url=self.base_url,data=self.key_world, headers=self.header)
        # response = requests.get(self.url, params=self.key_world, headers=self.header)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        return None

        # POST
        # data = urlencode(self.key_world).encode()
        # request = Request(url=self.url, data=data)
        # response = urllib.request.urlopen(request)
        # return response.read().decode()

    def parse_detail_href(self, html):
        print(html)
        # job_list = html["content"]["positionResult"]["result"]
        # for job_info in job_list:
        #     pprint(job_info)

    def run(self):
        html = self.get_html()
        self.parse_detail_href(html)


la_gou = LaGou()
la_gou.run()
