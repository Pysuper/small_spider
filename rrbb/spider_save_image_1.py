import os
import re
import time
import gevent
import requests
import threading
import urllib.request
import multiprocessing
from gevent import monkey
from urllib.request import *
from bs4 import BeautifulSoup

# monkey.patch_all()

# 打开链接，获取HTML
def get_one_page(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        return response.text
    except:
        print('无法访问！！！请检查链接地址')


def get_one_html(url):
    response = get_one_page(url)
    soup = BeautifulSoup(response, 'lxml')
    images_list = soup.find_all('li', class_='col-md-2 col-sm-3 col-xs-4')
    return images_list


def get_next_page(url):
    info_list = get_one_html(url)
    # 循环获取所有页面详情
    for photo_page in info_list:
        title = photo_page.find('a', class_='videopic lazy')['title']
        href = photo_page.find('a', class_='videopic lazy')['href']
        src = 'https://www.90rrbb.com' + href
        index_response = get_one_page(src)
        href = re.findall(r' <img src="/home/load.+?title="(.+?)" originalSrc="(.+?)">', index_response, re.S)
        # print(href)
        # 将列表中的数据取--URL,Name
        for href_info in href:
            finally_title = href_info[0]
            finally_href = href_info[1]

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            req = urllib.request.Request(url=finally_href, headers=headers)
            content = urllib.request.urlopen(req).read()
            with open('./images/%s.jpg' % href_info[1][-11:-4], 'wb') as f:
                f.write(content)
                print('%s------下载完成！' % href_info[1][-11:-4])
        print(finally_href)

def get_last_page():
    """
    获取当前访问页面的最后一页，转int类型
    :param url: 当前访问的URL地址
    :return: 当前页面的最后一页（int）
    """
    url = 'https://www.90rrbb.com/tupian/list-all-insert_time-1.html'
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    # 寻找最后一页的xpath,取得文本信息
    last_page = soup.find('ul', class_='cleafix').find('li', class_='visible-xs').get_text()
    return int(last_page[-3:])

def main():
    while True:
        # num = int(input('请输入：'))
        num = get_last_page()
        for page in range(1, num):
            url = 'https://www.90rrbb.com/tupian/list-all-insert_time-%d.html' % page
            get_next_page(url)

if __name__ == '__main__':
    # save_list = []
    # save_images = gevent.spawn(main)
    # save_list.append(save_images)
    # gevent.joinall(save_list)
    # threading.Thread(target=main).start()
    main()









