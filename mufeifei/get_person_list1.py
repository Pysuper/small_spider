import requests
from bs4 import BeautifulSoup


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
    person_detail_title = []
    person_url_soup = BeautifulSoup(first_url_html, 'lxml')
    person_soup_list = person_url_soup.find('div', class_="topc5").find_all('div', class_="listbox")
    for person_soup in person_soup_list:
        # person_detail_info = person_soup.a["href"]
        # print(person_detail_info)
        person_detail_list.append(person_soup.a["href"])
        person_detail_title.append(person_soup.a.img["alt"])
    return person_detail_list,person_detail_title


def get_every_page(url):
    """返回首页中所有页数中的链接列表"""
    one_url_list = []
    html = requests.get(url).text
    soup = BeautifulSoup(html,'lxml')
    page_soup = soup.find('div',class_="text-c").find_all("a")
    last_page = int(page_soup[-2].text)
    for page_num in range(last_page):
        one_url = "http://www.cct58.com/mneinv/%d.html" % page_num
        one_url_list.append(one_url)
    return one_url_list


def get_every_person(url,head):
    person_mx27_list = []
    # 从首页中获取所有的人物链接
    first_url_html = get_url_html(url, head)
    person_detail_list,person_detail_title = parse_person_html(first_url_html)
    # 得到每个人物写真页面的链接
    # for person_title in person_detail_title:
    #     title = person_title
    for person_mx27_detail in person_detail_list:
        person_mx27 = person_mx27_detail + "mx27/"
        person_mx27_list.append(person_mx27)
        # print("*"*40)
        # print(person_mx27)
    return person_mx27_list,person_detail_title




