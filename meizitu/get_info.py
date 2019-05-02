import os
import urllib.request
from bs4 import BeautifulSoup


def get_url_html(url):
    """
    获取当前页面所有组图的详细地址
    :param url: 要获取源码的 URL 链接
    :return: 网页源码
    """
    page = urllib.request.urlopen(url)
    response = page.read()
    html = response.decode('utf-8')
    return html


def parse_menu_url(menu_html):
    """
    只为--获取首页菜单中的标题和链接（每日更新）
    :param url_html: 链接首页的源代码
    :return: 标题链接的列表，标题名的列表
    """
    url_list_soup = BeautifulSoup(menu_html, 'lxml')
    url_soup = url_list_soup.find('ul', class_="menu").find_all('li')

    menu_url_list = []
    menu_title_list = []

    for url_soup_info in url_soup:
        title = url_soup_info.a['title']
        href = url_soup_info.a['href']
        menu_url_list.append(href)
        menu_title_list.append(title)
        # print(title,href)
    return menu_url_list, menu_title_list


def get_last_num(first_url):
    """
    获取该页面（组图列表页面）的最后一页的页数
    :param first_url: 组图页面URL
    :return: 最后一页的页数(int类型)
    """
    first_url_html = get_url_html(first_url)
    # print(first_url_html)
    first_url_soup = BeautifulSoup(first_url_html, 'lxml')
    find_last_page = first_url_soup.find('div', class_='nav-links').find_all('a')
    # print(find_last_page[-2].text)
    last_page_num = int(find_last_page[-2].text)
    return last_page_num


def get_detail_page(group_page_html):
    """
    获取当前页面中所有组图的进入链接
    :param one_html:要获取组图链接的页面
    :return:当前页面中所有组图的详情页链接
    """
    html = BeautifulSoup(group_page_html, 'lxml')
    soup_list = html.find('div', class_='postlist').find_all('li')

    for soup in soup_list:
        detail_href = soup.span.a['href']
        detail_title = soup.span.a.string
        yield detail_href, detail_title


def parse_detail_info(group_detail_html):
    """
    从组图的页面源码中,找到可以 拼接出所有图片的详细地址 的源链接
    :param group_detail_html: 组图的详情页源码
    :return: 这组图片的最大页数,查看每张图片时候的源链接（和数字拼接）
    """
    page_soup_html = BeautifulSoup(group_detail_html, 'lxml')
    finally_page_soup = page_soup_html.find('div', class_='pagenavi').find_all('a')
    finally_page_num = finally_page_soup[-2].string

    detail_info_soup = page_soup_html.find('div', class_='main-image').find('a')
    page_href_info = detail_info_soup['href']
    page_href = page_href_info[:-2]

    return finally_page_num, page_href


def ordinary_parse_images(first_url):
    """处理前面几个正常显示的页面"""
    last_num = int(get_last_num(first_url))

    for page in range(0, last_num):
        url = first_url + "page/%d/" % page
        group_page_html = get_url_html(url)

        for detail_href, detail_title in get_detail_page(group_page_html):
            yield detail_href, detail_title


def special_parse_every(first_url):
    """
    处理每日更新中的页面链接
    :param url: 每日更新的链接
    :return: 每日更新中的组图链接列表,和它的标题
    """
    html = get_url_html(first_url)
    html_soup = BeautifulSoup(html, 'lxml')
    arch_list = html_soup.find('div', class_="all").find_all('ul', class_="archives")

    for arch_soup in arch_list:
        image_info_list = arch_soup.find_all("a")
        for image_info in image_info_list:
            image_info_href = image_info["href"]
            image_info_title = image_info.string
            yield image_info_href, image_info_title


def get_show_info(one_html, file_name):
    """
    第六页和前面几页不一样,单独处理
    :param one_html: 第六页的网页链接
    :param file_name: 图片保存时的名称
    :return: 图片保存情况
    """
    html = BeautifulSoup(one_html, 'lxml')
    show_soup_list = html.find('div', class_='postlist').find('div', id='comments').find('ul').find_all('li')

    for show_images_href in show_soup_list:
        images_href = show_images_href.p.img["src"]
        images_title = images_href[-12:]

        req = urllib.request.Request(url=images_href)
        content = urllib.request.urlopen(req).read()
        if os.path.exists("%s/妹子自拍" % file_name):
            with open("%s/妹子自拍/%s" % (file_name, images_title), 'wb') as f:
                f.write(content)
                print('%s-----已保存' % images_href)
        else:
            print("正在创建文件夹-----")
            os.mkdir("%s/妹子自拍" % file_name)
            with open("%s/妹子自拍/%s" % (file_name, images_title), 'wb') as f:
                f.write(content)
                print('%s-----已保存' % images_href)


def get_menu_url(url):
    """
    通过一个url,根据用户的判断，找到目标网址
    :return: 菜单栏中的标题名和链接
    """
    print("=" * 10 + "欢迎来到妹子图片下载" + "=" * 10)
    print("~~~~~ 1-@-首   页 ~~~~~")
    print("~~~~~ 2-@-性感妹子 ~~~~~")
    print("~~~~~ 3-@-日本妹子 ~~~~~")
    print("~~~~~ 4-@-台湾妹子 ~~~~~")
    print("~~~~~ 5-@-清纯妹子 ~~~~~")
    print("~~~~~ 6-@-妹子自拍 ~~~~~")
    print("~~~~~ 7-@-每日更新 ~~~~~")
    print("=" * 10 + "欢迎来到妹子图片下载" + "=" * 10)
    menu_num = int(input("\n请选择要下载的图片："))
    menu_html = get_url_html(url)
    menu_url_list, menu_title_list = parse_menu_url(menu_html)

    return menu_url_list, menu_title_list, menu_num


def main(url, file_name):
    menu_url_list, menu_title_list, menu_num = get_menu_url(url)
    first_url = menu_url_list[menu_num - 1]
    menu_name = menu_title_list[menu_num - 1]

    while True:
        if menu_num in range(6):
            print("正在准备----------", first_url)
            for detail_href, detail_title in ordinary_parse_images(first_url):
                yield detail_href, detail_title, menu_name

        elif menu_num == 6:
            first_html_text = get_url_html(first_url)
            first_url_soup = BeautifulSoup(first_html_text, 'lxml')
            find_last_page = first_url_soup.find('div', class_='pagenavi-cm').find_all('a')
            last_page_num = int(find_last_page[-3].text)

            num = 0
            for num_page in range(last_page_num):
                every_href = "http://www.mzitu.com/zipai/comment-page-%d/#comments" % num_page
                one_html = get_url_html(every_href)
                get_show_info(one_html, file_name)
                num += 1

        elif menu_num == 7:
            for image_info_href, image_info_title in special_parse_every(first_url):
                yield image_info_href, image_info_title, menu_name

        else:
            print("您的输入有误,请重新输入：")
