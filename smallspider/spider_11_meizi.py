import os
import urllib
import threading
from bs4 import BeautifulSoup
from urllib.request import urlopen
from multiprocessing import Pool

# 获取所有的url及headers,确定保存的目录
file_name = "./images"
head = {'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Referer': 'http://www.mzitu.com'}


def get_one_url(url):
    """获取当前页面所有组图的详细地址"""
    page = urllib.request.urlopen(url)
    response = page.read()
    html = response.decode('utf-8')
    return html


def get_detail_page(one_html):
    """获取组图中的所有地址"""
    html = BeautifulSoup(one_html, 'lxml')
    soup_list = html.find('div', class_='postlist').find_all('li')
    detail_href_list = []
    for soup in soup_list:
        detail_href = soup.span.a['href']
        detail_href_list.append(detail_href)
    return detail_href_list


def parse_detail_info(detail_href_html):
    """处理所有组图，获取每一套图片的详细地址"""
    page_soup_html = BeautifulSoup(detail_href_html, 'lxml')
    finally_page_soup = page_soup_html.find('div', class_='pagenavi').find_all('a')
    finally_page_num = finally_page_soup[-2].string
    detail_info_soup = page_soup_html.find('div', class_='main-image').find('a')
    page_href_info = detail_info_soup['href']
    page_href = page_href_info[:-2]
    return finally_page_num, page_href


def parse_image_info(image_html):
    image_soup = BeautifulSoup(image_html, 'lxml')
    image_soup.find('div', class_='main-image').find('p')
    child_file_name = image_soup.img['alt']
    image_detail_href = image_soup.img['src']
    image_name = image_detail_href[-6:]

    req = urllib.request.Request(url=image_detail_href, headers=head)
    content = urllib.request.urlopen(req).read()

    if os.path.exists(file_name + '/%s' % child_file_name):
        with open(file_name + '/%s/%s' % (child_file_name, image_name), 'wb') as f:
            f.write(content)
            print("%s%s----下载完成." % (child_file_name, image_name))
    else:
        os.mkdir(file_name + '/%s' % child_file_name)
        with open(file_name + '/%s/%s' % (child_file_name, image_name), 'wb') as f:
            f.write(content)
            print("%s%s----下载完成." % (child_file_name, image_name))


def main():
    # 获取所有的url
    for page in range(1, 193):
        url = "http://www.mzitu.com/page/%d/" % page
        one_html = get_one_url(url)

        # 获取当前网页中的所有组图地址
        detail_href_list = get_detail_page(one_html)
        for detail_src in detail_href_list:
            detail_href_html = get_one_url(detail_src)
            finally_page_num, page_href = parse_detail_info(detail_href_html)
            try:
                finally_page = int(finally_page_num)

                # 获取所欲图片地址
                for page_num in range(finally_page):
                    image_info = page_href + "/" + str(page_num)
                    image_html = get_one_url(image_info)

                    # 保存图片
                    save_thread = threading.Thread(target=parse_image_info, args=(image_html,))
                    save_thread.setDaemon(True)
                    save_thread.start()
            except:
                print("===========这组图片是直接显示的，没有详情URL===========")
                continue


if __name__ == '__main__':
    cpu_num = os.cpu_count()
    pool = Pool(cpu_num)
    for i in range(cpu_num):
        pool.apply_async(main)
    pool.close()
    pool.join()
