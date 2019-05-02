import os
import re
import urllib.request
import multiprocessing
from bs4 import BeautifulSoup


def get_url_html(url):
    """
    获取qq,联系方式,图片链接
    :param url: 网页链接
    :return: qq,联系方式,图片链接
    """
    page = urllib.request.urlopen(url)
    response = page.read()
    html = response.decode('gbk')

    qq = re.findall(r"""4">【(.*?)】：</font><font size="6"><u>(\d+)</u></font>""", html, re.S)
    boss = re.findall("""4">【经理电话】：(.*?)</font><u><font size="5">(\d+)</font></""", html, re.S)
    girl_image_list = re.findall(r""".*?.gif" zoomfile="(.*?)" file""", html, re.S)
    return html, qq, boss, girl_image_list


def parse_first_page(first_url_html):
    """
    从当前页面中，获取所有的访问链接
    :param first_url_html: 当前网页中的所有下一页链接
    :return: 所有链接的列表
    """
    second_url_soup = BeautifulSoup(first_url_html, 'lxml')
    second_info_soup = second_url_soup.find('div', id='wp').find_all('div', class_='pns')

    second_info_list = []
    for second_soup in second_info_soup:
        second_url_info = second_soup.find('a')['href']
        second_detail_inf0 = 'https://www.shlf.tw' + second_url_info
        second_info_list.append(second_detail_inf0)
    return second_info_list


def save_info(second_url_info):
    """
    下载网页信息
    :param second_url_info: 要下载的网页链接
    :return: 图片下载完成
    """
    html, qq, boss, girl_image_list = get_url_html(second_url_info)
    for girl_image_href in girl_image_list:
        file_name = second_url_info[-16:-9]
        image_name = girl_image_href[-6:]

        try:
            if os.path.exists("./image_info/%s" % file_name):
                content = urllib.request.urlopen(girl_image_href).read()
                with open("./image_info/%s/%s" % (file_name, image_name), 'wb') as f:
                    f.write(content)
                    print("%s-----已保存." % image_name)

            else:
                os.mkdir("./image_info/%s" % file_name)
                content = urllib.request.urlopen(girl_image_href).read()
                with open("./image_info/%s/%s" % (file_name, image_name), 'wb') as f:
                    f.write(content)
                    print("%s-----已保存." % image_name)
                with open("././image_info/%s/%s.txt" % (file_name, "info"), "wt") as e:
                    e.write('"%s""%s""%s"' % (qq, boss, second_url_info))
        except:
            continue


if __name__ == '__main__':
    url = "https://www.shlf.tw/thread-68704-1-1.html"
    html, qq, boss, girl_image_list = get_url_html(url)

    pool = multiprocessing.Pool(processes=10)
    second_url_list = parse_first_page(html)
    for second_url_info in second_url_list:
        pool.apply_async(save_info, args=(second_url_info,))
    pool.close()
    pool.join()
