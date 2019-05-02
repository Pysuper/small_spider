import requests
from lxml import etree
from six.moves import zip


def get_url_html(url, head):
    """通过网页链接--获取当前页面的 HTML """
    response = requests.get(url, headers=head)
    response.encoding = "gbk"
    if response.status_code == 200:
        return response.text
    else:
        print("无法访问...")


def get_170_detail(html):
    """通过返回的源码,使用 xpath 获取到其中想要的信息"""
    info_list = []
    xpath_html = etree.HTML(html)
    title_list = xpath_html.xpath('//*[@id="header"]/div/div[3]/div[2]/div[1]/div[1]/div[2]/ul/a/text()')
    href_list = xpath_html.xpath('//*[@id="header"]/div/div[3]/div[2]/div[1]/div[1]/div[2]/ul/a/@href')
    for title, href in zip(title_list, href_list):
        href = "http://www.ygdy8.net" + href
        info_list.append((title, href))
    # print(info_list)
    return info_list


def get_new_detail(html):
    info_list = []
    xpath_html = etree.HTML(html)
    movie_2018 = xpath_html.xpath('//*[@class="title_all"]/p/em/a/@href')
    name_2018 = xpath_html.xpath('//*[@class="title_all"]/p/text()')
    for movie, name in zip(movie_2018, name_2018):
        movie = "http://www.ygdy8.net" + movie
        info_list.append((name, movie))
    return info_list


def parse_detail_info(href_html):
    """通过返回的详情页的链接列表,获取每个详情页中的信息"""
    # print(href_html)
    xpath_html = etree.HTML(href_html)
    content = xpath_html.xpath('//*[@id="Zoom"]/span/p[0]/text()')
    # print(content)
    for i in content:
        print(i)



if __name__ == '__main__':
    url = "http://www.ygdy8.net/index.html"
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    # proxy = {"http": "106.75.226.36:808"}
    # 获取当前页面的源码
    html = get_url_html(url, head)
    info_list = get_170_detail(html)[1:]
    # get_new_detail(html)
    for url in info_list:
        href = url[1]
        href_html = get_url_html(href,head)
        parse_detail_info(href_html)
        break