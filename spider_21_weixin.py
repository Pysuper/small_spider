from urllib.parse import urlencode
import pymysql
import requests
from requests.exceptions import ConnectionError
from lxml.etree import XMLSyntaxError
from pyquery import PyQuery as pq

PROXY_POOL_URL = "http://testabc.yuwoyg.com:8086/api/web/manage/proxy/get"
# KEYWORD = input("请输入查询关键字")
KEYWORD = "宿迁"

MAX_COUNT = 50
base_url = "https://weixin.sogou.com/weixin?"

headers = {
    "Cookie": "IPLOC=CN3201; SUID=F4E502702D18960A000000005CD97EDC; SUV=1557757660655178; SNUID=F7E1017404018CC6BC684ACD04E55E9A; ppinf=5|1557757918|1558967518|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTUlQUQlOTAlRTclQTUlQTV8Y3J0OjEwOjE1NTc3NTc5MTh8cmVmbmljazoxODolRTUlQUQlOTAlRTclQTUlQTV8dXNlcmlkOjQ0Om85dDJsdUUxMFhJVmR1Y3ByWXJWTmIxR0lYVTRAd2VpeGluLnNvaHUuY29tfA; pprdig=fSpW1OMisLokkmPJpKY6v35ea0bicNFnXD66pYIwo6N-E4xyXeW68Sx770aTGPMY528Gr8j3a5ehwGBJ6sLgkaEjyvf2tKUfauaRtVM9MuNwRQHPDlroXZBgElhIejRb63sxBY2TA57d0jG3t59eo9zVMlCL8d7lftJaZWiados; sgid=03-38531383-AVzZf952nPMcR1jjjzJBOKQ; ppmdig=1557796781000000b0094b5797dd51f169b50f76251ace0e; sct=2",
    "Host": "account.sogou.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}

proxy = None


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_html(url, count=1):
    print('Crawling', url)
    print('Trying Count', count)
    global proxy
    if count >= MAX_COUNT:
        print('Tried Too Many Counts')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # Need Proxy
            print('302')
            proxy = get_proxy()
            if proxy:
                print('Using Proxy', proxy)
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occurred', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)


def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html

def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')

def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def parse_detail(html):
    try:
        doc = pq(html)
        title = doc('.rich_media_title').text()  #rich_media_title
        content = doc('.rich_media_content').text()  #rich_media_content
        date = doc('.publish_time').text()
        publisher = doc('.js_name').text()
        return {
            'title': title,
            'content': content,
            'date': date,
            'publisher': publisher,
        }
    except XMLSyntaxError:
        return None


def save_to_mysql(data):
    pass


def main():
    get_html(base_url)


if __name__ == '__main__':
    main()

