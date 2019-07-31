# from pprint import pprint
#
# import requests
#
# url = "https://docs.djangoproject.com/zh-hans/2.1/"
# headers = {
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
#
#
# def get_html(url, headers):
#     response = requests.get(url, headers=headers)
#     response.encoding = response.apparent_encoding
#     if response.status_code == 200:
#         return response.text
#     return "无法获取当前页面"
#
#
# html_text = get_html(url, headers)
# pprint(html_text)


# import re
# from urllib.parse import urlencode
# from requests.exceptions import RequestException
# from bs4 import BeautifulSoup
# import requests
# import json
# from multiprocessing import Pool
#
#
# headers = {
#     "accept": " text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "accept-encoding": " gzip, deflate, br",
#     "accept-language": " zh-CN,zh;q=0.9",
#     "cache-control": " max-age=0",
#     "cookie": " tt_webid=6593288429483263501; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=1656c41f30d113-03ed0919f04cfb-2711d3e-144000-1656c41f30e5c; tt_webid=6593288429483263501; csrftoken=ff39a448f9f14bca7156d2caa951c334; CNZZDATA1259612802=1962152454-1535114645-null%7C1535199910; __tasessionId=g5w8ipujt1535204022781",
#     "referer": " https://www.toutiao.com/",
#     "upgrade-insecure-requests": " 1",
#     "user-agent": " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.33 Safari/537.36"
# }
#
#
# def get_page_index(offset, keyword):
#     data = {
#         'offset': offset,
#         'format': 'json',
#         'keyword': keyword,
#         'autoload': 'autoload',
#         'count': 20,
#         'cur_tab': 1,
#     }
#
#     # urlencode 可将字典对象转换为url内部请求的参数
#     url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
#     response = requests.get(url, headers)
#     try:
#         if response.status_code == 200:
#             # print(response.text)
#             return response.text
#         return None
#     except RequestException:
#         print('请求索引页出错')
#         return None
#         # return
#
#
# def parse_page_index(html):
#     """
#     这里没有写完
#     """
#     # html 原本是一串字符串，json.loads()--将html转换为对象
#     data = json.loads(html)
#     if data and 'data' in data.keys():
#         for item in data.get('data'):
#             yield item.get('article_url')
#
#
# def get_page_detail(url):
#     try:
#         response = requests.get(url, headers)
#         if response.status_code == 200:
#             # print(response.text)
#             return response.text
#         return None
#     except RequestException:
#         print('请求索引页出错')
#         return None
#
#
# def parse_page_detail(html, url):
#     soup = BeautifulSoup(html, 'lxml')
#     # print(soup)
#     # print(html)
#     title = soup.select('title')
#     print(title)
#     images_patter = re.compile("gallery:(.*?) sibling", re.S)
#     result = re.search(images_patter, html)
#     if result:
#         data = json.loads(result.group(1))
#         if data and 'sub_images' in data.keys():
#             sub_images = data.get('sub_images')
#             images = [item.get('url') for item in sub_images]
#             return {
#                 'title': title,
#                 'url': url,
#                 'images': images
#             }
#
#
# def main():
#     html = get_page_index(1, '街拍')
#     # print(html)
#     for url in parse_page_index(html):
#         if url == None:
#             del url
#         else:
#             html = get_page_detail(url)
#             if html:
#                 parse_page_detail(html, url)
#
#
# if __name__ == '__main__':
#     # pool = Pool(10)
#     # pool.apply_async(main)
#     # pool.close()
#     # pool.join()
#     main()

"""
neihantu_test 保存图片
"""
import urllib
from urllib import request

image_num = "test_name"
image_url = "https://nhpic.77tcms.com/pic/2019-05-02/fzNBqlNKfzNBqlNK15316157fzNBqlNKfzNBqlNK.gif"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
# request.urlretrieve(image_url, './images/{}.gif'.format(image_num))
req = urllib.request.Request(url=image_url, headers=headers)
# urllib.request.urlopen(req).read()
with open('./images/1.gif', 'wb') as f:
    f.write(urllib.request.urlopen(req).read())