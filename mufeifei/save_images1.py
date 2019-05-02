import threading
import time
import os
import urllib
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
    # page = urllib.request.urlopen(url,head)
    # response = page.read()
    # html = response.decode('utf-8')
    # print('qwew')
    # return html


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
        img_info_list.append(img_href)
    return img_info_list


def save_img(img_src,head,save_name,file_name):
    """通过图片详情页的链接,获得图片链接"""
    time.sleep(2)
    img_info_html = get_url_html(img_src,head)
    img_info_soup = BeautifulSoup(img_info_html, 'lxml')
    img_href = img_info_soup.find("div", id="content").a.img["src"]
    img_name = img_href[-13:]
    # print(img_name)
    content = urlopen(img_href).read()
    # print("+" * 50)

    try:
        if os.path.exists("%s" % save_name):    # 这是images
            if os.path.exists("%s/%s" % (save_name,file_name)): # 这是./images/人名字
                with open("%s/%s/%s" % (save_name,file_name,img_name), "wb") as f:
                    f.write(content)
                    print("%s----下载完成..." % img_name)
                    time.sleep(.2)
            else:
                os.mkdir("%s/%s" % (save_name,file_name))
                with open("%s/%s/%s" % (save_name,file_name,img_name), "wb") as f:
                    f.write(content)
                    print("%s----下载完成..." % img_name)
                    time.sleep(.2)
        else:
            if os.path.exists("%s/%s" % (save_name,file_name)): # 这是./images/人名字
                with open("%s/%s/%s" % (save_name,file_name,img_name), "wb") as f:
                    f.write(content)
                    print("%s----下载完成..." % img_name)
                    time.sleep(.2)
            else:
                os.mkdir("%s/%s" % (save_name,file_name))
                with open("%s/%s/%s" % (save_name,file_name,img_name), "wb") as f:
                    f.write(content)
                    print("%s----下载完成..." % img_name)
                    time.sleep(2)
    except:
        pass

def downloads(url_list,head,save_name,title_list):
    for title in title_list:
        file_name = title
    for url in url_list:
    # 获取首页的 HTML 文本,获取其中有用的链接
        html = get_url_html(url, head)
        first_title_list, first_href_list = parse_first_html(html)

        # print(first_title_list)

        # 组图连接
        for first_get_href in first_href_list:
            second_href_html = get_url_html(first_get_href, head)
            img_info_list = parse_second_html(second_href_html)

            # 图片链接
            for img_info in img_info_list:
                img_href = img_info["href"]
                try:
                    threading.Thread(target=save_img,args=(img_href,head,save_name,file_name)).start()
                    time.sleep(2)
                    # save_img(img_href,head,save_name,file_name)
                except:
                    continue