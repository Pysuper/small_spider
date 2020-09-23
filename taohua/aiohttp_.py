# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/20 下午8:22
# @Author  : Zheng Xingtao
# @File    : aiohttp_.py


import asyncio
import aiohttp


async def get_home():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get("http://thzd.cc/forum-177-1.html") as response:
                    html = await response.text()
                    print(html)
            except:
                pass
            await asyncio.sleep(5)


asyncio.run(get_home())
