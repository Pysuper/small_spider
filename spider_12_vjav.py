import csv
import threading
import requests
import urllib.parse
from lxml import etree


def get_url():
    # 获取网页源码
    # url_list = ["https://www.vjav.com/search/%20%20%20Yoshizawa%20Akiho%20/2/"]
    for i in range(1,13):
        url = "https://www.vjav.com/search/%20%20%20Yoshizawa%20Akiho%20/" + "%d/" % i
        yield url

def parse_utl_html():
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    proxy = {'http': '127.0.0.1:1080'}
    html_text = []
    for url in get_url():
        print(url)
        response = requests.get(url,headers=head,proxies=proxy)
        if response.status_code ==200:
            yield response.text
            # html_text.append(response.text)
            # return html_text
        else:
            print("无法访问...")
        # break

def parse_detail_href():
    for text in parse_utl_html():
        xpath_html = etree.HTML(text)
        movie_list = xpath_html.xpath('//*[@id="list_videos_videos_list_search_result_items"]/div/a/@href')
        title_list = xpath_html.xpath('//*[@id="list_videos_videos_list_search_result_items"]/div/a/strong/text()')

        for title,href in zip(title_list,movie_list):
        # for href in movie_list:
            title = "".join(title).strip()[19:-4]
            # jzmb_info = {"title":title[20:-5],"url":href}
            yield title,href


def save_info():
    # for movie_info in parse_detail_href():
        # headers = ['title', 'url']
        # with open('./jzmb.csv','a') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(headers)
        #     writer.writerow(movie_info)

    for href,movie_info in parse_detail_href():
        with open("movie_info.text",'a') as f:
            f.write(href + "          ")
            f.write(movie_info + '\n')
            print(movie_info)
            # break

if __name__ == '__main__':
    """使用VPN访问国外网页,保存网站信息"""
    threading.Thread(target=save_info).start()


