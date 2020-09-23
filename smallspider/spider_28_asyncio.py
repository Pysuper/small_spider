# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Zheng Xingtao
# File : spider_28_asyncio
# Datetime : 2020/8/21 上午9:19

import asyncio
import aiohttp
from lxml import etree
from pprint import pprint

loop = asyncio.get_event_loop()


async def get_category():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get("http://www.nipic.com/photo") as response:
                    html = await response.text()
                    x_html = etree.HTML(html)

                    category_href_list = x_html.xpath("//div[@class='menu-box-bd']/dl/dd/a/@href")
                    category_title_list = x_html.xpath("//div[@class='menu-box-bd']/dl/dd/a/text()")
                    for category_href, category_title in zip(category_href_list, category_title_list):
                        category_task = {
                            'category_title': category_title,
                            'category_href': "http://www.nipic.com" + category_href,
                        }
                        loop.create_task(parse_detail(session, category_task))
            except Exception as e:
                print(e)
            await asyncio.sleep(5)


async def parse_detail(session, task):
    try:
        async with session.get(task["category_href"]) as response:
            html = await response.text()

            x_html = etree.HTML(html)
            detail_href_list = x_html.xpath("//div[@class='mainV2']//li/a/@href")
            detail_title_list = x_html.xpath("//div[@class='mainV2']//li/a/@title")
            for detail_href, detail_title in zip(detail_href_list, detail_title_list):
                detail_task = {
                    'category_href': task["category_href"],
                    'category_title': task["category_title"],
                    'detail_href': detail_href,
                    'detail_title': detail_title
                }
                loop.create_task(download_img(session, detail_task))
    except Exception as e:
        print(e)
    await asyncio.sleep(5)


async def download_img(session, detail_task):
    try:
        async with session.get(detail_task["detail_href"]) as response:
            html = await response.text()
            x_html = etree.HTML(html)
            img_href = x_html.xpath("//img[@class='works-img']/@src")[0]
            # for i in img_href:
            #     print(i)
            pprint(detail_task)
            print(img_href)
    except Exception as e:
        print(e)
    await asyncio.sleep(5)


# python 3.7
# asyncio.run(get_category())

# python 3.5
asyncio.get_event_loop().run_until_complete(get_category())
