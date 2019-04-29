from pprint import pprint

import requests

url = "https://docs.djangoproject.com/zh-hans/2.1/"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}


def get_html(url, headers):
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    if response.status_code == 200:
        return response.text
    return "无法获取当前页面"


html_text = get_html(url, headers)
pprint(html_text)
