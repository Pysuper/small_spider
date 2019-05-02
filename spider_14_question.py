import os
import urllib

import requests
from bs4 import  BeautifulSoup
from urllib.request import urlopen


def get_url_html(url):
    response = requests.get(url)
    response.encoding = "utf-8"
    if response.status_code == 200:

        return response.text
    return "无法访问..."

def get_last_page(html):
    last_html = BeautifulSoup(html,"lxml")
    last_soup_list = last_html.find('div',id="pages").find_all('a')
    return int(last_soup_list[-2].text)

def parse_detail_url(detail_url):
    img_href_list = []
    detail_url_html = get_url_html(detail_url)
    detail_soup = BeautifulSoup(detail_url_html,"lxml")
    detail_soup_list = detail_soup.find("div",class_="content").find_all("img")
    for img_info in detail_soup_list:
        img_href = img_info["src"]
        img_href_list.append(img_href)
    return img_href_list


def downloads(img_href_list):
    head = {'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Referer': 'http://www.mzitu.com'}


    for img_href in img_href_list:
        image_name = img_href[-5:]
        print(image_name,img_href)
        req = urllib.request.Request(url=img_href, headers=head)
        content = urllib.request.urlopen(req).read()

        if os.path.exists("./images"):
            with open("./images/%s" % image_name,"wb") as f:
                f.write(content)
                print("%s---下载完成!" % image_name)
        # else:
        #     os.mkdir("./images")
        #     print("文件夹创建完成...")
        #     with open("./images/%s" % image_name,"wb") as f:
        #         f.write(content)
        #         print("%s---下载完成!" % img_href)


if __name__ == '__main__':
    url = "https://www.meituri.com/a/23434/"
    # 获取首页的源码
    html = get_url_html(url)
    last_page_num = get_last_page(html)

    # 获取所有页的链接
    for page in range(1,last_page_num):
        if page== 1:
            detail_url = url
        else:
            detail_url = url + "%d.html" % page
        images_href_list = parse_detail_url(detail_url)

        downloads(images_href_list)