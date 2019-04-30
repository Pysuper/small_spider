import os
import re
import time

import requests
import urllib.request
from bs4 import BeautifulSoup
import multiprocessing
from urllib.request import *
import threading
import gevent
from gevent import monkey


monkey.patch_all()


def get_one_page(url,headers):
    """
    使用链接，获取当前页面的HTML文本
    :param url: 要访问的网页地址
    :return: 当前页面的HTML文本
    """
    response = requests.get(url,headers)
    response.encoding = 'utf-8'
    # if response.status_code == 200:
    return response.text
    # print('访问出错！')


def get_one_html(url,headers):
    """
    获取当前页面的信息列表
    :param url: 当前访问的页面地址
    :return: 当前页面的详请列表
    """
    response = get_one_page(url,headers)
    soup = BeautifulSoup(response, 'lxml')
    photo_list = soup.find_all('li', class_='col-md-2 col-sm-3 col-xs-4')
    return photo_list


def get_next_page(url,headers):
    """
    获取页面的详细信息，分析拼接详情页的URL，再调用获取HTML文本的方法，匹配获取的数据，并保存图片
    :param url: 最初访问的链接地址
    :param headers: 使用的浏览器信息
    :return: 下载是否完成
    """
    info_list = get_one_html(url,headers)
    # 循环获取所有页面详情
    for photo_page in info_list:
        title = photo_page.find('a', class_='videopic lazy')['title']
        href = photo_page.find('a', class_='videopic lazy')['href']
        # print(title,href)
        src = 'https://www.90rrbb.com' + href
        index_response = get_one_page(src,headers)
        # print(index_response)
        href = re.findall(r' <img src="/home/load.+?title="(.+?)" originalSrc="(.+?)">', index_response, re.S)

        # 将列表中的数据取--URL,Name
        for href_info in href:
            # finally_title = href_info[0]
            # finally_href = href_info[1]
            # print(href_info[1])

            request = urllib.request.Request(url=href_info[1]) # , headers=headers
            image_info = urllib.request.urlopen(request)
            content = image_info.read()

            # print(multiprocessing.current_process().pid)

            # 保存数据，没有文件夹，自动创建
            try:
                if os.path.exists('./images'):
                    # 因为很多图片的名称是一样的，这里取URL中的数字为图片名称
                    try:
                        with open('./images/%s.jpg' % href_info[1][-11:-4], 'wb') as f:
                            f.write(content)
                            # print('%s------下载完成!进程号----' % href_info[1][-11:-4], multiprocessing.current_process().pid)
                            print('%s------下载完成!协程号----%s' % (href_info[1][-11:-4],gevent.getcurrent()))
                            # time.sleep(0.2)
                    except:
                        continue
                else:
                    os.mkdir('./images')
                    with open('./images/%s.jpg' % href_info[1][-11:-4], 'wb') as f:
                        f.write(content)
                        print('%s------下载完成！' % href_info[1][-11:-4])
            except:
                print('保存错误，请检查存储地址...%s' + href_info[1])


def get_last_page(url):
    """
    获取当前访问页面的最后一页，转int类型
    :param url: 当前访问的URL地址
    :return: 当前页面的最后一页（int）
    """
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    # 寻找最后一页的xpath,取得文本信息
    last_page = soup.find('ul', class_='cleafix').find('li', class_='visible-xs').get_text()
    print(int(last_page[-3:]))


def main():
    """
    通过键盘输入，获得循环次数，拼接URL，调用解析下载方法，保存数据
    :return: 下载是否完成
    """
    # num = int(input('最多下载至多少页：'))
    # print('正在加载，请稍后...')
    num = 410
    time.sleep(1)
    # 循环拼接URL，并模拟浏览器访问
    for page in range(2, num + 1):
        url = 'https://www.90rrbb.com/tupian/list-all-insert_time-%d.html' % page
        print(url)
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        get_next_page(url,headers)


if __name__ == '__main__':
    main()
    # 创建进程池
    # pool = multiprocessing.Pool(6)
    # # 循环执行任务
    # for i in range(10):
    #     pool.apply_async(main)
    # pool.close()
    # pool.join()

    # 创建携程
    # gevent_list = []
    # images = gevent.spawn(main)
    # gevent_list.append(images)
    # gevent.joinall(gevent_list)

    # # 线程
    # for i in range(4):
    #
    #     threading.Thread(target=main).start()
