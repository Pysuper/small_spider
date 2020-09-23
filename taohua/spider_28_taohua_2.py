# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/11 下午8:05
# @Author  : Zheng Xingtao
# @File    : spider_28_taohua.py

import os
import json
import requests
from lxml import etree
from queue import Queue
from pprint import pprint
from threading import Thread
from concurrent.futures.thread import ThreadPoolExecutor


"""
['http://thzd.cc/forum.php/forum-181-1.html',
 'http://thzd.cc/forum.php/forum-182-1.html',
 'http://thzd.cc/forum.php/forum-69-1.html',
 'http://thzd.cc/forum.php/forum-177-1.html',
 'http://thzd.cc/forum.php/forum-172-1.html',
 'http://thzd.cc/forum.phphttp://hsck8.com/',
 'http://thzd.cc/forum.php/forum-152-1.html',
 'http://thzd.cc/forum.php/forum-196-1.html',
 'http://thzd.cc/forum.php/forum-73-1.html',
 'http://thzd.cc/forum.php/forum-199-1.html',
 'http://thzd.cc/forum.php/forum.php?gid=190',
 'http://thzd.cc/forum.php/forum.php?gid=61']
 """


class TaoHua(object):
    """获取最新疫情数据"""

    def __init__(self):
        self.cities = []
        self.url = 'http://thzd.cc/forum.php'

    def get_html(self, url):
        """
        获取网页中的数据
        :param url: 网页URL
        :return: 当前网页源码
        """
        response = requests.get(url, timeout=500)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        return None

    def parse_html(self, html):
        """
        返回JSON数据类型的data数据
        :param html: 当前网页源码
        :return: 网页中的JSON数据信息
        """
        if html == None:
            return None
        selector = etree.HTML(html)

        """页面标题"""
        infos_1_titles = selector.xpath("//div[@id='levnav']/ul[1]/li/a/text()")
        infos_1_urls = selector.xpath("//div[@id='levnav']/ul[1]/li/a/@href")

        infos_2_titles = selector.xpath("//div[@id='levnav']/ul[2]/li/a/text()")
        infos_2_urls = selector.xpath("//div[@id='levnav']/ul[2]/li/a/@href")

        title_urls = []
        for infos_1_title, infos_1_url in zip(infos_1_titles, infos_1_urls):
            info_url_dict = {}
            info_url_dict["title"] = infos_1_title
            info_url_dict["url"] = self.url + infos_1_url

            # print(info_url_dict)
            title_urls.append(info_url_dict)

        for infos_2_title, infos_2_url in zip(infos_2_titles, infos_2_urls):
            info_url_dict = {}
            info_url_dict["title"] = infos_2_title
            info_url_dict["url"] = self.url + infos_2_url

            # print(info_url_dict)
            title_urls.append(info_url_dict)

        # pprint(title_urls)

        """首发内容"""
        shou_fa_titles = selector.xpath("//div[@class='bm_c']//tr//td/h2/a/text()")
        shou_fa_urls = selector.xpath("//div[@class='bm_c']//tr//td/h2/a/@href")

        shoufa_url_list = []
        for shou_fa_title, shou_fa_url in zip(shou_fa_titles, shou_fa_urls):
            shoufa_url_dict = {}
            shoufa_url_dict["title"] = shou_fa_title
            shoufa_url_dict["url"] = self.url + shou_fa_url

            # print(shoufa_url_dict)
            shoufa_url_list.append(shoufa_url_dict)

        """各个细分类"""

        more_titles = selector.xpath("//div[@class='bm_c']//tr//dt/a/text()")
        more_urls = selector.xpath("//div[@class='bm_c']//tr//dt/a/@href")

        more_url_list = []
        for more_title, more_url in zip(more_titles, more_urls):
            more_url_dict = {}
            more_url_dict["title"] = more_title
            more_url_dict["url"] = self.url + more_url
            # print(more_url_dict)

            more_url_list.append(more_url_dict)

        return title_urls + shoufa_url_list + more_url_list

    def parse_data(self, data):
        """
        将网页中的数据，存储到Dict中
        :param data: JSON格式的网页数据
        :return: 将数据保存到全局变量 self.cities 中
        """
        pass

    def save_to_file(self, item):
        """
        将获取到的数据保存到文件中
        :param item: Dict组成的List数据
        :return: 数据保存状态
        """
        pass

    def save_to_sql(self, item):
        """
        将获取到的数据保存到SQL中：MySQL、Redis、MongoDB...
        :param item: Dict组成的List数据
        :return: 数据保存到数据中的保存状态
        """
        pass

    def run(self):
        html = self.get_html(self.url)
        url_info_list = self.parse_html(html)
        return url_info_list


