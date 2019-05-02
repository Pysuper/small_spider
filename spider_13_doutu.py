import os
import re
import requests
from bs4 import BeautifulSoup
from urllib import request


def parse_page(url, head):
    print(url)
    response = requests.get(url, headers=head)
    text = BeautifulSoup(response.text, 'lxml')
    image_info_list = text.find("div", class_="page-content text-center").find_all('a')
    for image_info in image_info_list:
        image_title = image_info.find("p").text

        # 使用正则表达式中的替换--替换掉不能用来命名的字符串--,./?
        img_title = re.sub(r"[\?！？、，./,!]", "_", image_title)

        image_href = image_info.find('img', class_="img-responsive lazy image_dta")["data-original"]

        # 将链接名按照一定的规则分割
        img_name = os.path.splitext(image_href)[1]
        request.urlretrieve(image_href, "./images/" + img_title + img_name)
        print(image_title + "----下载完成!")


def get_last(url, head):
    response = requests.get(url, headers=head)
    last_html = BeautifulSoup(response.text, 'lxml')
    page_num = last_html.find("ul", class_="pagination").find_all('li')
    last_page_num = page_num[-2].text
    return int(last_page_num)


def main():
    url = "http://www.doutula.com/photo/list/?page=1"
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    last_page_num = get_last(url, head)
    for num in range(1, last_page_num):
        url = "http://www.doutula.com/photo/list/?page=%d" % num
        # print(url)
        parse_page(url, head)
        # break   # 这里测试的时候,只需要执行一次就够了---可以使用 break 跳出循环


if __name__ == '__main__':
    main()
