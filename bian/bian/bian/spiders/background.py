# -*- coding: utf-8 -*-
import scrapy
from bian.items import BianItem

class BackgroundSpider(scrapy.Spider):
    name = 'background'
    allowed_domains = ['netbian.com']
    start_urls = ['http://pic.netbian.com/index_2.html']

    def parse(self, response):
        # 获取响应
        li_list = response.xpath('//ul[@class="clearfix"]/li/a/img/@src')
        for li in li_list:
            print("http://pic.netbian.com" + li.extract())

