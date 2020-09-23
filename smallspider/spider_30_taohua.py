# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/23 下午7:18
# @Author  : Zheng Xingtao
# @File    : spider_30_taohua.py


import asyncio
import aiohttp
from lxml import etree
from pprint import pprint

loop = asyncio.get_event_loop()

base_url = "http://taohuazu9.com/"
start_url = "http://taohuazu9.com/forum.php?gid=190"


async def get_category():
    """获取分类信息"""
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(start_url) as response:
                    html = await response.text()
                    x_html = etree.HTML(html)

                    category_href_list = x_html.xpath("//div[@id='category_190']//tr/td[2]/h2/a/@href")
                    category_title_list = x_html.xpath("//div[@id='category_190']//tr/td[2]/h2/a/text()")
                    for category_href, category_title in zip(category_href_list, category_title_list):
                        category_task = {
                            'category_title': category_title,
                            'category_href': base_url + category_href,
                        }
                        loop.create_task(parse_detail(category_task))
            except Exception as e:
                print(e)
            await asyncio.sleep(5)


async def parse_detail(task):
    """获取帖子的详细信息"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(task["category_href"]) as response:
                html = await response.text()
                x_html = etree.HTML(html)

                detail_href_list = x_html.xpath("//ul[@id='waterfall']/li//h3/a/@href")
                detail_title_list = x_html.xpath("//ul[@id='waterfall']/li//h3/a/text()")
                for detail_href, detail_title in zip(detail_href_list, detail_title_list):
                    detail_task = {
                        'category_title': task["category_title"],
                        'category_href': task["category_href"],
                        'detail_title': detail_title,
                        'detail_href': base_url + detail_href
                    }
                loop.create_task(download_img(session, detail_task))
        except Exception as e:
            print(e)
        await asyncio.sleep(5)


async def download_img(session, detail_task):
    """获取torrent下载链接"""
    try:
        async with session.get(detail_task["detail_href"]) as response:
            html = await response.text()
            x_html = etree.HTML(html)
            img_href = x_html.xpath("//span[@initialized='true']/a/@href")
            pprint(detail_task, img_href)
    except Exception as e:
        print(e)
    await asyncio.sleep(5)


# python 3.7
# asyncio.run(get_category())

# python 3.5
asyncio.get_event_loop().run_until_complete(get_category())