class ForOne(object):
    def __init__(self, base_url, page_num):
        self.url = "http://thzd.cc/"
        # self.base_url = "http://thzd.cc/forum-181-{}.html"
        self.base_url = base_url
        self.page_num = page_num

    def url_list(self):
        """
        处理当前的url_list
        :return: 返回当前url的列表
        """
        for page in range(1, self.page_num):
            yield self.base_url.format(page)

    def get_html(self, url):
        """
        获取网页中的数据
        :param url: 网页URL
        :return: 当前网页源码
        """
        response = requests.get(url, timeout=500)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        return None

    def parse_html(self, html):
        """
        返回JSON数据类型的data数据
        :param html: 当前网页源码
        :return: 网页中的JSON数据信息
        """
        if html == None:
            return None

        selector = etree.HTML(html)

        """标题页"""
        title_list = []
        info_1_titles = selector.xpath(
            "//table[@id='threadlisttableid']/tbody/tr/th/a[@onclick='atarget(this)']/text()")
        info_1_urls = selector.xpath("//table[@id='threadlisttableid']/tbody/tr/th/a[@onclick='atarget(this)']/@href")
        for info_1_title, info_1_url in zip(info_1_titles, info_1_urls):
            title_dict = {}
            title_dict["title"] = info_1_title
            title_dict["url"] = self.url + info_1_url
            title_list.append(title_dict)
        return title_list

    def run(self):
        for url in self.url_list():
            print(url)
            html = self.get_html(url)
            title_url_list = self.parse_html(html)
            yield title_url_list


class ForDetail(object):
    def __init__(self):
        self.url = "http://thzd.cc/"

    def get_html(self, url):
        """
        获取网页中的数据
        :param url: 网页URL
        :return: 当前网页源码
        """
        response = requests.get(url, timeout=500)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        return None

    def parse_html(self, html):
        """
        返回JSON数据类型的data数据
        :param html: 当前网页源码
        :return: 网页中的JSON数据信息
        """
        if html == None:
            return None
        selector = etree.HTML(html)

        """详情页"""
        detail_url = selector.xpath("//p[@class='attnm']/a/@href")[0]
        return self.url + detail_url

    def parse_resutle(self, html):
        if html == None:
            return None
        # print(html)
        selector = etree.HTML(html)

        """详情页"""
        result_url = selector.xpath("""//a[@onclick="hideWindow('imc_attachad')"]/@href""")[0]
        resutl_name = selector.xpath("//div[@class='f_c']//tbody/tr[1]/td/div/text()")[0]

        return resutl_name, result_url
        # return "asdasd"

    def download(self, name, url):
        get = requests.get(url)
        SAVE_PATH = '/home/zheng/Downloads/taohua/' + name

        if os.path.isfile(SAVE_PATH):
            return
        with open(SAVE_PATH, 'wb') as download:
            download.write(get.content)

    def run(self, save_name, download_page_url):
        html = self.get_html(url=download_page_url)
        detail_url = self.parse_html(html)
        detail_html = self.get_html(detail_url)
        resutl_name, restult_url = self.parse_resutle(detail_html)
        # print(restult_url)

        # 这里下载的时候使用多任务处理
        self.download(save_name, restult_url)


def run(title_info):
    try:
        ForDetail().run(title_info["title"].strip(), title_info["url"])
        print("下载完成:", title_info["url"], title_info["title"])
    except:
        pass


