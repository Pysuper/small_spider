# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/23 下午7:18
# @Author  : Zheng Xingtao
# @File    : spider_30_taohua.py


import asyncio
import os
from pprint import pprint
import urllib.request
import aiohttp
from lxml import etree

loop = asyncio.get_event_loop()

base_url = "http://taohuazu9.com/"
start_url = "http://taohuazu9.com/forum.php?gid=190"
save_path = "/home/zheng/Videos/"


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
                        loop.create_task(parse_detail(session, category_task))
            except Exception as e:
                print(e)
            await asyncio.sleep(5)


async def parse_detail(session, task):
    """获取帖子的详细信息"""
    try:
        async with session.get(task["category_href"]) as response:
            html = await response.text()
            x_html = etree.HTML(html)

            detail_href_list = x_html.xpath("//ul[@id='waterfall']/li//h3/a/@href")
            detail_title_list = x_html.xpath("//ul[@id='waterfall']/li//h3/a/text()")
            image_href = x_html.xpath("""//ul[@id='waterfall']/li/div/a[@onclick="atarget(this)"]/img/@src""")[0]
            for detail_href, detail_title in zip(detail_href_list, detail_title_list):
                detail_task = {
                    'category_title': task["category_title"],
                    'category_href': task["category_href"],
                    'detail_title': detail_title.replace(" ", "").replace("/", "-"),
                    'detail_href': base_url + detail_href,
                    'image_href': image_href,
                }
                # pprint(detail_task)
            loop.create_task(get_torrent_page(session, detail_task))
    except Exception as e:
        print(e)
    await asyncio.sleep(5)


async def get_torrent_page(session, detail_task):
    """获取torrent下载页面"""
    try:
        async with session.get(detail_task["detail_href"]) as response:
            html = await response.text()
            x_html = etree.HTML(html)
            torrent_href = x_html.xpath("""//span[@onmouseover="showMenu({'ctrlid':this.id,'pos':'12'})"]/a/@href""")[0]
            torrent_name = x_html.xpath("""//span[@onmouseover="showMenu({'ctrlid':this.id,'pos':'12'})"]/a/text()""")[
                0]
            torrent_task = {
                "category_title": detail_task["category_title"],
                "category_href": detail_task["category_href"],
                "detail_title": detail_task["detail_title"],
                "detail_href": detail_task["detail_href"],
                "image_href": detail_task["image_href"],
                "torrent_href": base_url + torrent_href,
                "torrent_name": torrent_name,
            }
            # pprint(torrent_task)
            # print(randam, torrent_task)
            loop.create_task(get_torrent(session, torrent_task))
    except Exception as e:
        print(e)
    await asyncio.sleep(5)


async def get_torrent(session, torrent_task):
    """获取torrent下载链接"""
    try:
        async with session.get(torrent_task["torrent_href"]) as response:
            html = await response.text()
            x_html = etree.HTML(html)
            torrent_href = x_html.xpath("""//a[@onclick="hideWindow('imc_attachad')"]/@href""")[0]
            file_task = {
                "category_title": torrent_task["category_title"],
                "category_href": torrent_task["category_href"],
                "detail_title": torrent_task["detail_title"],
                "detail_href": torrent_task["detail_href"],
                "torrent_href": torrent_task["torrent_href"],
                "torrent_name": torrent_task["torrent_name"],
                "image_href": torrent_task["image_href"],
                "file_url": torrent_href
            }
            # pprint(file_task)
            loop.create_task(save_torrent(session, file_task))
    except Exception as e:
        print(e)
    await asyncio.sleep(5)


async def save_torrent(session, file_task):
    try:
        image_name = file_task["detail_title"] + ".jpg"
        torrent_name = file_task["torrent_name"]

        file_save_path = save_path + file_task["category_title"] + "/" + file_task["detail_title"] + "/"
        if not os.path.exists(file_save_path):
            os.makedirs(file_save_path)

        # 使用urllib.request
        urllib.request.urlretrieve(file_task["image_href"], file_save_path + image_name)
        urllib.request.urlretrieve(file_task["file_url"], file_save_path + torrent_name)

        # async with session.get(file_task["file_url"]) as torrent:
        #     pprint(file_task)
        #     with open(file_save_path + torrent_name, "w") as code:
        #         code.write(torrent.content)

        # a bytes-like object is required, not 'StreamReader'
        # async with session.get(file_task["image_href"]) as image:
        #     with open(file_save_path + image_name, "wb") as code:
        #         code.write(image.content.encode())

        print(os.getpid(), "{} 保存完成！".format(file_task["category_title"] + "--" + file_task["detail_title"]))
    except Exception as e:
        print(e)
    await asyncio.sleep(5)


# python 3.7
# asyncio.run(get_category())

# python 3.5
asyncio.get_event_loop().run_until_complete(get_category())
