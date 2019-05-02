import os
import urllib.request
from urllib.request import urlopen

import requests
import six.moves
import threading
import multiprocessing
from bs4 import BeautifulSoup


def get_url_html(url, head):
    """获取网页源码"""
    response = requests.get(url, head)
    response.encoding = "utf-8"
    if response.status_code == 200:
        return response.text
    return "无法访问..."


def parse_person_html(first_url_html):
    """
    获取一页的链接,找到页面中所有类图的标题和链接
    :param first_url_html: 总页数中的 一页链接
    :return: 当前页面中的所有链接和名称
    """
    person_detail_list = []
    group_title_list = []
    person_url_soup = BeautifulSoup(first_url_html, 'lxml')
    person_soup_list = person_url_soup.find('div', class_="topc5").find_all('div', class_="listbox")
    for person_soup in person_soup_list:
        person_detail_info = person_soup.a["href"]
        group_title = person_soup.span.text
        # print(person_detail_info)
        # print(group_title)
        person_detail_list.append(person_detail_info)
        group_title_list.append(group_title)
    return person_detail_list, group_title_list


def get_every_page(url):
    """返回首页中所有页数中的链接列表"""
    one_url_list = []
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    page_soup = soup.find('div', class_="text-c").find_all("a")
    last_page = int(page_soup[-2].text)
    for page_num in range(last_page):
        one_url = "http://www.cct58.com/mneinv/%d.html" % page_num
        one_url_list.append(one_url)
    return one_url_list


def get_every_person(url, head):
    person_mx27_list = []
    # 从首页中获取所有的人物链接
    first_url_html = get_url_html(url, head)
    person_detail_list, group_title_list = parse_person_html(first_url_html)
    # 得到每个人物写真页面的链接
    for person_mx27_detail in person_detail_list:
        person_mx27 = person_mx27_detail + "mx27/"
        person_mx27_list.append(person_mx27)
        # print(person_mx27)
    return person_mx27_list, group_title_list


def get_page_person():
    url = "http://www.cct58.com/mneinv/1.html"
    one_url_list = get_every_page(url)  # 获得每一页的链接
    for url in one_url_list:
        print(url)


def parse_first_html(html):
    """处理第一次访问到的网页源码"""
    first_title_list = []
    first_href_list = []
    first_url_soup = BeautifulSoup(html, 'lxml')
    first_soup_list = first_url_soup.find('div', class_="cn").find_all('a')
    for first_url_info in first_soup_list:
        # title = first_url_info.img["alt"]
        # href = first_url_info["href"]
        # print(title, href)
        first_title_list.append(first_url_info.img["alt"])
        first_href_list.append(first_url_info["href"])
    return first_title_list, first_href_list


def parse_second_html(second_href_html):
    """获得这个链接中有用的信息--详细页面的链接--原始图片--最后返回的是原始图片的详情页面链接"""
    img_info_list = []
    second_href_soup = BeautifulSoup(second_href_html, 'lxml')
    second_info_list = second_href_soup.find('div', class_="my-mx-top10").find_all("a")
    for img_href in second_info_list:
        img_info_list.append(img_href["href"])
    return img_info_list


def save_img(img_href,img_href_html,group_title,second_name):
    """通过图片详情页的链接,获得图片链接"""
    img_info_soup = BeautifulSoup(img_href_html, 'lxml')
    img_src = img_info_soup.find("div", id="content").a.img["src"]
    img_name = img_href[-8:-5]
    # print(group_title,second_name,img_name,img_href)
    content = urlopen(img_src).read()
    # req = urllib.request.Request(url=img_src, headers=head)
    # content = urllib.request.urlopen(req).read()

    try:
        if os.path.exists("./images/%s" % group_title):    # 这是images
            if os.path.exists("./images/%s/%s" % (group_title,second_name)): # 这是./images/人名字
                with open("./images/%s/%s/%s.jpg" % (group_title,second_name,img_name), "wb") as f:
                    f.write(content)
                    print("%s----下载完成..." % img_name,img_src)
                    # time.sleep(.2)
            else:
                os.mkdir("./images/%s/%s" % (group_title,second_name))
                with open("./images/%s/%s/%s.jpg" % (group_title,second_name,img_name), "wb") as f:
                    f.write(content)
                    print("%s----下载完成..." % img_name,img_src)
                    # time.sleep(.2)
        else:
            os.mkdir("./images/%s" % group_title)
            if os.path.exists("./images/%s/%s" % (group_title,second_name)): # 这是./images/人名字
                with open("./images/%s/%s/%s.jpg" % (group_title,second_name,img_name), "wb") as f:
                    f.write(content)
                    print("%s----下载完成..." % img_name,img_src)
                    # time.sleep(.2)
            else:
                os.mkdir("./images/%s/%s" % (group_title,second_name))
                with open("./images/%s/%s/%s.jpg" % (group_title,second_name,img_name), "wb") as f:
                    f.write(content)
                    print("%s----下载完成..." % img_name,img_src)
                    # time.sleep(2)
    except:
        pass


if __name__ == '__main__':
    url = "http://www.cct58.com/mneinv/1.html"
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}

    one_url_list = get_every_page(url)  # 获得每一页的链接
    for url in one_url_list:
        # print(url)
        person_mx27_list, group_title_list = get_every_person(url, head)  # 获取的是每一个标题中的链接

        for url_second,group_title in six.moves.zip(person_mx27_list, group_title_list):
            # print(group_title,url_second)
            html = get_url_html(url_second, head)
            first_title_list, first_href_list = parse_first_html(html)

            for second_name,first_get_href in six.moves.zip(first_title_list, first_href_list):
                # print(group_title,second_name,first_get_href)
                second_href_html = get_url_html(first_get_href, head)
                img_info_list = parse_second_html(second_href_html)

                # for img_href in img_info_list:
                #     img_href_html = get_url_html(img_href,head)    # 这个就是每一张图片所在的网页-是一个链接
                    # save_img(img_href,img_href_html,group_title,second_name)

                    # threading.Thread(target=save_img,args=(img_href,img_href_html,group_title,second_name)).start()
                pool = multiprocessing.Pool(os.cpu_count())

                for img_href in img_info_list:
                    img_href_html = get_url_html(img_href, head)
                    pool.apply_async(save_img,args=(img_href,img_href_html,group_title,second_name))
                pool.close()