# 创建线程池-Queue队列
def queue_pool():
    queue = Queue()
    # base_url = "http://thzd.cc/forum-181-{}.html"
    base_url = "http://thzd.cc/forum-177-{}.html"
    page_num = 1000
    try:
        for title_url_info in ForOne(base_url, page_num).run():
            # pprint(title_url_info)

            for title_info in title_url_info:
                if "日更新" not in title_info["title"]:
                    # ForDetail().run(title_info["title"].strip(), title_info["url"])
                    save_thread = Thread(target=run, args=(title_info,))
                    save_thread.daemon = True  # 随主线程退出而退出
                    save_thread.start()
        queue.join()
    except:
        pass


if __name__ == '__main__':
    queue_pool()

"""
单线程
base_url = "http://thzd.cc/forum-181-{}.html"
page_num = 254
for title_url_info in ForOne(base_url, page_num).run():
    # pprint(title_url_info)

    for title_info in title_url_info:

        if "日更新" not in title_info["title"]:
            try:
                ForDetail().run(title_info["title"].strip(), title_info["url"])
                print("下载完成:", title_info["url"], title_info["title"])
            except:
                continue
"""

category_info = {
    {'url': 'http://thzd.cc/forum.php/forum-181-1.html', 'title': '欧美无码'},
    {'url': 'http://thzd.cc/forum.php/forum-182-1.html', 'title': '国内原创'},
    {'url': 'http://thzd.cc/forum.php/forum-69-1.html', 'title': '原创合集'},
    {'url': 'http://thzd.cc/forum.php/forum-177-1.html', 'title': '手机视频'},
    {'url': 'http://thzd.cc/forum.php/forum-152-1.html', 'title': '成人小说'},
    {'url': 'http://thzd.cc/forum.php/forum-196-1.html', 'title': '热门电影'},
    {'url': 'http://thzd.cc/forum.php/forum-73-1.html', 'title': '成人动漫'},
    {'url': 'http://thzd.cc/forum.php/forum-199-1.html', 'title': '影片归档'},
    {'url': 'http://thzd.cc/forum.php/forum.php?gid=190', 'title': '在线视频'},
    {'url': 'http://thzd.cc/forum.phpforum-181-1.html', 'title': '亚洲無碼原創'},
    {'url': 'http://thzd.cc/forum.phpforum-220-1.html', 'title': '亚洲有碼原創'},
    {'url': 'http://thzd.cc/forum.phpforum-182-1.html', 'title': '欧美無碼'},
    {'url': 'http://thzd.cc/forum.phpforum-69-1.html', 'title': '国内原创(BT)'},
    {'url': 'http://thzd.cc/forum.phpforum-203-1.html', 'title': '各类合集资源'},
    {'url': 'http://thzd.cc/forum.phpforum-177-1.html', 'title': '蓝光高清原盘'},
    {'url': 'http://thzd.cc/forum.phpforum-325-1.html', 'title': '在线播片'},
    {'url': 'http://thzd.cc/forum.phpforum-265-1.html', 'title': '115网盘礼包分享'},
    {'url': 'http://thzd.cc/forum.phpforum-47-1.html', 'title': '站务'},
    {'url': 'http://thzd.cc/forum.phpforum-246-1.html', 'title': '赞助会员申请'},
    {'url': 'http://thzd.cc/forum.phpforum-118-1.html', 'title': '建議&BUG提交'},
    {'url': 'http://thzd.cc/forum.phpforum-42-1.html', 'title': '性爱自拍'},
    {'url': 'http://thzd.cc/forum.phpforum-56-1.html', 'title': '人體藝術'},
    {'url': 'http://thzd.cc/forum.phpforum-57-1.html', 'title': '街頭抓拍'},
    {'url': 'http://thzd.cc/forum.phpforum-221-1.html', 'title': '欧美图片'},
    {'url': 'http://thzd.cc/forum.phpforum-239-1.html', 'title': 'AV美图'},
    {'url': 'http://thzd.cc/forum.phpforum-200-1.html', 'title': '動態圖區'},
    {'url': 'http://thzd.cc/forum.phpforum-307-1.html', 'title': '漫畫十八禁'},
    {'url': 'http://thzd.cc/forum.phpforum-79-1.html', 'title': '桃花原創發片預告'},
    {'url': 'http://thzd.cc/forum.phpforum-172-1.html', 'title': '桃花原創合集（BT）'},
    {'url': 'http://thzd.cc/forum.phpforum-73-1.html', 'title': '三级*未分级(BT)'},
    {'url': 'http://thzd.cc/forum.phpforum-137-1.html', 'title': '美圖寫真(BT)'},
    {'url': 'http://thzd.cc/forum.phpforum-196-1.html', 'title': '热门电影(BT)'},
    {'url': 'http://thzd.cc/forum.phpforum-45-1.html', 'title': '网友求片(BT)'},
    {'url': 'http://thzd.cc/forum.phpforum-254-1.html', 'title': '破解帐号专区'},
    {'url': 'http://thzd.cc/forum.phpforum-249-1.html', 'title': 'VIP资源交流'},
    {'url': 'http://thzd.cc/forum.phpforum-250-1.html', 'title': 'VIP问题解答'},
    {'url': 'http://thzd.cc/forum.phpforum-225-1.html', 'title': '网络资源交流'},
    {'url': 'http://thzd.cc/forum.phpforum-226-1.html', 'title': '邀请码交易'},
    {'url': 'http://thzd.cc/forum.phpforum-227-1.html', 'title': '桃花交易区'},
    {'url': 'http://thzd.cc/forum.phpforum-191-1.html', 'title': 'X-art'},
    {'url': 'http://thzd.cc/forum.phpforum-197-1.html', 'title': 'ABP系列'},
    {'url': 'http://thzd.cc/forum.phpforum-198-1.html', 'title': 'XXX-AV'},
    {'url': 'http://thzd.cc/forum.phpforum-199-1.html', 'title': '成人动漫'},
    {'url': 'http://thzd.cc/forum.phpforum-201-1.html', 'title': 'IPZ系列'},
    {'url': 'http://thzd.cc/forum.phpforum-202-1.html', 'title': 'Heyzo系列'},
    {'url': 'http://thzd.cc/forum.phpforum-204-1.html', 'title': 'SNIS系列'},
    {'url': 'http://thzd.cc/forum.phpforum-205-1.html', 'title': 'ADN系列'},
    {'url': 'http://thzd.cc/forum.phpforum-206-1.html', 'title': 'CHN系列'},
    {'url': 'http://thzd.cc/forum.phpforum-211-1.html', 'title': 'YRH系列'},
    {'url': 'http://thzd.cc/forum.phpforum-219-1.html', 'title': 'MIDE系列'},
    {'url': 'http://thzd.cc/forum.phpforum-222-1.html', 'title': 'MyWife系列'},
    {'url': 'http://thzd.cc/forum.phpforum-223-1.html', 'title': 'ODFA系列'},
    {'url': 'http://thzd.cc/forum.phpforum-230-1.html', 'title': 'BGN系列'},
    {'url': 'http://thzd.cc/forum.phpforum-231-1.html', 'title': 'Parm系列'},
    {'url': 'http://thzd.cc/forum.phpforum-245-1.html', 'title': 'WanZ系列'},
    {'url': 'http://thzd.cc/forum.phpforum-39-1.html', 'title': '日韩情色(BT)'},
    {'url': 'http://thzd.cc/forum.phpforum-40-1.html', 'title': '西方美人(BT)'},
    {'url': 'http://thzd.cc/forum.phpforum-60-1.html', 'title': '国产专栏（BT）'},
    {'url': 'http://thzd.cc/forum.phpforum-58-1.html', 'title': '三级伦理（BT）'},
    {'url': 'http://thzd.cc/forum.phpforum-41-1.html', 'title': '动漫精品（BT）'},
    {'url': 'http://thzd.cc/forum.phpforum-63-1.html', 'title': '精美套图（BT)'},
    {'url': 'http://thzd.cc/forum.phpforum-65-1.html', 'title': '精品视频'},
    {'url': 'http://thzd.cc/forum.phpforum-80-1.html', 'title': '日韓長片'},
    {'url': 'http://thzd.cc/forum.phpforum-81-1.html', 'title': '成人动漫'},
    {'url': 'http://thzd.cc/forum.phpforum-75-1.html', 'title': '亚洲无码'},
    {'url': 'http://thzd.cc/forum.phpforum-76-1.html', 'title': '亚洲有码'},
    {'url': 'http://thzd.cc/forum.phpforum-77-1.html', 'title': '欧美情色'},
    {'url': 'http://thzd.cc/forum.phpforum-78-1.html', 'title': '成人动漫'},
    {'url': 'http://thzd.cc/forum.phpforum-251-1.html', 'title': '中文字幕'},
    {'url': 'http://thzd.cc/forum.phpforum-252-1.html', 'title': '伦理写真'},
    {'url': 'http://thzd.cc/forum.phpforum-309-1.html', 'title': '桃花族门事件专区'},
    {'url': 'http://thzd.cc/forum.phpforum-312-1.html', 'title': '原味交易区'},
    {'url': 'http://thzd.cc/forum.phpforum-311-1.html', 'title': '国模专区'},
    {'url': 'http://thzd.cc/forum.phpforum-318-1.html', 'title': 'MFStar模范学院'},
    {'url': 'http://thzd.cc/forum.phpforum-267-1.html', 'title': 'TuiGirl推女郎'},
    {'url': 'http://thzd.cc/forum.phpforum-268-1.html', 'title': 'AISS爱丝'},
    {'url': 'http://thzd.cc/forum.phpforum-269-1.html', 'title': 'AAA女郎'},
    {'url': 'http://thzd.cc/forum.phpforum-270-1.html', 'title': 'ROSI写真'},
    {'url': 'http://thzd.cc/forum.phpforum-308-1.html', 'title': 'LEGBABY美腿宝贝'},
    {'url': 'http://thzd.cc/forum.phpforum-316-1.html', 'title': 'XIUREN秀人网'},
    {'url': 'http://thzd.cc/forum.phpforum-271-1.html', 'title': 'Beautyleg写真'},
    {'url': 'http://thzd.cc/forum.phpforum-272-1.html', 'title': '第DISI第四印象'},
    {'url': 'http://thzd.cc/forum.phpforum-273-1.html', 'title': 'LiGui丽柜'},
    {'url': 'http://thzd.cc/forum.phpforum-274-1.html', 'title': 'MASKED QUEEN假面女皇'},
    {'url': 'http://thzd.cc/forum.phpforum-275-1.html', 'title': 'ugirls尤果网'},
    {'url': 'http://thzd.cc/forum.phpforum-276-1.html', 'title': 'TGOD推女神'},
    {'url': 'http://thzd.cc/forum.phpforum-278-1.html', 'title': 'MiStar魅研社'},
    {'url': 'http://thzd.cc/forum.phpforum-279-1.html', 'title': 'BoLoli波萝社'},
    {'url': 'http://thzd.cc/forum.phpforum-280-1.html', 'title': 'MYGIRL美媛馆'},
    {'url': 'http://thzd.cc/forum.phpforum-281-1.html', 'title': '街拍专区'},
    {'url': 'http://thzd.cc/forum.phpforum-210-1.html', 'title': '其他写真'},
    {'url': 'http://thzd.cc/forum.phpforum-295-1.html', 'title': '國外寫真區'},
    {'url': 'http://thzd.cc/forum.phpforum-301-1.html', 'title': 'ISHOW爱秀'},
    {'url': 'http://thzd.cc/forum.phpforum-302-1.html', 'title': 'FEILIN嗲囡囡'},
    {'url': 'http://thzd.cc/forum.phpforum-303-1.html', 'title': '爱尤物'},
    {'url': 'http://thzd.cc/forum.phpforum-304-1.html', 'title': 'PANS盘丝洞'},
    {'url': 'http://thzd.cc/forum.phpforum-305-1.html', 'title': 'TouTiao头条女神'},
    {'url': 'http://thzd.cc/forum.phpforum-306-1.html', 'title': '动感小站'},
    {'url': 'http://thzd.cc/forum.phpforum-317-1.html', 'title': '108TV酱'},
    {'url': 'http://thzd.cc/forum.phpforum-319-1.html', 'title': '写真专区失效帖及补档汇总'},
    {'url': 'http://thzd.cc/forum.phpforum-320-1.html', 'title': 'KeLaGirls克拉女神'},
    {'url': 'http://thzd.cc/forum.phpforum-321-1.html', 'title': 'MiCat猫萌榜'},
    {'url': 'http://thzd.cc/forum.phpforum-322-1.html', 'title': 'MISSLEG'},
    {'url': 'http://thzd.cc/forum.phpforum-323-1.html', 'title': '黑丝爱HEISIAI'},
    {'url': 'http://thzd.cc/forum.phpforum-324-1.html', 'title': 'Girlt果团网'},
    {'url': 'http://thzd.cc/forum.phpforum-153-1.html', 'title': '真實錄音區'},
    {'url': 'http://thzd.cc/forum.phpforum-151-1.html', 'title': '有聲小說'},
    {'url': 'http://thzd.cc/forum.phpforum-152-1.html', 'title': '成人小說'},
    {'url': 'http://thzd.cc/forum.phpforum-154-1.html', 'title': '校園春色'},
    {'url': 'http://thzd.cc/forum.phpforum-155-1.html', 'title': '武俠玄幻'},
    {'url': 'http://thzd.cc/forum.phpforum-156-1.html', 'title': '完結小說'},
    {'url': 'http://thzd.cc/forum.phpforum-129-1.html', 'title': '博彩綜合討論區'},
    {'url': 'http://thzd.cc/forum.phpforum-130-1.html', 'title': '博彩問問'},
    {'url': 'http://thzd.cc/forum.phpforum-131-1.html', 'title': '博彩資訊'},
    {'url': 'http://thzd.cc/forum.phpforum-292-1.html', 'title': '时时彩讨论区'},
    {'url': 'http://thzd.cc/forum.phpforum-293-1.html', 'title': '福彩3D讨论区'},
    {'url': 'http://thzd.cc/forum.phpforum-294-1.html', 'title': '双色球讨论区'},
    {'url': 'http://thzd.cc/forum.phpforum-291-1.html', 'title': '会员验证区'},
    {'url': 'http://thzd.cc/forum.phpforum-283-1.html', 'title': '华东地区'},
    {'url': 'http://thzd.cc/forum.phpforum-284-1.html', 'title': '华南地区'},
    {'url': 'http://thzd.cc/forum.phpforum-285-1.html', 'title': '华中地区'},
    {'url': 'http://thzd.cc/forum.phpforum-286-1.html', 'title': '华北地区'},
    {'url': 'http://thzd.cc/forum.phpforum-287-1.html', 'title': '西北地区'},
    {'url': 'http://thzd.cc/forum.phpforum-288-1.html', 'title': '西南地区'},
    {'url': 'http://thzd.cc/forum.phpforum-289-1.html', 'title': '东北地区'},
    {'url': 'http://thzd.cc/forum.phpforum-290-1.html', 'title': '其它地區'},
    {'url': 'http://thzd.cc/forum.phpforum-242-1.html', 'title': 'AV涨姿势'},
    {'url': 'http://thzd.cc/forum.phpforum-243-1.html', 'title': '破解帐号'},
    {'url': 'http://thzd.cc/forum.phpforum-244-1.html', 'title': 'BT技术區'},
    {'url': 'http://thzd.cc/forum.phpforum-216-1.html', 'title': 'AV新闻'},
    {'url': 'http://thzd.cc/forum.phpforum-217-1.html', 'title': 'AV话题'},
    {'url': 'http://thzd.cc/forum.phpforum-218-1.html', 'title': '女优百科'},
    {'url': 'http://thzd.cc/forum.phpforum-44-1.html', 'title': '性知识话题'},
    {'url': 'http://thzd.cc/forum.phpforum-38-1.html', 'title': '成人交友区'},
    {'url': 'http://thzd.cc/forum.phpforum-49-1.html', 'title': '戒色特区'},
    {'url': 'http://thzd.cc/forum.phpforum-53-1.html', 'title': '桃花聊天室'},
    {'url': 'http://thzd.cc/forum.phpforum-179-1.html', 'title': '女优讨论区'},
    {'url': 'http://thzd.cc/forum.phpforum-178-1.html', 'title': '新手提问'},
    {'url': 'http://thzd.cc/forum.phpforum-84-1.html', 'title': '新手報道'},
    {'url': 'http://thzd.cc/forum.phpforum-176-1.html', 'title': '翻墙必备'},
    {'url': 'http://thzd.cc/forum.phpforum-240-1.html', 'title': '常用软件'}
}
