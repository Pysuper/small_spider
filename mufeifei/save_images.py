import threading
import time
import os
from multiprocessing import Pool
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_url_html(url, head):
    """获取网页 HTML 文本"""
    response = requests.get(url, head)
    response.encoding = "encoding"
    if response.status_code == 200:
        return response.text


def parse_first_html(html):
    """处理第一次访问到的网页源码"""
    first_title_list = []
    first_href_list = []
    first_url_soup = BeautifulSoup(html, 'lxml')
    first_soup_list = first_url_soup.find('div', class_="cn").find_all('a')
    for first_url_info in first_soup_list:
        # title = first_url_info.img["alt"]
        # href = first_url_info["href"]
        first_title_list.append(first_url_info.img["alt"])
        first_href_list.append(first_url_info["href"])
    return first_title_list, first_href_list


def parse_second_html(second_href_html):
    """获得这个链接中有用的信息--详细页面的链接--原始图片--最后返回的是原始图片的详情页面链接"""
    img_info_list = []
    second_href_soup = BeautifulSoup(second_href_html, 'lxml')
    second_info_list = second_href_soup.find('div', class_="my-mx-top10").find_all("a")
    for img_href in second_info_list:
        print(img_href)
        img_info_list.append(img_href)
    return img_info_list


def save_img(img_src,head):
    """通过图片详情页的链接,获得图片链接"""
    img_info_html = get_url_html(img_src,head)
    img_info_soup = BeautifulSoup(img_info_html, 'lxml')
    img_href = img_info_soup.find("div", id="content").a.img["src"]
    img_name = img_href[-13:]
    # print(img_name)
    content = urlopen(img_href).read()
    print("+" * 50)
    with open("./images1/%s" % img_name, "wb") as f:
        f.write(content)
        print("%s----下载完成..." % img_name)
        time.sleep(.2)


def downloads(url_list,head):
    img_href_list = []
    for url in url_list:
        print(url)
    # 获取首页的 HTML 文本,获取其中有用的链接
        html = get_url_html(url, head)
        first_title_list, first_href_list = parse_first_html(html)
        for first_get_href in first_href_list:
            second_href_html = get_url_html(first_get_href, head)
            img_info_list = parse_second_html(second_href_html)
            for img_info in img_info_list:
                img_href = img_info["href"]
                img_href_list.append(img_href)
                # print("=" * 60)
                print(img_href)
    return img_href_list


# if __name__ == '__main__':
#     cpu_num = os.cpu_count()
#     pool =Pool(cpu_num)
#     img_href_list = main()
#     for img_info in img_href_list:
#         threading.Thread(target=save_img,args=(img_info,)).start()
#     pool.close()
#     pool.join()





















