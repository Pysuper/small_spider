import requests
import threading
from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_one_html(url, headers):
    """获取首页源码"""
    response = requests.get(url, headers)
    response.encoding = 'gbk'
    if response.status_code == 200:
        return response.text
    print("访问出错，请重新连接！")


def get_detail_src(text):
    """获取原网页中详情页的链接"""
    html = BeautifulSoup(text, 'lxml')
    soup_list = html.find('div', class_='list').find_all('li')
    href_list = []
    for soup in soup_list:
        href = 'http://www.netbian.com' + soup.a['href']
        href_list.append(href)
    return href_list


def parse_detail(detail_text):
    """进一步获取详情页源码"""
    html = BeautifulSoup(detail_text, 'lxml')
    soup = html.find('div', class_='pic-down').find('a')
    href = "http://www.netbian.com" + soup['href']
    return href


def parse_finally(finally_html):
    """最后处理高清图片的URL链接"""
    html = BeautifulSoup(finally_html, 'lxml')
    soup = html.find('td', align="left").a
    return soup['title'], soup['href']


def save_image(title, href):
    """保存图片"""
    content = urlopen(href)
    with open('./images1/%s.jpg' % title, 'wb') as f:
        f.write(content.read())
        print("%s----图片下载完成！" % title)


if __name__ == '__main__':

    for num in range(1, 11):
        if num == 1:
            url = 'http://www.netbian.com/meinv/index.htm'
        else:
            url = 'http://www.netbian.com/meinv/index_%d.htm' % num
        head = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/69.0.3497.81 Chrome/69.0.3497.81 Safari/537.36"}
        text = get_one_html(url, head)
        src_list = get_detail_src(text)

        for src in src_list:
            try:
                detail_text = get_one_html(src, head)
                next_detail_url = parse_detail(detail_text)
                finally_html = get_one_html(next_detail_url, head)
                image_title, image_href = parse_finally(finally_html)
                image_thread = threading.Thread(target=save_image, args=(image_title, image_href))
                image_thread.setDaemon(True)
                image_thread.start()
            except:
                continue
