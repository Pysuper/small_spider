import re
from urllib.parse import urlencode
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import requests
import json
from multiprocessing import Pool


class Toutiao():
    def __init__(self):
        self.headers = {
            "accept": "application/json, text/javascript",
            "accept-encoding": "gzip, deflate, br",
            "content-type": "application/x-www-form-urlencoded",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": " max-age=0",
            "cookie": "t_webid=6685485624336680461; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16a6bc064634cb-055e628ad4cd8e-1a201708-1fa400-16a6bc0646455b; CNZZDATA1259612802=570466005-1556584692-%7C1556584692; tt_webid=6685485624336680461; __tasessionId=130vsbor11556585931978; csrftoken=d239a88c1f430daf017c23b3cea8c8e4; s_v_web_id=592682568335e1091789ede49f0f50ce",
            "referer": "https://www.toutiao.com",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }

    def get_page_index(self):
        # data = {
        #     'offset': 0, # offset,
        #     'format': 'json',
        #     'keyword': "街拍", # keyword,
        #     'autoload': 'autoload',
        #     'count': 20,
        #     'cur_tab': 1,
        # }
        data = {
            "aid": 24,
            "app_name": "web_search",
            "offset": 20,
            "format": "json",
            "keyword": "街拍",
            "autoload": "true",
            "count": 20,
            "en_qc": 1,
            "cur_tab": 1,
            "from": "search_tab",
            "pd": "synthesis",
            "timestamp":"1556585982662"
        }
        # urlencode 可将字典对象转换为url内部请求的参数
        url = 'https://www.toutiao.com/api/search/content/?' + urlencode(data)
        response = requests.get(url, self.headers)
        response.encoding = response.apparent_encoding
        print(url, response.text)
        # try:
        #     if response.status_code == 200:
        #         return response.text
        #     return None
        # except RequestException:
        #     print('请求索引页出错')
        #     return None


    def parse_page_index(self, html):
        """
        这里没有写完
        """
        # html 原本是一串字符串，json.loads()--将html转换为对象
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')


    def get_page_detail(self, url):
        try:
            response = requests.get(url, self.headers)
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            print('请求索引页出错')
            return None


    def parse_page_detail(self, html, url):
        soup = BeautifulSoup(html, 'lxml')
        title = soup.select('title')
        images_patter = re.compile("gallery:(.*?) sibling", re.S)
        result = re.search(images_patter, html)
        print("ON")
        if result:
            data = json.loads(result.group(1))
            if data and 'sub_images' in data.keys():
                sub_images = data.get('sub_images')
                images = [item.get('url') for item in sub_images]
                return {
                    'title': title,
                    'url': url,
                    'images': images
                }


    def run(self):
        page_html = self.get_page_index()
        print(page_html)
        # for url in self.parse_page_index(page_html):
        #     if url == None:
        #         del url
        #     else:
        #         html = self.get_page_detail(url)
        #         if html:
        #             self.parse_page_detail(html, url)

toutiao = Toutiao()
toutiao.run()

# if __name__ == '__main__':
    # pool = Pool(10)
    # pool.apply_async(main)
    # pool.close()
    # pool.join()
    # main()
