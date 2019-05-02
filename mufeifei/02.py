import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_url_html(url, head):
    """获取网页源码"""
    response = requests.get(url, head)
    response.encoding = "utf-8"
    if response.status_code == 200:
        return response.text
    return "无法访问..."


def parse_person_html(first_url_html):
    """获取人物的详情页面"""
    person_detail_list = []
    person_url_soup = BeautifulSoup(first_url_html, 'lxml')
    person_soup_list = person_url_soup.find('div', class_="topc5").find_all('div', class_="listbox")
    for person_soup in person_soup_list:
        # person_detail_info = person_soup.a["href"]
        # print(person_detail_info)
        person_detail_list.append(person_soup.a["href"])
    return person_detail_list


if __name__ == '__main__':
    url = "http://www.cct58.com/mneinv/"
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}

    # 从首页中获取所有的人物链接
    first_url_html = get_url_html(url, head)
    person_detail_list = parse_person_html(first_url_html)
    # 得到每个人物写真页面的链接
    for person_mx27_detail in person_detail_list:
        person_mx27 = person_mx27_detail + "mx27/"
        print(person_mx27)