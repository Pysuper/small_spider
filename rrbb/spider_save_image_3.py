import os
import re
import time
import urllib
import requests
import threading
from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_html(url, headers):
    """获取网页链接"""
    response = requests.get(url, headers)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return response.text


def get_detail_info(detail_response):
    html = BeautifulSoup(detail_response, 'lxml')
    info_list = html.find('div', class_='hy-video-list').find_all('li')
    # print(info_list)
    for info in info_list:
        href = 'https://www.97rrbb.com' + info.find('a')['href']
        title = info.find('h5').text
    return href, title


def parse_imafes_info(response, title, headers):
    """处理详情页信息，下载图片"""
    # html = re.findall(r'<" originalsrc="(.*?)">',response,re.S)
    # print('123455646')
    # print(html)

    html = BeautifulSoup(response, 'lxml')
    info_list = html.find('div', id='playlist').find_all('img')
    # print(info_list)
    for info in info_list:
        # print(info)
        href = info['originalsrc']
        # print(href)
    return href


def save_image(src, header):
    name = title[5:] + '----' + src[-6:]
    # print(src)
    try:
        if os.path.exists('./images'):
            print(src)
            print(name)

            req = urllib.request.Request(url=src, headers=header)
            time.sleep(5)
            content = urllib.request.urlopen(req)
            demo = content.read()

            with open('./images/%s' % name, 'wb') as f:
                print('????')
                f.write(demo)
                print('%s----已保存' % src[-6:])
    except:
        print("%s--下载失败" % src)


if __name__ == '__main__':
    for page in range(1, 170):
        head = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        url = 'https://www.97rrbb.com/meinv/list-all-insert_time-%d.html' % page

        text = get_html(url, head)
        href, title = get_detail_info(text)
        # print(title, href)
        detail_text = get_html(href, head)
        # 获取并保存图片
        src = parse_imafes_info(detail_text, title, head)

        save_image(src, head)
#         # print(detail_text)
#         thread = threading.Thread(target=parse_save_images,args=((detail_text, title, head)))
#         thread.setDaemon(True)
#         thread.start()





# <img src="/static/style/v4/images/default_com.jpg" title="前海农迈">






