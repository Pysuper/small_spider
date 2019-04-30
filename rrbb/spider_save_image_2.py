import os
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

    href_list = []
    title_list = []
    for info in info_list:
        # print(info.a['href'],info.a['title'])
        href = info.a["href"]
        title = info.a["title"]
        href_list.append(href)
    return href_list


def parse_detail_info(detail_html):
    """处理详情页信息，下载图片"""
    html = BeautifulSoup(detail_html, 'lxml')
    info_list = html.find('div', id='playlist').find_all('img')
    # print(info_list)

    detail_info_list = []
    detail_title_list = []
    for info in info_list:
        # print(info)
        href = info['originalsrc']
        # print(href)
        title = info['title']
        detail_info_list.append(href)
        detail_title_list.append(title)
    return detail_info_list, detail_title_list


def save_image(image_href, title, head):
    """图片下载出现问题"""

    # print(title[:-2]+image_href[-6:],image_href)
    # 秀人网 第351期01.jpg https://tu.ttt669.com/girl/XiuRen/351/01.jpg
    name = image_href[-6:-3]

    try:
        if os.path.exists('./images1/%s' % title):

            # content = urlopen(image_href)
            # print(image_href)
            req = urllib.request.Request(url=image_href, headers=head)
            content = urllib.request.urlopen(req)
            with open('./images1/%s/%sjpg' % (title, name), 'wb') as f:
                f.write(content.read())
                print('%s----已保存' % (title[:-2] + image_href[-6:]))

        else:
            os.mkdir('./images1/%s' % title)

            req = urllib.request.Request(url=image_href, headers=head)
            content = urllib.request.urlopen(req)
            with open('./images1/%s/%sjpg' % (title, name), 'wb') as f:
                f.write(content.read())
                print('%s----已保存' % title[:-2] + image_href[-6:])
                print(image_href)
    except:
        print("%s--下载失败" % title[:-2] + image_href[-6:])
        print(image_href)


if __name__ == '__main__':
    for page in range(1, 170):
        url = 'https://www.97rrbb.com/meinv/list-all-insert_time-%d.html' % page

        # url = 'https://www.98rrbb.com/meinv/list-all.html'
        head = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}

        # 获取首页源代码
        text = get_html(url, head)

        # 获取每个详情页的URL
        href_list = get_detail_info(text)
        # print(href_list)
        for src in href_list:
            href = 'https://www.98rrbb.com' + src
            detail_html = get_html(href, head)
            # print(detail_html)
            detail_href_list, detail_title_list = parse_detail_info(detail_html)

            for title in detail_title_list:
                fina_title = title[:-1]
            for detail_href in detail_href_list:
                # save_image(detail_href, fina_title)

                save_thread = threading.Thread(target=save_image, args=(detail_href, fina_title, head))
                save_thread.setDaemon(True)
                save_thread.start()
