import multiprocessing
import time
import requests
import re
import gevent
from bs4 import BeautifulSoup

# url = 'https://www.90rrbb.com/xiazai/list-all.html'


def get_one_page(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return response.text
    else:

        print('访问出错！')


def get_next_page(url):
    print(url)
    html = get_one_page(url)
    soup = BeautifulSoup(html, 'lxml')
    info = soup.find_all('li', class_='col-md-2 col-sm-3 col-xs-4')
    for movie_info in info:
        title = movie_info.find('a', class_='videopic lazy')['title']
        href = movie_info.find('a', class_='videopic lazy')['href']
        src = 'https://www.90rrbb.com' + href
        # print(title,src)
        # href_index = get_next_page(src)
        html = get_one_page(src)
        # soup = BeautifulSoup(html,'lxml')
        # result = soup.find('table',class_='table')
        # print(result)
        try:
            movie_torrents = re.findall('<input type="text" data-clipboard-text="(.*?)" id="lin1k', html, re.S)
            movie_title = re.findall('<h3>(.+?)</h3>', html, re.S)
            # print(movie_title[0])
            text = movie_title[0]
            for movie_torrent in movie_torrents:
                href = movie_torrent[0]
                # torrent = movie_torrent[1]
                # print(movie_torrent)
                with open('./1.text','a') as f:
                    f.write('\n' + text)
                    f.write(movie_torrent)

            print('%s--已保存' % movie_title[0])
        except:
            continue


# def get_last_page(url):
#     """
#     获取当前访问页面的最后一页，转int类型
#     :param url: 当前访问的URL地址
#     :return: 当前页面的最后一页（int）
#     """
#     response = requests.get(url)
#     response.encoding = 'utf-8'
#     soup = BeautifulSoup(response.text, 'lxml')
#     # 寻找最后一页的xpath,取得文本信息
#     last_page = soup.find('ul', class_='cleafix').find('li', class_='visible-xs').get_text()
#     print(int(last_page[-3:]))


def main():


    num = int(input('最后下载到：'))
    time.sleep(1)
    if num <= 72:
        for page in range(18, num + 1):
            url = 'https://www.90rrbb.com/xiazai/list-all-insert_time-%s.html' % page
            get_next_page(url)
    elif num > 72:
        print('对不起，超出范围，请重新输入！')
    else:
        print('请正确输入！')


if __name__ == '__main__':
    run_list = []
    images = gevent.spawn(main)
    run_list.append(images)
    gevent.joinall(run_list)

    # 创建进程池
    # pool = multiprocessing.Pool(6)
    # # 循环执行任务
    # for i in range(10):
    #     pool.apply_async(main)
    #     print(multiprocessing.current_process().pid)
    # pool.close()
    # pool.join()