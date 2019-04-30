import re
import os
import urllib
import threading
from bs4 import BeautifulSoup
from multiprocessing import Pool
from urllib.request import urlopen

file_name = "C:\软件\Pycharm-Windows\Python文件\爬虫文件\images"
# file_name = "E:meizitu"
# head = {'X-Requested-With': 'XMLHttpRequest',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
#         'Referer': 'http://www.mzitu.com'}

head = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept - Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
        'Connection': 'Keep-Alive',
        'Host': 'zhannei.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}


def get_one_url(url):
    """获取当前页面所有组图的详细地址"""
    print(url)
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


def parse_image_info(image_html, menu_name):
    image_soup = BeautifulSoup(image_html, 'lxml')
    image_soup.find('div', class_='main-image').find('p')
    child_file_name = image_soup.img['alt']
    image_detail_href = image_soup.img['src']
    image_name = image_detail_href[-6:]

    req = urllib.request.Request(url=image_detail_href, headers=head)
    content = urllib.request.urlopen(req).read()

    # 拼接新的文件名，有？C:\软件\Pycharm-Windows\Python文件\爬虫文件\images\每日更新\幻想办公室激情极品女秘书俞夕梦等你来征服
    # print(child_file_name)
    chile_new_name = re.findall("\w+", child_file_name)[0] + re.findall("\w+", child_file_name)[1]
    # print(new_menu_name)

    # 判断主文件是否创建了
    if os.path.exists(file_name + r'\%s' % (menu_name)):
        # 判断子文件夹是否创建
        if os.path.exists(file_name + r'\%s\%s' % (menu_name, chile_new_name)):
            print(menu_name + '已创建')
            with open(file_name + r'\%s\%s' % (chile_new_name, image_name), 'wb') as f:
                f.write(content)
            print(chile_new_name, image_name)
            print("%s%s----下载完成." % (chile_new_name, image_name))

        else:
            # 如果子文件夹没有创建，就先创建子文件夹-下载图片
            os.mkdir(file_name + r'\%s\%s' % (menu_name, chile_new_name))

            with open(file_name + 'r\%s\%s' % (chile_new_name, image_name), 'wb') as f:
                f.write(content)

            print(chile_new_name, image_name)
            print("%s%s----下载完成." % (chile_new_name, image_name))

    else:
        # 没有创建主文件夹，就先创建主文件夹
        os.mkdir(file_name + r'\%s' % (menu_name))
        os.mkdir(file_name + r'\%s\%s' % (menu_name, chile_new_name))

        with open(file_name + r'\%s\%s' % (chile_new_name, image_name), 'wb') as f:
            f.write(content)

        print(chile_new_name, image_name)
        print("%s--%s----下载完成." % (chile_new_name, image_name))


def parse_first_url(url_html):
    """获取首页菜单中的几个链接"""
    url_list_soup = BeautifulSoup(url_html, 'lxml')
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
    """获取最后一页的页数"""
    first_url_html = get_one_url(first_url)
    # print(first_url_html)
    first_url_soup = BeautifulSoup(first_url_html, 'lxml')
    find_last_page = first_url_soup.find('div', class_='nav-links').find_all('a')
    # print(find_last_page[-2].text)
    last_page_num = find_last_page[-2].text
    return last_page_num


def main():
    url = 'http://www.mzitu.com'
    print(1)
    # get_last_num(url)

    url_html = get_one_url(url)
    # 获取首页中所有的标题地址,及标签名
    menu_url_list, menu_title_list = parse_first_url(url_html)

    # 获取每一个标签名
    for url_menu_name in menu_title_list:
        menu_name = url_menu_name

    # 获取所有的url
    for first_url in menu_url_list:
        try:
            # 获取最后一页的页数--193
            last_page_num = get_last_num(first_url)
            # print(last_page_num)
            for page in range(1, int(last_page_num)):

                # 获取当前页面下的所有链接--http://www.mzitu.com//page/1/
                detail_url = first_url + "page/%d/" % page
                # print(menu_name,detail_url)
                one_html = get_one_url(detail_url)

                # 获取当前网页中的所有组图地址
                detail_href_list = get_detail_page(one_html)
                for detail_src in detail_href_list:
                    detail_href_html = get_one_url(detail_src)
                    finally_page_num, page_href = parse_detail_info(detail_href_html)
                    try:
                        finally_page = int(finally_page_num)

                        # 获取所有图片地址
                        for page_num in range(finally_page):
                            image_info = page_href + "/" + str(page_num)
                            image_html = get_one_url(image_info)

                            # 保存图片
                            save_thread = threading.Thread(target=parse_image_info, args=(image_html, menu_name))
                            save_thread.setDaemon(True)
                            save_thread.start()
                    except:
                        print(set("===========这组图片是直接显示的，没有详情URL==========="))
                        continue
        except:
            print("===========访问错误,请重新启动===========")
            continue


#
if __name__ == '__main__':
    # 获取所有的url及headers, 确定保存的目录
    cpu_num = os.cpu_count()
    pool = Pool(cpu_num)
    for i in range(cpu_num):
        pool.apply_async(main)
    pool.close()
    pool.join()

main()
