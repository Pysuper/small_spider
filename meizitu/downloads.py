import os
import threading
import urllib.request
from bs4 import BeautifulSoup
from mzitu_spider.get_info import get_url_html, parse_detail_info


def save_image(image_save_href, child_save_name, image_save_name, file_name, menu_name):
    """
    下载图片
    :param image_detail_href: 图片的下载地址
    :param menu_name: 菜单标题名
    :param child_file_name: 组图标题名
    :param image_name: 图片序号
    :return: 下载情况
    """
    head = {'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Referer': 'http://www.mzitu.com'}

    req = urllib.request.Request(url=image_save_href, headers=head)
    content = urllib.request.urlopen(req).read()

    child_name = child_save_name

    # 判断主文件是否创建了
    if os.path.exists(file_name + '/%s' % (menu_name)):
        # 判断子文件夹是否创建
        if os.path.exists(file_name + '/%s/%s' % (menu_name, child_name)):
            # 如果图片已下载，返回
            if os.path.exists(file_name + '/%s/%s/%s' % (menu_name, child_name, image_save_name)):
                return
            with open(file_name + '/%s/%s/%s' % (menu_name, child_name, image_save_name), 'wb') as f:
                f.write(content)
                print("%s%s----下载完成." % (child_name, image_save_name))

        else:
            # 如果子文件夹没有创建，就先创建子文件夹-下载图片
            print("正在创建文件夹-----", file_name + '/%s/%s' % (menu_name, child_name))
            os.mkdir(file_name + '/%s/%s' % (menu_name, child_name))
            with open(file_name + '/%s/%s/%s' % (menu_name, child_name, image_save_name), 'wb') as f:
                f.write(content)
                print("%s%s----下载完成." % (child_name, image_save_name))

    else:
        # 没有创建主文件夹，就先创建主文件夹
        print("正在创建文件夹-----", file_name + '/%s' % (menu_name))
        print("正在创建文件夹-----", file_name + '/%s/%s' % (menu_name, child_name))
        os.mkdir(file_name + '/%s' % (menu_name))
        os.mkdir(file_name + '/%s/%s' % (menu_name, child_name))

        with open(file_name + '/%s/%s/%s' % (menu_name, child_name, image_save_name), 'wb') as f:
            f.write(content)
            print("%s--%s----下载完成." % (child_name, image_save_name))


def images_downloads(image_group, file_name, menu_name):
    """
    获取到组图链接列表，提取单张图片地址
    :param finally_page_num: 这个组图中图片的最后页数
    :param page_href:组图的链接
    :return:
    """
    detail_href_html = get_url_html(image_group)
    finally_page_num, page_href = parse_detail_info(detail_href_html)

    for page_num in range(0, int(finally_page_num)):
        try:
            image_info = page_href + "/" + str(page_num)
            image_html = get_url_html(image_info)
            image_save_href, child_save_name, image_save_name = parse_image_info(image_html)

            threading.Thread(target=save_image,args=(image_save_href, child_save_name, image_save_name, file_name, menu_name)).start()

        except:
            print("==========%s%s 未获取到信息==========" % (image_save_href, image_save_name))
            continue


def parse_image_info(image_html):
    """
    从单张图片的访问地址中拿到其下载信息
    :param image_html: 图片的访问地址
    :param menu_name: 每组图片的标题
    :return: 单张图片的下载地址,下载后的图片名称
    """
    image_soup = BeautifulSoup(image_html, 'lxml')
    image_soup.find('div', class_='main-image').find('p')
    child_file_name = image_soup.img['alt']
    image_detail_href = image_soup.img['src']
    image_save_name = image_detail_href[-6:]
    return image_detail_href, child_file_name, image_save_name

