# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/23 下午9:09
# @Author  : Zheng Xingtao
# @File    : spider_31_taohua.py


import requests
from lxml import etree


class ParseTaoHua(object):
    def __init__(self):
        self.base_url = "http://taohuazu9.com/"
        self.start_url = "http://taohuazu9.com/forum.php?gid=190"
        self.header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"}

    def get_html(self, url):
        response = requests.get(url, headers=self.header)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        return None

    def get_category(self, html):
        x_html = etree.HTML(html)
        category_href_list = x_html.xpath("//div[@id='category_190']//tr/td[2]/h2/a/@href")
        category_title_list = x_html.xpath("//div[@id='category_190']//tr/td[2]/h2/a/text()")
        for category_href, category_title in zip(category_href_list, category_title_list):
            category_task = {
                'category_title': category_title,
                'category_href': self.base_url + category_href,
            }
            yield category_task

    def get_detail(self, html):
        print(html)
        x_html = etree.HTML(html)
        detail_href_list = x_html.xpath("//tr/th/a")

        for detail in detail_href_list:
            print("detail", detail)

        # detail_title_list = x_html.xpath("//tr/th/a[2]/text()")
        # for detail_href, detail_title in zip(detail_href_list, detail_title_list):
        #     detail_task = {
        #         'detail_title': detail_title,
        #         'detail_href': self.base_url + detail_href,
        #     }
        #     yield detail_task

    def run(self):
        base_html = self.get_html(self.start_url)
        for category_task in self.get_category(base_html):
            category_html = self.get_html(category_task["category_href"])

            print(category_task)
            self.get_detail(category_html)
            break


            # print(category_task)
            # for detail_task in self.get_detail(category_html):
            #     print(detail_task)
            #
            # break


if __name__ == '__main__':
    ParseTaoHua().run()
